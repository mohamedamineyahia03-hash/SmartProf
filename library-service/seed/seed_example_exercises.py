"""Phase 1 seed: a handful of example exercises with real provenance (source ->
generation_run -> exercise), so the sync API and the Main App's pull job can be
exercised end-to-end before the real crawler/generation pipeline exists (Phase 2).

These specific rows are manually authored placeholders, not real AI-generated
content — they exist only to prove the FK chain and the export contract work.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # library-service/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import Exercise, GenerationRun, Source  # noqa: E402

EXAMPLES = [
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/numeration",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de dénombrement d'objets illustrés (source d'inspiration uniquement).",
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "denombrement",
            "exercise_format": "comptage",
            "difficulty": "en_cours",
            "content_fr": {"question": "Compte les pommes et écris le nombre.", "answer": 4},
            "content_ar": {"question": "عدّ التفاحات واكتب العدد.", "answer": 4},
        },
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/calcul",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "calcul",
            "trimester_hint": "T1",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple d'addition simple avec supports visuels (source d'inspiration uniquement).",
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "calcul",
            "skill_code": "addition",
            "exercise_format": "qcm",
            "difficulty": "en_cours",
            "content_fr": {"question": "Combien font 3 + 2 ?", "choices": ["4", "5", "6"], "answer": "5"},
            "content_ar": {"question": "كم مجموع 3 + 2؟", "choices": ["4", "5", "6"], "answer": "5"},
        },
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/geometrie",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "espace_geometrie",
            "trimester_hint": "T3",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de reconnaissance de formes géométriques (source d'inspiration uniquement).",
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T3",
            "domain_code": "espace_geometrie",
            "skill_code": "formes",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "content_fr": {
                "question": "Quelle forme a 3 côtés ?",
                "choices": ["carré", "triangle", "cercle"],
                "answer": "triangle",
            },
            "content_ar": {
                "question": "أي شكل له 3 أضلاع؟",
                "choices": ["مربع", "مثلث", "دائرة"],
                "answer": "مثلث",
            },
        },
    },
]


def main():
    with app.app_context():
        db.create_all()

        if Exercise.query.first() is not None:
            print("Examples already seeded, skipping.")
            return

        for example in EXAMPLES:
            source = Source(**example["source"])
            db.session.add(source)
            db.session.flush()

            generation_run = GenerationRun(
                source_id=source.id,
                model_provider="anthropic",
                model_name="claude-opus-5",
                prompt_template_version="v1-seed-example",
                status="success",
                raw_model_output="(seed example, not a real model call)",
            )
            db.session.add(generation_run)
            db.session.flush()

            exercise = Exercise(
                generation_run_id=generation_run.id,
                source_id=source.id,
                review_status="approved",
                reviewed_by="seed-script",
                status="published",
                curriculum_schema_version="v1",
                **example["exercise"],
            )
            db.session.add(exercise)

        db.session.commit()
        print(f"Seeded {len(EXAMPLES)} example exercises.")


if __name__ == "__main__":
    main()
