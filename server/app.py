from flask import Flask, jsonify

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
