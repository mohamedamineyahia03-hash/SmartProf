from flask import Flask, jsonify, request
from flask_cors import CORS
from data.skills_matrix import SKILLS_MATRIX
from diagnostic_engine import diagnose

app = Flask(__name__)
CORS(app)

SUBJECTS = [
    {"id": "math", "name": "Mathématiques"},
    {"id": "fr", "name": "Français"},
    {"id": "science", "name": "Sciences"},
    {"id": "en", "name": "Anglais"},
    {"id": "ar", "name": "Arabe"},
]

LEVELS = {
    "1": "1ère année primaire",
    "2": "2ème année primaire",
    "3": "3ème année primaire",
    "4": "4ème année primaire",
    "5": "5ème année primaire",
}


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SmartProf"}


@app.get("/api/subjects")
def subjects():
    return jsonify(SUBJECTS)


@app.get("/api/levels")
def levels():
    return jsonify(LEVELS)


@app.get("/api/skills")
def skills():
    return jsonify(SKILLS_MATRIX)


@app.post("/api/diagnostic")
def diagnostic():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    level = data.get("level")
    subject = data.get("subject")
    results = data.get("results", {})

    if str(level) not in LEVELS:
        return jsonify({"error": "Invalid level"}), 400

    if not isinstance(subject, str) or not subject:
        return jsonify({"error": "Subject is required"}), 400

    if subject not in {item["id"] for item in SUBJECTS}:
        return jsonify({"error": "Invalid subject"}), 400

    return jsonify(diagnose(level, subject, results))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
