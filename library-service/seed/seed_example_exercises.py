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
            "content_fr": {
                "question": "Compte les pommes et écris le nombre.",
                "answer": 4,
                "explanation": "Pointe chaque pomme du doigt en comptant une seule fois : 1, 2, 3, 4. Il y a bien 4 pommes en tout.",
            },
            "content_ar": {
                "question": "عدّ التفاحات واكتب العدد.",
                "answer": 4,
                "explanation": "أشر إلى كل تفاحة وعدّها مرة واحدة فقط: 1، 2، 3، 4. المجموع هو 4 تفاحات.",
            },
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
            "content_fr": {
                "question": "Combien font 3 + 2 ?",
                "choices": ["4", "5", "6"],
                "answer": "5",
                "explanation": "Pars de 3 et avance de 2 : 4, 5. Donc 3 + 2 = 5.",
            },
            "content_ar": {
                "question": "كم مجموع 3 + 2؟",
                "choices": ["4", "5", "6"],
                "answer": "5",
                "explanation": "ابدأ من 3 وتقدّم خطوتين: 4، 5. إذن 3 + 2 = 5.",
            },
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
                "explanation": "Un triangle a exactement 3 côtés et 3 sommets. Le carré en a 4, et le cercle n'a pas de côtés droits.",
            },
            "content_ar": {
                "question": "أي شكل له 3 أضلاع؟",
                "choices": ["مربع", "مثلث", "دائرة"],
                "answer": "مثلث",
                "explanation": "المثلث له بالضبط 3 أضلاع و3 رؤوس. أما المربع فله 4 أضلاع، والدائرة ليس لها أضلاع مستقيمة.",
            },
        },
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/numeration-comparaison",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "numeration",
            "trimester_hint": "T1",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de comparaison de petits nombres (source d'inspiration uniquement).",
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T1",
            "domain_code": "numeration",
            "skill_code": "ordre_nombres",
            "exercise_format": "selection",
            "difficulty": "decouverte",
            "content_fr": {
                "question": "Quel est le plus grand nombre ?",
                "choices": ["3", "7", "5"],
                "answer": "7",
                "explanation": "Compare les nombres deux à deux : 7 est plus grand que 3 et plus grand que 5. C'est donc le plus grand des trois.",
            },
            "content_ar": {
                "question": "ما هو أكبر عدد؟",
                "choices": ["3", "7", "5"],
                "answer": "7",
                "explanation": "قارن الأعداد اثنين اثنين: 7 أكبر من 3 وأكبر من 5. إذن هو الأكبر بين الثلاثة.",
            },
        },
    },
    {
        "source": {
            "url": "https://example-manuel-tunisien.tn/math1/problemes-additifs",
            "title": "Manuel Mathématiques 1ère année (exemple)",
            "license_status": "unlicensed",
            "subject_code": "math",
            "level_code": "1",
            "domain_hint": "problemes",
            "trimester_hint": "T2",
            "region_scope": "tunisia_official",
            "content_snapshot": "Exemple de petit problème additif avec récit (source d'inspiration uniquement).",
            "status": "used_for_generation",
        },
        "exercise": {
            "subject_code": "math",
            "level_code": "1",
            "trimester": "T2",
            "domain_code": "problemes",
            "skill_code": "resoudre",
            "exercise_format": "saisie_nombre",
            "difficulty": "maitrise",
            "content_fr": {
                "question": "Léa a 6 billes. Elle en gagne 3 de plus. Combien de billes a-t-elle maintenant ?",
                "answer": 9,
                "explanation": "Léa gagne des billes, donc on additionne : 6 + 3 = 9. Elle a maintenant 9 billes.",
            },
            "content_ar": {
                "question": "لدى ليلى 6 كرات. ربحت 3 كرات إضافية. كم كرة أصبح لديها الآن؟",
                "answer": 9,
                "explanation": "ليلى ربحت كرات، إذن نجمع: 6 + 3 = 9. أصبح لديها الآن 9 كرات.",
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
