import hmac
import logging
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.orm import joinedload

from db import db
from models import (
    ChildProfile,
    CurriculumDomain,
    CurriculumLevel,
    CurriculumSkill,
    CurriculumSubject,
    LibraryCacheExercise,
    Payment,
    Session,
)
from academic_calendar import TRIMESTER_DATES, current_trimester, is_trimester_unlocked
from auth import authenticate, current_user, login_user, logout_user, register_user
from diagnostic_engine import diagnose
from entitlements import has_active_entitlement
from payments import bank_transfer
from session_engine import build_exam_session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FREE_CHILD_SLOTS = 2

# Set SMARTPROF_ENV=production on any real deployment. Gates the dev-secret
# check below and nothing else — local/dev/staging all behave as before.
IS_PRODUCTION = os.environ.get("SMARTPROF_ENV", "development") == "production"

app = Flask(__name__)

# Open by default (matches prior behaviour, convenient for local dev). Set
# ALLOWED_ORIGINS to a comma-separated list (e.g. "https://smartprof.tn")
# to restrict it — required before a real deployment goes live.
_allowed_origins = os.environ.get("ALLOWED_ORIGINS")
if _allowed_origins:
    CORS(app, origins=[o.strip() for o in _allowed_origins.split(",") if o.strip()])
else:
    CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "smartprof.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Dev fallback only — MUST be overridden via env var before any real deployment,
# otherwise session cookies could be forged by anyone who reads this source.
_DEV_SECRET_KEY = "dev-only-insecure-secret-change-in-production"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", _DEV_SECRET_KEY)
db.init_app(app)

# Dev fallback only, same rule as SECRET_KEY and library-service's API_KEY —
# gates the payment-confirmation admin routes. No admin/staff account system
# exists yet, so a shared key (checked in constant time) is the whole model.
_DEV_ADMIN_KEY = "dev-local-admin-key"
ADMIN_KEY = os.environ.get("ADMIN_KEY", _DEV_ADMIN_KEY)

if IS_PRODUCTION and (app.config["SECRET_KEY"] == _DEV_SECRET_KEY or ADMIN_KEY == _DEV_ADMIN_KEY):
    raise RuntimeError(
        "SMARTPROF_ENV=production but SECRET_KEY and/or ADMIN_KEY are still the dev "
        "defaults. Set both via environment variables before starting a real deployment."
    )

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per minute"], storage_uri="memory://")

# Local rotating log file — a real hosted error tracker (e.g. Sentry) needs its
# own account/DSN, which is a decision for whoever deploys this; this gives a
# durable local record of server errors in the meantime, in any environment.
_LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(_LOG_DIR, exist_ok=True)
_file_handler = RotatingFileHandler(os.path.join(_LOG_DIR, "app.log"), maxBytes=2_000_000, backupCount=5)
_file_handler.setLevel(logging.WARNING)
_file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
app.logger.addHandler(_file_handler)
app.logger.setLevel(logging.WARNING)


@app.errorhandler(Exception)
def _log_unhandled_exception(exc):
    from werkzeug.exceptions import HTTPException

    if isinstance(exc, HTTPException):
        return exc
    app.logger.exception("Unhandled exception on %s %s", request.method, request.path)
    return jsonify({"error": "internal_error"}), 500


@app.after_request
def _security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # 'unsafe-inline' is required because the app/vitrine pages use inline
    # <script>/<style> blocks rather than external files — this CSP still
    # blocks loading script/style/frames from any other origin, which is
    # the actual attack surface for stored/reflected XSS on this app.
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "object-src 'none'"
    )
    if IS_PRODUCTION:
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


def require_admin_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not hmac.compare_digest(request.headers.get("X-Admin-Key") or "", ADMIN_KEY):
            return jsonify({"error": "unauthorized"}), 401
        return fn(*args, **kwargs)

    return wrapper


@app.get("/")
def vitrine():
    """Public showcase page — mission, full programme structure, services,
    content-originality/licence statement. Never exposes actual exercise
    content (only structure via the already-public /api/subjects and
    /api/skills), on purpose: convince first, unlock via /app after."""
    return send_from_directory(BASE_DIR.replace("server", "web"), "vitrine.html")


@app.get("/app")
def index():
    return send_from_directory(BASE_DIR.replace("server", "web"), "index_smartprof_arabe_complet.html")


@app.get("/confidentialite")
def privacy_policy():
    return send_from_directory(BASE_DIR.replace("server", "web"), "confidentialite.html")


@app.get("/mentions-legales")
def legal_notice():
    return send_from_directory(BASE_DIR.replace("server", "web"), "mentions-legales.html")


@app.get("/cgu")
def terms_of_use():
    return send_from_directory(BASE_DIR.replace("server", "web"), "cgu.html")


@app.get("/robots.txt")
def robots_txt():
    return send_from_directory(BASE_DIR.replace("server", "web"), "robots.txt")


@app.get("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(BASE_DIR.replace("server", "web"), "sitemap.xml")


@app.get("/manifest.json")
def pwa_manifest():
    return send_from_directory(BASE_DIR.replace("server", "web"), "manifest.json")


@app.get("/sw.js")
def service_worker():
    # Servi depuis la racine (pas /app/sw.js) exprès : la portée par défaut
    # d'un service worker est son propre dossier, donc /sw.js est le seul
    # emplacement qui couvre à la fois / (vitrine) et /app (appli).
    return send_from_directory(
        BASE_DIR.replace("server", "web"), "sw.js", mimetype="application/javascript"
    )


@app.get("/icons/<path:filename>")
def pwa_icons(filename):
    return send_from_directory(os.path.join(BASE_DIR.replace("server", "web"), "icons"), filename)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SmartProf"}


@app.get("/api/subjects")
def subjects():
    """Accepts an optional ?child_id= so the frontend can show "essai gratuit"
    instead of a hard lock on a paid subject this child hasn't tried yet —
    see start_session() for where that free look is actually granted/spent."""
    rows = CurriculumSubject.query.order_by(CurriculumSubject.id).all()

    child_id = request.args.get("child_id", type=int)
    tried_subjects = set()
    if child_id is not None:
        tried_subjects = {
            row.subject_code
            for row in Session.query.filter_by(child_profile_id=child_id).with_entities(Session.subject_code).distinct()
        }

    client_ip = _client_ip()
    return jsonify(
        [
            {
                "id": s.code,
                "name": s.label_fr,
                "name_ar": s.label_ar,
                "free_levels": s.free_levels,
                "trial_available": (
                    child_id is not None
                    and s.code not in tried_subjects
                    and not _ip_already_used_trial(client_ip, s.code)
                ),
            }
            for s in rows
        ]
    )


@app.get("/api/levels")
def levels():
    rows = CurriculumLevel.query.order_by(CurriculumLevel.code).all()
    return jsonify({l.code: l.label_fr for l in rows})


@app.get("/api/skills")
def skills():
    """The section tree for every level x subject, consumed by the frontend to
    render the arborescence: "programme" sections grouped under the
    trimester tab they belong to, plus "expression" sections (Expression
    orale et écrite, Récitation) listed separately since they sit outside
    the trimester tabs entirely. Clicking a section starts an exam session
    scoped to its domain code (POST /api/session/start).

    Trimesters unlock progressively with the school calendar (see
    academic_calendar.is_trimester_unlocked) — identical for every level,
    since all levels follow the same Ministry calendar. current_trimester
    and trimester_starts let the frontend grey out T2/T3 before they open
    and explain when they will, without hardcoding the dates client-side."""
    tree = {}
    domains = CurriculumDomain.query.order_by(CurriculumDomain.sort_order).all()
    for domain in domains:
        level_code = domain.level.code
        subject_code = domain.subject.code
        section = {
            "code": domain.code,
            "name_fr": domain.name_fr,
            "name_ar": domain.name_ar,
            "skill_count": len(domain.skills),
        }
        subject_tree = tree.setdefault(level_code, {}).setdefault(
            subject_code, {"programme": {}, "expression": []}
        )
        if domain.category == "expression":
            subject_tree["expression"].append(section)
        else:
            trimesters = [t.trimester for t in domain.trimesters] or ["T1"]
            for trimester in trimesters:
                subject_tree["programme"].setdefault(trimester, []).append(section)

    return jsonify(
        {
            "levels": tree,
            "current_trimester": current_trimester(),
            "trimester_starts": {t: start.isoformat() for t, (start, _end) in TRIMESTER_DATES.items()},
        }
    )


@app.get("/api/v1/curriculum-schema")
def curriculum_schema():
    """Consumed by the external library-service to know which domains/skills/formats
    it needs to source and generate exercises for."""
    level_code = request.args.get("level")
    subject_code = request.args.get("subject")

    query = CurriculumDomain.query.join(CurriculumLevel).join(CurriculumSubject)
    if level_code:
        query = query.filter(CurriculumLevel.code == level_code)
    if subject_code:
        query = query.filter(CurriculumSubject.code == subject_code)

    domains = query.order_by(CurriculumDomain.sort_order).all()
    payload = []
    for domain in domains:
        payload.append(
            {
                "level": domain.level.code,
                "subject": domain.subject.code,
                "domain": domain.code,
                "name_fr": domain.name_fr,
                "name_ar": domain.name_ar,
                "trimesters": [t.trimester for t in domain.trimesters],
                "skills": [
                    {
                        "code": sk.code,
                        "name_fr": sk.name_fr,
                        "name_ar": sk.name_ar,
                        "exercise_formats": [f.format_code for f in sk.exercise_formats],
                    }
                    for sk in domain.skills
                ],
            }
        )
    return jsonify(payload)


@app.post("/api/diagnostic")
def diagnostic():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    level = data.get("level")
    subject = data.get("subject")
    results = data.get("results", {})

    level_row = CurriculumLevel.query.filter_by(code=str(level)).first()
    if level_row is None:
        return jsonify({"error": "Invalid level"}), 400

    if not isinstance(subject, str) or not subject:
        return jsonify({"error": "Subject is required"}), 400

    subject_row = CurriculumSubject.query.filter_by(code=subject).first()
    if subject_row is None:
        return jsonify({"error": "Invalid subject"}), 400

    return jsonify(diagnose(str(level), subject, results))


def child_payload(child):
    return {"id": child.id, "display_name": child.display_name, "level_code": child.level_code}


def user_payload(user):
    children = ChildProfile.query.filter_by(user_id=user.id).order_by(ChildProfile.id).all()
    return {
        "id": user.id,
        "email": user.email,
        "children": [child_payload(c) for c in children],
        "free_child_slots": FREE_CHILD_SLOTS,
        "referral_code": user.referral_code,
    }


@app.post("/api/auth/register")
@limiter.limit("10 per hour")
def register():
    data = request.get_json(silent=True) or {}
    user, error = register_user(data.get("email"), data.get("password"), data.get("ref"))

    if error == "invalid_email":
        return jsonify({"error": error, "message": "Adresse email invalide."}), 400
    if error == "password_too_short":
        return jsonify(
            {"error": error, "message": "Le mot de passe doit contenir au moins 8 caractères."}
        ), 400
    if error == "email_already_registered":
        return jsonify({"error": error, "message": "Un compte existe déjà avec cet email."}), 409

    login_user(user)
    return jsonify(user_payload(user)), 201


@app.post("/api/auth/login")
@limiter.limit("15 per hour")
def login():
    data = request.get_json(silent=True) or {}
    user = authenticate(data.get("email"), data.get("password"))
    if user is None:
        return jsonify({"error": "invalid_credentials", "message": "Email ou mot de passe incorrect."}), 401

    login_user(user)
    return jsonify(user_payload(user))


@app.post("/api/auth/logout")
def logout():
    logout_user()
    return jsonify({"status": "ok"})


@app.get("/api/auth/me")
def me():
    user = current_user()
    if user is None:
        return jsonify({"error": "not_authenticated"}), 401
    return jsonify(user_payload(user))


@app.post("/api/children")
def add_child():
    user = current_user()
    if user is None:
        return jsonify({"error": "not_authenticated"}), 401

    data = request.get_json(silent=True) or {}
    display_name = (data.get("display_name") or "").strip()
    level_code = str(data.get("level_code", ""))

    if not display_name:
        return jsonify({"error": "display_name_required", "message": "Le prénom de l'enfant est requis."}), 400
    if not CurriculumLevel.query.filter_by(code=level_code).first():
        return jsonify({"error": "invalid_level", "message": "Niveau invalide."}), 400

    existing_count = ChildProfile.query.filter_by(user_id=user.id).count()
    if existing_count >= FREE_CHILD_SLOTS:
        return jsonify(
            {
                "error": "supplement_required",
                "message": f"Un supplément payant est nécessaire à partir du {FREE_CHILD_SLOTS + 1}ème enfant (bientôt disponible).",
            }
        ), 402

    child = ChildProfile(user_id=user.id, display_name=display_name, level_code=level_code)
    db.session.add(child)
    db.session.commit()

    return jsonify(child_payload(child)), 201


def _as_naive_utc(dt):
    """Normalizes a datetime for comparison regardless of whether it came back
    tz-aware or naive from the DB (SQLite doesn't consistently preserve tzinfo)."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _skill_labels(skill_codes, lang):
    """Batched version of _skill_label — one query for every code instead of
    one per code, used by child_report() where both skill breakdowns can
    otherwise issue dozens of individual lookups."""
    skill_codes = list(skill_codes)
    if not skill_codes:
        return {}
    rows = CurriculumSkill.query.filter(CurriculumSkill.code.in_(skill_codes)).all()
    found = {row.code: (row.name_ar if lang == "ar" else row.name_fr) for row in rows}
    return {code: found.get(code, code.replace("_", " ")) for code in skill_codes}


def _session_score(session_row):
    # "correct" is None for grading_mode="open" answers (expression écrite /
    # récitation) — they're recorded but never scored, so they're excluded
    # from both the numerator and the denominator here.
    graded = [a for a in (session_row.answers or {}).values() if a.get("correct") is not None]
    correct = sum(1 for a in graded if a.get("correct"))
    return correct, len(graded)


@app.get("/api/children/<int:child_id>/report")
def child_report(child_id):
    """Progress report: last activity + trends, deliberately NOT live/real-time
    presence — the design choice is to show history, not surveil whether a
    child is 'online right now', which reads as monitoring rather than support."""
    user = current_user()
    if user is None:
        return jsonify({"error": "not_authenticated"}), 401

    child = ChildProfile.query.filter_by(id=child_id, user_id=user.id).first()
    if child is None:
        return jsonify({"error": "not_found"}), 404

    lang = request.args.get("lang", "fr")
    sessions = (
        Session.query.filter_by(child_profile_id=child.id).order_by(Session.created_at.desc()).all()
    )

    last_activity = sessions[0].created_at if sessions else None

    week_ago = _as_naive_utc(datetime.now(timezone.utc) - timedelta(days=7))
    week_sessions = [s for s in sessions if _as_naive_utc(s.created_at) and _as_naive_utc(s.created_at) >= week_ago]

    week_correct = week_total = 0
    for s in week_sessions:
        c, t = _session_score(s)
        week_correct += c
        week_total += t
    average_this_week = round(100 * week_correct / week_total) if week_total else None

    # Compétences vraiment travaillées CETTE semaine -- distinct de skills
    # plus bas qui agrège tout l'historique. C'est le coeur du récap hebdo :
    # pas juste "N séances", mais sur quoi précisément.
    week_skill_stats = {}
    for s in week_sessions:
        for answer in (s.answers or {}).values():
            skill = answer.get("skill")
            if not skill or answer.get("correct") is None:
                continue
            stats = week_skill_stats.setdefault(skill, {"correct": 0, "total": 0})
            stats["total"] += 1
            if answer.get("correct"):
                stats["correct"] += 1
    week_labels = _skill_labels(week_skill_stats.keys(), lang)
    skills_this_week = [
        {
            "skill": skill,
            "label": week_labels[skill],
            "correct": stats["correct"],
            "total": stats["total"],
            "percentage": round(100 * stats["correct"] / stats["total"]) if stats["total"] else 0,
        }
        for skill, stats in week_skill_stats.items()
    ]
    skills_this_week.sort(key=lambda s: s["total"], reverse=True)

    skill_stats = {}
    for s in sessions:
        for answer in (s.answers or {}).values():
            skill = answer.get("skill")
            if not skill or answer.get("correct") is None:  # None = ungraded (grading_mode="open")
                continue
            stats = skill_stats.setdefault(skill, {"correct": 0, "total": 0})
            stats["total"] += 1
            if answer.get("correct"):
                stats["correct"] += 1

    all_labels = _skill_labels(skill_stats.keys(), lang)
    skills = [
        {
            "skill": skill,
            "label": all_labels[skill],
            "correct": stats["correct"],
            "total": stats["total"],
            "percentage": round(100 * stats["correct"] / stats["total"]) if stats["total"] else 0,
        }
        for skill, stats in skill_stats.items()
    ]
    skills.sort(key=lambda s: s["percentage"], reverse=True)

    # Require at least 2 attempts before calling something a strength/weakness —
    # one lucky or unlucky answer isn't a pattern.
    evaluable = [s for s in skills if s["total"] >= 2]
    strengths = [s for s in evaluable if s["percentage"] >= 70][:3]
    weaknesses = [s for s in evaluable if s["percentage"] < 50][:3]

    recent_sessions = []
    for s in sessions[:10]:
        correct, total = _session_score(s)
        recent_sessions.append(
            {
                "id": s.id,
                "subject": s.subject_code,
                "level": s.level_code,
                "score": correct,
                "total": total,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "completed": s.completed_at is not None,
            }
        )

    return jsonify(
        {
            "child": child_payload(child),
            "last_activity": last_activity.isoformat() if last_activity else None,
            "sessions_this_week": len(week_sessions),
            "average_this_week": average_this_week,
            "skills_this_week": skills_this_week,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "skills": skills,
            "recent_sessions": recent_sessions,
        }
    )


def _client_ip():
    """Best-effort client IP — prefers X-Forwarded-For's first hop for once
    this sits behind a reverse proxy/load balancer, falls back to the direct
    socket address otherwise. Used only to slow down casual free-trial abuse
    (see Session.client_ip); not a fraud-proof device fingerprint."""
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _ip_already_used_trial(client_ip, subject_code):
    return client_ip != "unknown" and (
        Session.query.filter_by(subject_code=subject_code, client_ip=client_ip, is_trial=True).first() is not None
    )


def is_subject_locked(level_code, subject_row, user_id=None):
    """A subject requires an unlock at any level not listed in its free_levels
    (e.g. Fr/En at levels 1-2, En also at level 3) -- unless this user holds
    an active Entitlement for it (granted by a confirmed payment)."""
    if level_code in (subject_row.free_levels or []):
        return False
    return not has_active_entitlement(user_id, subject_row.code, level_code)


def public_content(content):
    """Strips the answer and the pedagogical explanation out of what's sent to
    the browser before it's answered — revealed only by
    GET /api/session/<id>/corrige, once every exercise in the session has an
    answer. A "récit à plusieurs questions" exercise nests its own
    answer/explanation inside each sub_questions[i], so those need
    stripping too. model_answer is the grading_mode="open" equivalent
    (expression écrite / récitation) — same rule, same hiding point."""
    hidden_keys = {"answer", "explanation", "model_answer"}
    public = {k: v for k, v in content.items() if k not in hidden_keys}
    if "sub_questions" in public:
        public["sub_questions"] = [
            {k: v for k, v in sub.items() if k not in hidden_keys} for sub in public["sub_questions"]
        ]
    return public


def public_exercise_payload(exercise):
    if exercise is None:
        return None
    return {
        "id": exercise.id,
        "domain": exercise.domain_code,
        "skill": exercise.skill_code,
        "format": exercise.exercise_format,
        "difficulty": exercise.difficulty,
        "language": exercise.language,
        "grading_mode": exercise.grading_mode,
        "content": public_content(exercise.content),
    }


@app.post("/api/session/start")
def start_session():
    data = request.get_json(silent=True) or {}
    level_code = str(data.get("level", ""))
    subject_code = data.get("subject", "")
    domain_code = data.get("domain", "")
    child_id = data.get("child_id")

    # child_id is optional (anonymous play still works), but when present it
    # must belong to the logged-in parent — this is what lets two devices each
    # attribute their own session to a different child, fully independently:
    # nothing here serializes across devices, so two children can be mid-session
    # in parallel with no coordination needed.
    user = current_user()
    child = None
    if child_id is not None:
        if user is None:
            return jsonify(
                {"error": "not_authenticated", "message": "Connexion parent requise pour sélectionner un enfant."}
            ), 401
        child = ChildProfile.query.filter_by(id=child_id, user_id=user.id).first()
        if child is None:
            return jsonify({"error": "invalid_child", "message": "Enfant introuvable."}), 400

    level_row = CurriculumLevel.query.filter_by(code=level_code).first()
    if level_row is None:
        return jsonify({"error": "invalid_level"}), 400

    subject_row = CurriculumSubject.query.filter_by(code=subject_code).first()
    if subject_row is None:
        return jsonify({"error": "invalid_subject"}), 400

    subject_locked = is_subject_locked(level_code, subject_row, user_id=user.id if user else None)
    if subject_locked:
        # One free look per child per paid subject (any level, any section) —
        # a diagnostic trial before asking a parent to pay, not a loophole:
        # anonymous play (no child) never gets it, it's spent the moment this
        # child has any session logged for the subject (same query
        # /api/subjects uses to advertise "essai gratuit"), and it's also
        # denied if this same device/IP has already spent a trial on this
        # subject under a different child or account — see _client_ip.
        client_ip = _client_ip()
        trial_available = (
            child is not None
            and Session.query.filter_by(child_profile_id=child.id, subject_code=subject_code).first() is None
            and not _ip_already_used_trial(client_ip, subject_code)
        )
        if not trial_available:
            return jsonify(
                {
                    "error": "subject_locked",
                    "message": "Cette matière nécessite un déblocage.",
                }
            ), 403

    domain_row = CurriculumDomain.query.filter_by(
        level_id=level_row.id, subject_id=subject_row.id, code=domain_code
    ).first()
    if domain_row is None:
        return jsonify({"error": "invalid_domain"}), 400

    # "programme" domains can span several trimesters — the frontend sends
    # which tab it was browsing under; "expression" domains have none, so
    # this stays empty. Exercise selection below is scoped by domain_code
    # alone, not by trimester — trimester here is purely descriptive except
    # for the unlock check right after.
    domain_trimesters = [t.trimester for t in domain_row.trimesters]
    trimester = data.get("trimester") or (domain_trimesters[0] if domain_trimesters else "")

    if domain_row.category != "expression" and not is_trimester_unlocked(trimester):
        return jsonify(
            {
                "error": "trimester_locked",
                "message": "Ce trimestre n'est pas encore débloqué.",
            }
        ), 403

    exercises = build_exam_session(level_code, subject_code, domain_code)
    if not exercises:
        return jsonify(
            {
                "error": "no_content",
                "message": "Aucun exercice n'est encore disponible pour cette section.",
            }
        ), 404

    session_row = Session(
        child_profile_id=child.id if child else None,
        level_code=level_code,
        subject_code=subject_code,
        trimester=trimester,
        domain_code=domain_code,
        exercise_ids=[e.id for e in exercises],
        answers={},
        client_ip=_client_ip(),
        user_agent=(request.headers.get("User-Agent") or "")[:255],
        is_trial=subject_locked,
    )
    db.session.add(session_row)
    db.session.commit()

    return jsonify(
        {
            "session_id": session_row.id,
            "domain": domain_code,
            "trimester": trimester,
            "total": len(exercises),
            "exercises": [public_exercise_payload(e) for e in exercises],
        }
    )


def _session_access_denied(session_row):
    """Anonymous play (no child attached) stays open to whoever holds the
    session_id, matching the rest of the anonymous-play support. A session
    tied to a child is only visible to that child's own parent account —
    session_id is a plain auto-incrementing int, trivially enumerable, so
    without this check anyone could read another child's answers/scores,
    read any corrige (bypassing the paywall on locked subjects), or post
    fake answers into a session that isn't theirs while it's still open."""
    if session_row.child_profile_id is None:
        return False
    user = current_user()
    if user is None:
        return True
    child = ChildProfile.query.filter_by(id=session_row.child_profile_id, user_id=user.id).first()
    return child is None


@app.get("/api/session/<int:session_id>")
def get_session(session_id):
    session_row = Session.query.get(session_id)
    if session_row is None:
        return jsonify({"error": "not_found"}), 404
    if _session_access_denied(session_row):
        return jsonify({"error": "forbidden"}), 403

    exercises = LibraryCacheExercise.query.filter(
        LibraryCacheExercise.id.in_(session_row.exercise_ids)
    ).all()
    by_id = {e.id: e for e in exercises}
    ordered = [by_id[eid] for eid in session_row.exercise_ids if eid in by_id]

    return jsonify(
        {
            "session_id": session_row.id,
            "level": session_row.level_code,
            "subject": session_row.subject_code,
            "trimester": session_row.trimester,
            "exercises": [public_exercise_payload(e) for e in ordered],
            "answers": session_row.answers,
            "completed_at": session_row.completed_at.isoformat() if session_row.completed_at else None,
        }
    )


@app.post("/api/session/<int:session_id>/answer")
def answer_session(session_id):
    session_row = Session.query.get(session_id)
    if session_row is None:
        return jsonify({"error": "not_found"}), 404
    if _session_access_denied(session_row):
        return jsonify({"error": "forbidden"}), 403
    if session_row.completed_at is not None:
        return jsonify({"error": "session_already_completed"}), 400

    data = request.get_json(silent=True) or {}
    try:
        exercise_id = int(data.get("exercise_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_exercise_id"}), 400
    given = data.get("answer")

    if exercise_id not in session_row.exercise_ids:
        return jsonify({"error": "exercise_not_in_session"}), 400

    exercise = LibraryCacheExercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({"error": "exercise_not_found"}), 404

    def normalize(value):
        return str(value).strip().lower()

    # grading_mode="open" (expression écrite / récitation): recorded but
    # never scored — "correct" stays None, which _session_score/child_report
    # both know to exclude from the score fraction.
    sub_results = None
    if exercise.grading_mode == "open":
        is_correct = None
    else:
        sub_questions = exercise.content.get("sub_questions")
        if sub_questions is not None:
            # "Récit à plusieurs questions" (problemes/recit_multi_questions):
            # one narrative, several sub-questions graded together as a
            # single exercise slot — correct only if every sub-answer is.
            given_list = given if isinstance(given, list) else []
            sub_results = []
            for i, sub in enumerate(sub_questions):
                given_i = given_list[i] if i < len(given_list) else None
                sub_correct = given_i is not None and normalize(given_i) == normalize(sub.get("answer"))
                sub_results.append(
                    {
                        "correct": sub_correct,
                        "correct_answer": sub.get("answer"),
                        "explanation": sub.get("explanation"),
                    }
                )
            is_correct = all(r["correct"] for r in sub_results)
        else:
            is_correct = normalize(given) == normalize(exercise.content.get("answer"))

    answer_entry = {"given": given, "correct": is_correct, "skill": exercise.skill_code}
    if sub_results is not None:
        answer_entry["sub_results"] = sub_results

    answers = dict(session_row.answers or {})
    answers[str(exercise_id)] = answer_entry
    session_row.answers = answers

    # Session-examen : pas de corrigé immédiat (voir GET .../corrige) — on se
    # contente d'enregistrer la réponse et de savoir si tout est répondu.
    if len(answers) >= len(session_row.exercise_ids):
        session_row.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify(
        {
            "stored": True,
            "answered_count": len(answers),
            "total": len(session_row.exercise_ids),
            "completed": session_row.completed_at is not None,
        }
    )


@app.get("/api/session/<int:session_id>/corrige")
def session_corrige(session_id):
    """Full answer key + score, available only once every exercise in the
    session has an answer — session-examen shows no per-question feedback
    (see answer_session above), so this is the only place correctness is
    ever revealed to the child."""
    session_row = Session.query.get(session_id)
    if session_row is None:
        return jsonify({"error": "not_found"}), 404
    if _session_access_denied(session_row):
        return jsonify({"error": "forbidden"}), 403
    if session_row.completed_at is None:
        return jsonify(
            {"error": "session_not_completed", "message": "Termine d'abord toutes les questions."}
        ), 400

    exercises = LibraryCacheExercise.query.filter(LibraryCacheExercise.id.in_(session_row.exercise_ids)).all()
    by_id = {e.id: e for e in exercises}
    ordered = [by_id[eid] for eid in session_row.exercise_ids if eid in by_id]

    items = []
    score = 0
    graded_total = 0
    for exercise in ordered:
        answer_entry = (session_row.answers or {}).get(str(exercise.id), {})
        is_correct = answer_entry.get("correct")
        graded = is_correct is not None

        item = {
            "exercise_id": exercise.id,
            "question": exercise.content.get("question"),
            "given": answer_entry.get("given"),
            "graded": graded,
            "correct": is_correct,
        }
        if exercise.content.get("sub_questions") is not None:
            item["sub_results"] = answer_entry.get("sub_results", [])
        else:
            item["correct_answer"] = exercise.content.get("answer")
            item["explanation"] = exercise.content.get("explanation")
        if not graded:
            item["model_answer"] = exercise.content.get("model_answer")
        if exercise.exercise_format == "recitation":
            item["text"] = exercise.content.get("text")
            item["author"] = exercise.content.get("author")

        if graded:
            graded_total += 1
            if is_correct:
                score += 1
        items.append(item)

    return jsonify(
        {
            "session_id": session_row.id,
            "score": score,
            "graded_total": graded_total,
            "total": len(ordered),
            "items": items,
        }
    )


def serialize_payment(payment):
    return {
        "id": payment.id,
        "subject": payment.subject_code,
        "level": payment.level_code,
        "billing_cycle": payment.billing_cycle,
        "provider": payment.provider,
        "status": payment.status,
        "reference": payment.reference,
        "amount_tnd": float(payment.amount_tnd) if payment.amount_tnd is not None else None,
        "created_at": payment.created_at.isoformat() if payment.created_at else None,
        "verified_at": payment.verified_at.isoformat() if payment.verified_at else None,
    }


@app.post("/api/payments/bank-transfer/request")
@limiter.limit("20 per hour")
def request_bank_transfer():
    """Creates a trackable Payment and hands back a reference + the
    business's RIB — the transfer itself happens outside this app entirely.
    Nothing is unlocked here; only POST /api/admin/payments/<id>/verify
    (a human, looking at the real bank statement) can do that."""
    user = current_user()
    if user is None:
        return jsonify({"error": "not_authenticated", "message": "Connexion parent requise."}), 401

    data = request.get_json(silent=True) or {}
    level_code = str(data.get("level", ""))
    subject_code = data.get("subject", "")
    billing_cycle = data.get("billing_cycle", "annual")

    subject_row = CurriculumSubject.query.filter_by(code=subject_code).first()
    if subject_row is None:
        return jsonify({"error": "invalid_subject"}), 400
    if CurriculumLevel.query.filter_by(code=level_code).first() is None:
        return jsonify({"error": "invalid_level"}), 400
    # Anything other than "annual" is treated by bank_transfer.verify() as a
    # never-expiring one_time grant -- without this check a caller could send
    # billing_cycle="whatever" and get permanent access confirmed for the
    # price of an annual one, since the admin only sees the label, not this
    # branch, when confirming.
    if billing_cycle not in ("annual", "one_time"):
        return jsonify({"error": "invalid_billing_cycle"}), 400

    payment = bank_transfer.create_request(user.id, subject_code, level_code, billing_cycle)
    return jsonify({"payment": serialize_payment(payment), "bank_details": bank_transfer.bank_details()})


@app.get("/api/payments/mine")
def my_payments():
    user = current_user()
    if user is None:
        return jsonify({"error": "not_authenticated"}), 401
    rows = Payment.query.filter_by(user_id=user.id).order_by(Payment.created_at.desc()).all()
    return jsonify([serialize_payment(p) for p in rows])


@app.get("/api/admin/payments/pending")
@require_admin_key
def admin_pending_payments():
    rows = (
        Payment.query.options(joinedload(Payment.user))
        .filter_by(status="pending_verification")
        .order_by(Payment.created_at)
        .all()
    )
    return jsonify(
        [
            {
                **serialize_payment(p),
                "user_email": p.user.email,
            }
            for p in rows
        ]
    )


@app.post("/api/admin/payments/<int:payment_id>/verify")
@require_admin_key
def admin_verify_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment is None:
        return jsonify({"error": "not_found"}), 404
    data = request.get_json(silent=True) or {}
    amount_tnd = data.get("amount_tnd")
    # amount_tnd is admin-supplied free text on the confirmation page (see
    # web/admin_payments.html) -- reject anything that isn't a plausible
    # positive amount rather than trusting it straight into the Numeric(8,2)
    # column (a negative value would "confirm" a transfer that pays nothing,
    # a non-numeric value would blow up at the DB layer instead of a clean 400).
    if amount_tnd is not None:
        if isinstance(amount_tnd, bool) or not isinstance(amount_tnd, (int, float)):
            return jsonify({"error": "invalid_amount"}), 400
        if amount_tnd <= 0 or amount_tnd > 999999.99:
            return jsonify({"error": "invalid_amount"}), 400
    bank_transfer.verify(payment, verified_by=data.get("verified_by", "admin"), amount_tnd=amount_tnd)
    return jsonify(serialize_payment(payment))


@app.get("/admin/payments")
def admin_payments_page():
    """Internal payment-confirmation tool — gated by the same X-Admin-Key
    the JSON routes require (entered client-side), not linked from
    anywhere public."""
    return send_from_directory(BASE_DIR.replace("server", "web"), "admin_payments.html")


if __name__ == "__main__":
    # debug=True (autoreload + interactive debugger) only outside production —
    # never expose the Werkzeug debugger publicly.
    app.run(host="127.0.0.1", port=5000, debug=not IS_PRODUCTION)
