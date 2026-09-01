import os
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from db import db
from models import (
    ChildProfile,
    CurriculumDomain,
    CurriculumLevel,
    CurriculumSkill,
    CurriculumSubject,
    LibraryCacheExercise,
    Session,
)
from academic_calendar import current_trimester
from auth import authenticate, current_user, login_user, logout_user, register_user
from diagnostic_engine import diagnose
from session_engine import SESSION_SIZE, STARTING_DIFFICULTY, next_difficulty, pick_next_exercise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FREE_CHILD_SLOTS = 2

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "smartprof.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Dev fallback only — MUST be overridden via env var before any real deployment,
# otherwise session cookies could be forged by anyone who reads this source.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-insecure-secret-change-in-production")
db.init_app(app)


@app.get("/")
def index():
    return send_from_directory(BASE_DIR.replace("server", "web"), "index_smartprof_arabe_complet.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SmartProf"}


@app.get("/api/subjects")
def subjects():
    rows = CurriculumSubject.query.order_by(CurriculumSubject.id).all()
    return jsonify(
        [
            {
                "id": s.code,
                "name": s.label_fr,
                "name_ar": s.label_ar,
                "is_free_at_level1_2": s.is_free_at_level1_2,
                "is_free_at_level3_5": s.is_free_at_level3_5,
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
    """Curriculum domains/skills for every level x subject, keyed the same way the
    legacy SKILLS_MATRIX was, but sourced from the DB and at skill granularity."""
    result = {}
    domains = (
        CurriculumDomain.query.order_by(CurriculumDomain.sort_order)
        .all()
    )
    for domain in domains:
        level_code = domain.level.code
        subject_code = domain.subject.code
        trimesters = [t.trimester for t in domain.trimesters] or ["T1"]
        skill_codes = [sk.code for sk in domain.skills]
        result.setdefault(level_code, {}).setdefault(subject_code, {})
        for trimester in trimesters:
            result[level_code][subject_code].setdefault(trimester, [])
            result[level_code][subject_code][trimester].extend(skill_codes)
    return jsonify(result)


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
    }


@app.post("/api/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    user, error = register_user(data.get("email"), data.get("password"))

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


def _skill_label(skill_code, lang):
    skill = CurriculumSkill.query.filter_by(code=skill_code).first()
    if skill is None:
        return skill_code.replace("_", " ")
    return skill.name_ar if lang == "ar" else skill.name_fr


def _session_score(session_row):
    answers = session_row.answers or {}
    correct = sum(1 for a in answers.values() if a.get("correct"))
    return correct, len(answers)


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

    skill_stats = {}
    for s in sessions:
        for answer in (s.answers or {}).values():
            skill = answer.get("skill")
            if not skill:
                continue
            stats = skill_stats.setdefault(skill, {"correct": 0, "total": 0})
            stats["total"] += 1
            if answer.get("correct"):
                stats["correct"] += 1

    skills = [
        {
            "skill": skill,
            "label": _skill_label(skill, lang),
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
            "strengths": strengths,
            "weaknesses": weaknesses,
            "skills": skills,
            "recent_sessions": recent_sessions,
        }
    )


def is_subject_locked(level_code, subject_row):
    """Fr/En require an unlock at levels 1-2; no account/entitlement system exists
    yet (Phase 4), so those two are always locked for now — the free subjects
    (math/science/ar, and everything at levels 3-5) are never affected."""
    if level_code in ("1", "2"):
        return not subject_row.is_free_at_level1_2
    return not subject_row.is_free_at_level3_5


def public_exercise_payload(exercise):
    """Strips the answer and the pedagogical explanation out of what's sent to
    the browser before it's answered — both are only ever revealed by
    /api/session/<id>/answer, after the child has submitted a response."""
    if exercise is None:
        return None
    hidden_keys = {"answer", "explanation"}
    return {
        "id": exercise.id,
        "domain": exercise.domain_code,
        "skill": exercise.skill_code,
        "format": exercise.exercise_format,
        "difficulty": exercise.difficulty,
        "content_fr": {k: v for k, v in exercise.content_fr.items() if k not in hidden_keys},
        "content_ar": {k: v for k, v in exercise.content_ar.items() if k not in hidden_keys},
    }


@app.post("/api/session/start")
def start_session():
    data = request.get_json(silent=True) or {}
    level_code = str(data.get("level", ""))
    subject_code = data.get("subject", "")
    child_id = data.get("child_id")

    # child_id is optional (anonymous play still works), but when present it
    # must belong to the logged-in parent — this is what lets two devices each
    # attribute their own session to a different child, fully independently:
    # nothing here serializes across devices, so two children can be mid-session
    # in parallel with no coordination needed.
    child = None
    if child_id is not None:
        user = current_user()
        if user is None:
            return jsonify(
                {"error": "not_authenticated", "message": "Connexion parent requise pour sélectionner un enfant."}
            ), 401
        child = ChildProfile.query.filter_by(id=child_id, user_id=user.id).first()
        if child is None:
            return jsonify({"error": "invalid_child", "message": "Enfant introuvable."}), 400

    if not CurriculumLevel.query.filter_by(code=level_code).first():
        return jsonify({"error": "invalid_level"}), 400

    subject_row = CurriculumSubject.query.filter_by(code=subject_code).first()
    if subject_row is None:
        return jsonify({"error": "invalid_subject"}), 400

    if is_subject_locked(level_code, subject_row):
        return jsonify(
            {
                "error": "subject_locked",
                "message": "Cette matière nécessite un déblocage.",
            }
        ), 403

    trimester = current_trimester()
    exercise = pick_next_exercise(level_code, subject_code, trimester, STARTING_DIFFICULTY)
    if exercise is None:
        return jsonify(
            {
                "error": "no_content",
                "message": "Aucun exercice n'est encore disponible pour ce choix.",
            }
        ), 404

    session_row = Session(
        child_profile_id=child.id if child else None,
        level_code=level_code,
        subject_code=subject_code,
        trimester=trimester,
        exercise_ids=[exercise.id],
        answers={},
        current_difficulty=STARTING_DIFFICULTY,
    )
    db.session.add(session_row)
    db.session.commit()

    return jsonify(
        {
            "session_id": session_row.id,
            "trimester": trimester,
            "total_target": SESSION_SIZE,
            "exercise": public_exercise_payload(exercise),
        }
    )


@app.get("/api/session/<int:session_id>")
def get_session(session_id):
    session_row = Session.query.get(session_id)
    if session_row is None:
        return jsonify({"error": "not_found"}), 404

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

    correct_values = {
        normalize(exercise.content_fr.get("answer")),
        normalize(exercise.content_ar.get("answer")),
    }
    is_correct = normalize(given) in correct_values

    answers = dict(session_row.answers or {})
    answers[str(exercise_id)] = {"given": given, "correct": is_correct, "skill": exercise.skill_code}
    session_row.answers = answers
    session_row.current_difficulty = next_difficulty(session_row.current_difficulty, is_correct)

    next_exercise = None
    if len(answers) < SESSION_SIZE:
        weak_skills = {a["skill"] for a in answers.values() if not a["correct"]}
        next_exercise = pick_next_exercise(
            session_row.level_code,
            session_row.subject_code,
            session_row.trimester,
            session_row.current_difficulty,
            excluded_ids=session_row.exercise_ids,
            weak_skill_codes=weak_skills,
        )
        if next_exercise is not None:
            session_row.exercise_ids = session_row.exercise_ids + [next_exercise.id]

    if next_exercise is None:
        session_row.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify(
        {
            "correct": is_correct,
            "correct_answer_fr": exercise.content_fr.get("answer"),
            "correct_answer_ar": exercise.content_ar.get("answer"),
            "explanation_fr": exercise.content_fr.get("explanation"),
            "explanation_ar": exercise.content_ar.get("explanation"),
            "completed": session_row.completed_at is not None,
            "score": sum(1 for a in answers.values() if a["correct"]),
            "total": len(answers),
            "next_exercise": public_exercise_payload(next_exercise),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
