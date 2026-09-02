"""Seed: starter content for the "expression" category sections (Expression
orale et écrite for arabe/français, plus Récitation for français) —
independent sections outside the trimester tree, see server/models.py
CurriculumDomain.category and data/arabic1/arabic1_curriculum.json,
data/fr1/fr1_curriculum.json.

All grading_mode="open": there is no single canonical answer to check, so
each exercise carries a "model_answer" (or, for récitation, just the text
to read) shown to the child as a self-check reference — never scored (see
server/app.py answer_session/_session_score, which exclude "open" answers
from the score fraction).

Content here is either an original short prompt (written for this seed, not
sourced/copied) or a traditional/anonymous French comptine in the public
domain (no identifiable living author, centuries-old oral tradition) — the
same "never copy a licensed source" policy the AI generation pipeline
enforces, just authored directly since there's no ANTHROPIC_API_KEY
configured yet and this content doesn't need external inspiration.

trimester="T1" below is a required-but-inert placeholder: "expression"
sections aren't trimester-gated (build_exam_session filters by domain_code
alone), so this value is never read for these entries.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # library-service/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import Exercise, GenerationRun, Source  # noqa: E402

SOURCE_URL_PREFIX = "local://expression_recitation_seed_v1"


def _source(id_suffix, subject_code, domain_hint, content_snapshot):
    return {
        "url": f"{SOURCE_URL_PREFIX}#{id_suffix}",
        "title": "Contenu Expression orale/écrite et Récitation (rédigé pour SmartProf)",
        "license_status": "explicit_open",
        "subject_code": subject_code,
        "level_code": "1",
        "domain_hint": domain_hint,
        "trimester_hint": None,
        "region_scope": "tunisia_web",
        "content_snapshot": content_snapshot,
        "status": "used_for_generation",
    }


EXAMPLES = [
    # --- Arabe : وصف صورة (شفوي) ---
    {
        "source": _source("AR_EXPR_001", "ar", "expression_orale_ecrite", "Prompt original — décrire une scène illustrée."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "wasf_sura",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "ar",
            "grading_mode": "open",
            "content": {
                "mode": "orale",
                "question": "صِفْ ما تراه في هذا المشهد بجملة واحدة على الأقل.",
                "visual": "🏠🌳☁",
                "model_answer": "مثال: أرى بيتًا بجانب شجرة كبيرة، والسماء بها غيوم.",
            },
        },
    },
    {
        "source": _source("AR_EXPR_002", "ar", "expression_orale_ecrite", "Prompt original — décrire une scène illustrée."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "wasf_sura",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "ar",
            "grading_mode": "open",
            "content": {
                "mode": "orale",
                "question": "صِفْ ما تراه في هذا المشهد بجملة واحدة على الأقل.",
                "visual": "🐱🐦🌸",
                "model_answer": "مثال: أرى قطة وعصفورًا بالقرب من زهرة.",
            },
        },
    },
    # --- Arabe : ترتيب الكلمات (مُصحَّح آليًا) ---
    {
        "source": _source("AR_EXPR_003", "ar", "expression_orale_ecrite", "Prompt original — ordonner les mots d'une phrase."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "tartib_kalimat",
            "exercise_format": "qcm", "difficulty": "en_cours", "language": "ar",
            "content": {
                "question": "رتّب الكلمات لتكوين جملة صحيحة: (المدرسة - إلى - أذهب)",
                "answer": "أذهب إلى المدرسة",
                "explanation": "الترتيب الصحيح للجملة يبدأ بالفعل ثم شبه الجملة: أذهب إلى المدرسة.",
                "choices": ["أذهب إلى المدرسة", "المدرسة أذهب إلى", "إلى أذهب المدرسة"],
            },
        },
    },
    {
        "source": _source("AR_EXPR_004", "ar", "expression_orale_ecrite", "Prompt original — ordonner les mots d'une phrase."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "tartib_kalimat",
            "exercise_format": "qcm", "difficulty": "en_cours", "language": "ar",
            "content": {
                "question": "رتّب الكلمات لتكوين جملة صحيحة: (كبيرة - القطة - جميلة)",
                "answer": "القطة جميلة كبيرة",
                "explanation": "الجملة تبدأ بالمبتدأ (القطة) ثم الصفات: القطة جميلة كبيرة.",
                "choices": ["القطة جميلة كبيرة", "كبيرة جميلة القطة", "جميلة كبيرة القطة"],
            },
        },
    },
    # --- Arabe : كتابة قصيرة (كتابي) ---
    {
        "source": _source("AR_EXPR_005", "ar", "expression_orale_ecrite", "Prompt original — rédaction courte."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "kitaba_qasira",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "ar",
            "grading_mode": "open",
            "content": {
                "mode": "ecrite",
                "question": "اكتب جملتين عن يومك في المدرسة.",
                "model_answer": "مثال: ذهبت إلى المدرسة صباحًا. تعلمت حروفًا جديدة مع معلمتي.",
            },
        },
    },
    {
        "source": _source("AR_EXPR_006", "ar", "expression_orale_ecrite", "Prompt original — rédaction courte."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "kitaba_qasira",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "ar",
            "grading_mode": "open",
            "content": {
                "mode": "ecrite",
                "question": "اكتب جملتين تصف فيهما أفراد عائلتك.",
                "model_answer": "مثال: أبي يعمل كل يوم. أمي تطبخ طعامًا لذيذًا.",
            },
        },
    },
    # --- Français : décrire une image (oral) ---
    {
        "source": _source("FR_EXPR_001", "fr", "expression_orale_ecrite", "Prompt original — décrire une scène illustrée."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "decrire_image",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "mode": "orale",
                "question": "Décris ce que tu vois sur cette image en une phrase au moins.",
                "visual": "🏠🌳☁",
                "model_answer": "Exemple : Je vois une maison à côté d'un grand arbre, et le ciel a des nuages.",
            },
        },
    },
    {
        "source": _source("FR_EXPR_002", "fr", "expression_orale_ecrite", "Prompt original — décrire une scène illustrée."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "decrire_image",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "mode": "orale",
                "question": "Décris ce que tu vois sur cette image en une phrase au moins.",
                "visual": "🐱🐦🌸",
                "model_answer": "Exemple : Je vois un chat et un oiseau près d'une fleur.",
            },
        },
    },
    # --- Français : raconter une histoire (oral) ---
    {
        "source": _source("FR_EXPR_003", "fr", "expression_orale_ecrite", "Prompt original — raconter un moment de la journée."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "raconter_histoire",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "mode": "orale",
                "question": "Raconte en 2 ou 3 phrases ce qui se passe un matin d'école.",
                "model_answer": "Exemple : Je me réveille tôt. Je prends mon petit-déjeuner. Puis je pars à l'école avec mon cartable.",
            },
        },
    },
    # --- Français : rédaction courte (écrit) ---
    {
        "source": _source("FR_EXPR_004", "fr", "expression_orale_ecrite", "Prompt original — rédaction courte."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "redaction_courte",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "mode": "ecrite",
                "question": "Écris deux phrases sur ta journée à l'école.",
                "model_answer": "Exemple : Je suis allé(e) à l'école ce matin. J'ai appris les lettres avec ma maîtresse.",
            },
        },
    },
    {
        "source": _source("FR_EXPR_005", "fr", "expression_orale_ecrite", "Prompt original — rédaction courte."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "expression_orale_ecrite", "skill_code": "redaction_courte",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "mode": "ecrite",
                "question": "Écris deux phrases pour décrire ta famille.",
                "model_answer": "Exemple : Mon papa travaille tous les jours. Ma maman prépare de bons repas.",
            },
        },
    },
    # --- Français : Récitation (comptines traditionnelles, domaine public) ---
    {
        "source": _source(
            "FR_RECIT_001", "fr", "recitation",
            "Comptine traditionnelle française, transmission orale, domaine public — aucun auteur identifiable.",
        ),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "recitation", "skill_code": "poeme_court",
            "exercise_format": "recitation", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Écoute puis récite ce poème à voix haute.",
                "text": "Une souris verte\nQui courait dans l'herbe,\nJe l'attrape par la queue,\nJe la montre à ces messieurs.\nCes messieurs me disent :\nTrempez-la dans l'huile,\nTrempez-la dans l'eau,\nÇa fera un escargot\nTout chaud.",
                "author": "Comptine traditionnelle",
            },
        },
    },
    {
        "source": _source(
            "FR_RECIT_002", "fr", "recitation",
            "Comptine traditionnelle française, transmission orale, domaine public — aucun auteur identifiable.",
        ),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "recitation", "skill_code": "poeme_court",
            "exercise_format": "recitation", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Écoute puis récite ce poème à voix haute.",
                "text": "Ainsi font, font, font\nLes petites marionnettes,\nAinsi font, font, font\nTrois petits tours et puis s'en vont.",
                "author": "Comptine traditionnelle",
            },
        },
    },
    {
        "source": _source(
            "FR_RECIT_003", "fr", "recitation",
            "Comptine traditionnelle française, transmission orale, domaine public — aucun auteur identifiable.",
        ),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "recitation", "skill_code": "poeme_court",
            "exercise_format": "recitation", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Écoute puis récite ce poème à voix haute.",
                "text": "Frère Jacques, Frère Jacques,\nDormez-vous ? Dormez-vous ?\nSonnez les matines, sonnez les matines,\nDing ding dong, ding ding dong.",
                "author": "Comptine traditionnelle",
            },
        },
    },
]


def main():
    with app.app_context():
        db.create_all()

        if Exercise.query.filter(Exercise.source_id.isnot(None)).join(Source).filter(
            Source.url.like(f"{SOURCE_URL_PREFIX}%")
        ).first() is not None:
            print("Expression/récitation examples already seeded, skipping.")
            return

        for example in EXAMPLES:
            source = Source(**example["source"])
            db.session.add(source)
            db.session.flush()

            generation_run = GenerationRun(
                source_id=source.id,
                model_provider="anthropic",
                model_name="claude-opus-5",
                prompt_template_version="v1-expression-seed",
                status="success",
                raw_model_output="(hand-authored seed content, not a real model call)",
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
        print(f"Seeded {len(EXAMPLES)} expression/récitation exercises.")


if __name__ == "__main__":
    main()
