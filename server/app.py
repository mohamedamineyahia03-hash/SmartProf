import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from db import db
from models import (
    CurriculumDomain,
    CurriculumDomainTrimester,
    CurriculumLevel,
    CurriculumSubject,
)
from diagnostic_engine import diagnose

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
