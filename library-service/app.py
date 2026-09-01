import os
from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS

from db import db
from generation.publish import approve, reject
from models import Exercise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("LIBRARY_SERVICE_API_KEY", "dev-local-key")

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "LIBRARY_DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "library.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def require_service_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-Api-Key") != API_KEY:
            return jsonify({"error": "unauthorized"}), 401
        return fn(*args, **kwargs)

    return wrapper


def serialize_exercise(exercise):
    return {
        "id": exercise.id,
        "level": exercise.level_code,
        "subject": exercise.subject_code,
        "trimester": exercise.trimester,
        "domain": exercise.domain_code,
        "skill": exercise.skill_code,
        "format": exercise.exercise_format,
        "difficulty": exercise.difficulty,
        "language": exercise.language,
        "content": exercise.content,
        "license": exercise.license,
        "status": exercise.status,
        "source_id": exercise.source_id,
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SmartProf Library Service"}


@app.get("/api/v1/exercises/export")
@require_service_api_key
def export_exercises():
    """Pulled periodically by the Main App's sync job (server/sync/library_sync.py).
    Only ever returns published exercises — this service is never in a student's
    live request path, so it's fine for this endpoint to be the sole point of
    contact between the two services."""
    level = request.args.get("level")
    subject = request.args.get("subject")
    trimester = request.args.get("trimester")
    domain = request.args.get("domain")
    status = request.args.get("status", "published")
    since = request.args.get("since", default=0, type=int)
    limit = min(request.args.get("limit", default=100, type=int), 500)

    query = Exercise.query.filter(Exercise.status == status, Exercise.id > since)
    if level:
        query = query.filter(Exercise.level_code == level)
    if subject:
        query = query.filter(Exercise.subject_code == subject)
    if trimester:
        query = query.filter(Exercise.trimester == trimester)
    if domain:
        query = query.filter(Exercise.domain_code == domain)

    rows = query.order_by(Exercise.id).limit(limit).all()
    return jsonify(
        {
            "exercises": [serialize_exercise(r) for r in rows],
            "next_cursor": rows[-1].id if rows else since,
            "count": len(rows),
        }
    )


@app.get("/api/v1/exercises/<int:exercise_id>")
@require_service_api_key
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(serialize_exercise(exercise))


def serialize_admin_exercise(exercise):
    payload = serialize_exercise(exercise)
    payload["review_status"] = exercise.review_status
    payload["reviewed_by"] = exercise.reviewed_by
    return payload


@app.get("/api/admin/exercises/pending")
@require_service_api_key
def admin_pending_exercises():
    """Internal review queue — not exposed to the Main App or end users."""
    rows = Exercise.query.filter_by(status="draft").order_by(Exercise.created_at).all()
    return jsonify([serialize_admin_exercise(e) for e in rows])


@app.post("/api/admin/exercises/<int:exercise_id>/approve")
@require_service_api_key
def admin_approve_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({"error": "not_found"}), 404
    approve(exercise)
    return jsonify(serialize_admin_exercise(exercise))


@app.post("/api/admin/exercises/<int:exercise_id>/reject")
@require_service_api_key
def admin_reject_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is None:
        return jsonify({"error": "not_found"}), 404
    reject(exercise)
    return jsonify(serialize_admin_exercise(exercise))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
