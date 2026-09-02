"""Seed: starter content for the "expression" category sections — Production
écrite (arabe/français) and Récitation (français only) — independent
sections outside the trimester tree, see server/models.py
CurriculumDomain.category and data/arabic1/arabic1_curriculum.json,
data/fr1/fr1_curriculum.json.

Oral expression was removed (2026-09-02): the section depended on working
speech synthesis for the "listen to the model" step, which wasn't reliable
enough to ship as a real feature — both curriculum files now call this
domain "production_ecrite" (Production écrite / الإنتاج الكتابي), written
only. Récitation keeps its "listen" button since read-aloud is TTS playing
back a fixed poem, not something the exercise depends on the child hearing
correctly to attempt.

grading_mode="auto" skills (ikmal_al_jumla, tartib_kalimat) are exact-match
QCM. grading_mode="open" skills (takwin_jumla, taabir_an_sura,
tartib_ahdath, intaj_hurr_muwajjah, décrire_image/raconter_histoire/
redaction_courte in French, récitation) carry a model_answer shown as a
self-check reference — never scored (see server/app.py answer_session/
_session_score, which exclude "open" answers from the score fraction).

The Arabic production_ecrite set (18 exercises, 6 skills) adapts the
exercise types from a user-supplied example worksheet (fill-in-the-blank
with a word bank, word ordering, sentence construction from given words,
describing a situation/picture, event sequencing, free guided production)
— not copied verbatim as a single fixed worksheet, but split one exercise
per prompt and re-authored so each stands alone with its own explanation/
model_answer, consistent with how every other seed script here works.
French content is either an original short prompt (written for this seed)
or a traditional/anonymous French comptine in the public domain (no
identifiable living author, centuries-old oral tradition) — same
"never copy a licensed source" policy the AI generation pipeline enforces,
just authored directly since there's no ANTHROPIC_API_KEY configured yet.

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

SOURCE_URL_PREFIX = "local://expression_recitation_seed_v2"


def _source(id_suffix, subject_code, domain_hint, content_snapshot):
    return {
        "url": f"{SOURCE_URL_PREFIX}#{id_suffix}",
        "title": "Contenu Production écrite et Récitation (rédigé pour SmartProf)",
        "license_status": "explicit_open",
        "subject_code": subject_code,
        "level_code": "1",
        "domain_hint": domain_hint,
        "trimester_hint": None,
        "region_scope": "tunisia_web",
        "content_snapshot": content_snapshot,
        "status": "used_for_generation",
    }


def _auto(id_suffix, skill, question, choices, answer, explanation):
    return {
        "source": _source(id_suffix, "ar", "production_ecrite", "Prompt original — exercice à choix, style adapté d'un exemple fourni."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": skill,
            "exercise_format": "qcm", "difficulty": "en_cours", "language": "ar",
            "content": {"question": question, "choices": choices, "answer": answer, "explanation": explanation},
        },
    }


def _open_ar(id_suffix, skill, question, model_answer, visual=None):
    content = {"question": question, "model_answer": model_answer}
    if visual:
        content["visual"] = visual
    return {
        "source": _source(id_suffix, "ar", "production_ecrite", "Prompt original — production libre, style adapté d'un exemple fourni."),
        "exercise": {
            "subject_code": "ar", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": skill,
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "ar",
            "grading_mode": "open",
            "content": content,
        },
    }


EXAMPLES = [
    # --- Arabe : إكمال الجملة (بمخزون كلمات، مُصحَّح آليًا) ---
    _auto("AR_PE_001", "ikmal_al_jumla", "أكمل بالكلمة المناسبة: أذهب إلى ...........",
          ["المدرسة", "القلم", "اللعب"], "المدرسة", "نذهب إلى المدرسة للتعلّم، فالكلمة المناسبة: المدرسة."),
    _auto("AR_PE_002", "ikmal_al_jumla", "أكمل بالكلمة المناسبة: هذا ........... جميل.",
          ["القلم", "المدرسة", "اللعب"], "القلم", "القلم أداة يمكن وصفها بأنها جميلة، فالكلمة المناسبة: القلم."),
    _auto("AR_PE_003", "ikmal_al_jumla", "أكمل بالكلمة المناسبة: أحب ...........",
          ["اللعب", "القلم", "المدرسة"], "اللعب", "اللعب نشاط نحب القيام به، فالكلمة المناسبة: اللعب."),
    _auto("AR_PE_004", "ikmal_al_jumla", "أكمل الجملة: القطة تأكل ...........",
          ["🐟 السمكة", "⚽ الكرة"], "🐟 السمكة", "القطة حيوان يأكل السمك، فالإجابة الصحيحة: السمكة."),
    _auto("AR_PE_005", "ikmal_al_jumla", "أكمل الجملة: الشمس ...........",
          ["مضيئة", "باردة"], "مضيئة", "الشمس مصدر للضوء والحرارة، فهي مضيئة."),
    _auto("AR_PE_006", "ikmal_al_jumla", "أكمل بالفعل المناسب: أبي ........... السيارة.",
          ["يقود", "تطبخ", "يلعب"], "يقود", "الأب يقود السيارة، فالفعل المناسب: يقود."),
    _auto("AR_PE_007", "ikmal_al_jumla", "أكمل بالفعل المناسب: أمي ........... الطعام.",
          ["تطبخ", "يلعب", "يقود"], "تطبخ", "الأم تطبخ الطعام، فالفعل المناسب: تطبخ."),
    _auto("AR_PE_008", "ikmal_al_jumla", "أكمل بالفعل المناسب: سامي ........... بالكرة.",
          ["يلعب", "يقود", "تطبخ"], "يلعب", "سامي يلعب بالكرة، فالفعل المناسب: يلعب."),

    # --- Arabe : ترتيب الكلمات (مُصحَّح آليًا) ---
    _auto("AR_PE_009", "tartib_kalimat", "رتّب الكلمات لتكوين جملة مفيدة: (يحب – سامي – اللعب)",
          ["سامي يحب اللعب", "يحب سامي اللعب", "اللعب يحب سامي"], "سامي يحب اللعب",
          "الجملة المفيدة تبدأ بالفاعل (سامي) ثم الفعل (يحب) ثم المفعول به (اللعب)."),

    # --- Arabe : تكوين جملة من كلمات معطاة (حرّ) ---
    _open_ar("AR_PE_010", "takwin_jumla", "كوّن جملة باستعمال كلمة: أمي", "مثال: أمي تحبني كثيرًا."),
    _open_ar("AR_PE_011", "takwin_jumla", "كوّن جملة مفيدة، استعمل الكلمات: ليلى – تفاحة – تأكل", "مثال: ليلى تأكل تفاحة."),
    _open_ar("AR_PE_012", "takwin_jumla", "أنتج جملة، استعمل الكلمات: أبي – الحديقة – شجرة – يسقي", "مثال: أبي يسقي شجرة في الحديقة."),

    # --- Arabe : التعبير عن صورة أو موقف (حرّ) ---
    _open_ar("AR_PE_013", "taabir_an_sura", "تخيّل صورة لطفل يلعب بالكرة. اكتب جملة مناسبة:",
             "مثال: الطفل يلعب بالكرة في الساحة.", visual="⚽"),
    _open_ar("AR_PE_014", "taabir_an_sura", "اقرأ: علي في المدرسة. يكتب في كراسه. اكتب جملة عن علي:",
             "مثال: علي يكتب في كراسه بعناية."),
    _open_ar("AR_PE_015", "taabir_an_sura", "الموقف: طفلان يلعبان بالكرة في ساحة المدرسة. استعمل الكلمات: طفلان – الكرة – الساحة – يلعبان",
             "مثال: الطفلان يلعبان بالكرة في ساحة المدرسة.", visual="⚽"),
    _open_ar("AR_PE_016", "taabir_an_sura", "الموقف: عصفور فوق شجرة، وطفل ينظر إليه. اكتب جملتين:",
             "مثال: العصفور فوق الشجرة. الطفل ينظر إلى العصفور بفرح.", visual="🐦🌳"),
    _open_ar("AR_PE_017", "taabir_an_sura", "الموقف: طفلة لديها قطة، وهي تلعب معها. اكتب جملتين:",
             "مثال: للطفلة قطة صغيرة. هي تلعب معها كل يوم.", visual="🐱"),

    # --- Arabe : ترتيب الأحداث (حرّ) ---
    _open_ar("AR_PE_018", "tartib_ahdath",
             "رتّب الأحداث التالية حسب تسلسلها الزمني ثم اكتبها بالترتيب: (يذهب سامي إلى المدرسة / يستيقظ سامي / يتناول سامي فطوره)",
             "الترتيب الصحيح: 1) يستيقظ سامي. 2) يتناول سامي فطوره. 3) يذهب سامي إلى المدرسة."),

    # --- Arabe : إنتاج كتابي حرّ موجّه ---
    _open_ar("AR_PE_019", "intaj_hurr_muwajjah",
             "اكتب 3 جمل عن عائلتك. يمكنك استعمال الكلمات: أبي – أمي – أخي – أختي – البيت – أحب – ألعب",
             "مثال: أبي يعمل بجدّ. أمي تهتمّ بنا. أحب اللعب مع أخي في البيت."),

    # --- Français : décrire une image ---
    {
        "source": _source("FR_PE_001", "fr", "production_ecrite", "Prompt original — décrire une scène illustrée."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": "decrire_image",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Décris ce que tu vois sur cette image en une phrase au moins.",
                "visual": "🏠🌳☁",
                "model_answer": "Exemple : Je vois une maison à côté d'un grand arbre, et le ciel a des nuages.",
            },
        },
    },
    {
        "source": _source("FR_PE_002", "fr", "production_ecrite", "Prompt original — décrire une scène illustrée."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": "decrire_image",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Décris ce que tu vois sur cette image en une phrase au moins.",
                "visual": "🐱🐦🌸",
                "model_answer": "Exemple : Je vois un chat et un oiseau près d'une fleur.",
            },
        },
    },
    # --- Français : raconter une histoire ---
    {
        "source": _source("FR_PE_003", "fr", "production_ecrite", "Prompt original — raconter un moment de la journée."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": "raconter_histoire",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Raconte en 2 ou 3 phrases ce qui se passe un matin d'école.",
                "model_answer": "Exemple : Je me réveille tôt. Je prends mon petit-déjeuner. Puis je pars à l'école avec mon cartable.",
            },
        },
    },
    # --- Français : rédaction courte ---
    {
        "source": _source("FR_PE_004", "fr", "production_ecrite", "Prompt original — rédaction courte."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": "redaction_courte",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
                "question": "Écris deux phrases sur ta journée à l'école.",
                "model_answer": "Exemple : Je suis allé(e) à l'école ce matin. J'ai appris les lettres avec ma maîtresse.",
            },
        },
    },
    {
        "source": _source("FR_PE_005", "fr", "production_ecrite", "Prompt original — rédaction courte."),
        "exercise": {
            "subject_code": "fr", "level_code": "1", "trimester": "T1",
            "domain_code": "production_ecrite", "skill_code": "redaction_courte",
            "exercise_format": "reponse_libre", "difficulty": "en_cours", "language": "fr",
            "grading_mode": "open",
            "content": {
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

        old = Exercise.query.filter(Exercise.source_id.isnot(None)).join(Source).filter(
            Source.url.like("local://expression_recitation_seed_v1%")
        ).all()
        if old:
            for exercise in old:
                run = exercise.generation_run
                source = exercise.source
                db.session.delete(exercise)
                db.session.flush()
                if run:
                    db.session.delete(run)
                if source:
                    db.session.delete(source)
            db.session.commit()
            print(f"Removed {len(old)} exercises from the retired oral-expression seed (v1).")

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
                prompt_template_version="v2-expression-seed",
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
