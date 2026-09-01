import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from db import db
from models import (
    CurriculumDomain,
    CurriculumLevel,
    CurriculumSubject,
    LibraryCacheExercise,
    Session,
)
from academic_calendar import current_trimester
from diagnostic_engine import diagnose
from session_engine import SESSION_SIZE, STARTING_DIFFICULTY, next_difficulty, pick_next_exercise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "smartprof.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
