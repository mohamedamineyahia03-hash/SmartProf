"""Stage 4 — the ONLY place allowed to produce exercise content, and always
via generation_run -> exercise (models.py: exercise.generation_run_id is
NOT NULL, so no code path can store a source's text directly as an
exercise). Uses Claude when ANTHROPIC_API_KEY is set; otherwise runs in an
explicitly-labeled dry-run mode so the rest of the pipeline (validate,
review, publish, sync) stays fully testable without a live key. Dry-run
output always lands in review_status='pending_human_review' just like real
output, so it never slips through auto-publish.

Content is single-language, never bilingual — SmartProf's interface is
Arabic-only (no language switcher) and no subject is translated into
French: Math/Éveil scientifique/Arabe are written in Arabic, Français
stays entirely in French, Anglais stays entirely in English. See
LANGUAGE_BY_SUBJECT.
"""

import json
import os

from db import db
from models import Exercise, GenerationRun

MODEL_NAME = "claude-opus-5"
PROMPT_TEMPLATE_VERSION = "v3"

# The one place that decides which language an exercise's content is
# written in. Never inferred from a UI toggle (there isn't one) — fixed per
# subject, matching the validated policy: only actual language-learning
# subjects carry non-Arabic content, and even then only in their own
# target language, never mixed with Arabic instructions.
LANGUAGE_BY_SUBJECT = {
    "math": "ar",
    "science": "ar",
    "ar": "ar",
    "fr": "fr",
    "en": "en",
}

LANGUAGE_NAMES = {
    "ar": "arabe",
    "fr": "français",
    "en": "anglais",
}

PROMPT_TEMPLATE = """Tu es un pédagogue qui crée des exercices scolaires ORIGINAUX pour des élèves tunisiens du primaire.

Texte d'inspiration (ne JAMAIS le copier ni le paraphraser de près — il sert uniquement à comprendre le type de notion abordée) :
---
{inspiration}
---

Crée UN exercice original et différent du texte ci-dessus, pour :
- Niveau : {level}
- Matière : {subject}
- Domaine : {domain_name} ({domain_name_alt})
- Compétence : {skill_name}
- Format : {exercise_format}
- Difficulté : {difficulty}

IMPORTANT : rédige tout le contenu (question, choix, réponse, explication) ENTIÈREMENT en {language_name}. N'utilise aucune autre langue, pas même pour une consigne ou un mot isolé.

Réponds STRICTEMENT avec ce JSON, rien d'autre, pas de texte avant/après :
{{"content": {{"question": "...", "visual": "...", "choices": ["...","...","..."], "answer": "...", "explanation": "..."}}}}
"choices" est optionnel : ne l'inclus que pour un format à choix (qcm/selection). "visual" est optionnel (voir consigne ci-dessous s'il est obligatoire pour cette compétence). "explanation" doit enseigner le raisonnement, pas seulement donner la réponse.{visual_instruction}
"""

# Format "multi_questions" (compétence problemes/recit_multi_questions) : un
# récit unique, plusieurs questions liées, chacune avec sa propre réponse et
# son explication — un JSON différent de tous les autres formats, donc un
# template dédié plutôt qu'une variante du principal.
MULTI_QUESTIONS_PROMPT_TEMPLATE = """Tu es un pédagogue qui crée des exercices scolaires ORIGINAUX pour des élèves tunisiens du primaire.

Texte d'inspiration (ne JAMAIS le copier ni le paraphraser de près — il sert uniquement à comprendre le type de notion abordée) :
---
{inspiration}
---

Crée UN récit original (2-3 phrases, différent du texte ci-dessus) suivi de 3 questions liées à ce récit, pour :
- Niveau : {level}
- Matière : {subject}
- Domaine : {domain_name} ({domain_name_alt})
- Compétence : {skill_name}
- Difficulté : {difficulty}

Les 3 questions doivent porter sur des aspects différents du récit (ex: une information directe, un calcul à partir du récit, une comparaison ou un choix entre deux éléments du récit) — pas 3 fois la même chose reformulée.

IMPORTANT : rédige tout le contenu (récit, questions, choix, réponses, explications) ENTIÈREMENT en {language_name}. N'utilise aucune autre langue, pas même pour une consigne ou un mot isolé.

Réponds STRICTEMENT avec ce JSON, rien d'autre, pas de texte avant/après :
{{"content": {{"question": "<le récit>", "sub_questions": [{{"question": "...", "choices": ["...","..."], "answer": "...", "explanation": "..."}}, {{"question": "...", "answer": "...", "explanation": "..."}}, {{"question": "...", "answer": "...", "explanation": "..."}}]}}}}
"choices" dans une sous-question est optionnel (uniquement si cette sous-question précise est à choix). Chaque sous-question a sa propre "explanation" qui enseigne le raisonnement, pas seulement la réponse.
"""

# Skills where a purely textual question forces the child to imagine the
# scene instead of observing it — counting, spatial position, and size/length
# comparison. VISUAL_INSTRUCTION makes "visual" mandatory (not just an
# option) for these, so the child looks, observes, and answers instead of
# reading an abstract description.
VISUAL_REQUIRED_SKILLS = {
    "denombrement",
    "reconnaissance_quantite",
    "ordre_nombres",
    "formes",
    "positions",
    "gauche_droite",
    "haut_bas",
    "dessus_dessous",
    "dedans_dehors",
    "devant_derriere",
    "pres_loin",
    "entre",
    "comparaison_longueurs",
    "rangement_longueurs",
    "comparaison_masses",
    "reconnaissance_monnaie",
    "dizaine_unites",
}

VISUAL_INSTRUCTION = """

Cette compétence porte sur le dénombrement, le repérage spatial ou la comparaison de grandeurs :
le champ "visual" est OBLIGATOIRE. Construis-le avec des emojis (et "<br>" pour organiser une
scène sur plusieurs lignes si besoin, par ex. pour montrer "dessus"/"dessous") qui MONTRENT
concrètement la situation — l'élève doit pouvoir regarder, observer, constater, puis répondre.
Ne décris jamais la scène seulement en texte dans "question" : "visual" doit la montrer."""

_DRY_RUN_LABEL = {
    "ar": {
        "draft_exercise": lambda skill: f"[مسودة] تمرين يجب توليده لمهارة « {skill['name_ar']} ».",
        "draft_story": lambda skill: f"[مسودة] قصة يجب توليدها لمهارة « {skill['name_ar']} ».",
        "sub_q": lambda i: f"[مسودة] سؤال {i}",
        "answer": "؟",
        "explanation": "محتوى تجريبي — سيُستبدل بمحتوى حقيقي فور ضبط مفتاح ANTHROPIC_API_KEY.",
    },
    "fr": {
        "draft_exercise": lambda skill: f"[Brouillon] Exercice à générer pour la compétence « {skill['name_fr']} ».",
        "draft_story": lambda skill: f"[Brouillon] Récit à générer pour la compétence « {skill['name_fr']} ».",
        "sub_q": lambda i: f"[Brouillon] Sous-question {i}",
        "answer": "?",
        "explanation": "Contenu de test — remplacé par une vraie génération dès qu'une clé ANTHROPIC_API_KEY est configurée.",
    },
    "en": {
        "draft_exercise": lambda skill: f"[Draft] Exercise to generate for skill « {skill['name_fr']} ».",
        "draft_story": lambda skill: f"[Draft] Story to generate for skill « {skill['name_fr']} ».",
        "sub_q": lambda i: f"[Draft] Sub-question {i}",
        "answer": "?",
        "explanation": "Test content — replaced by real generation once ANTHROPIC_API_KEY is set.",
    },
}


def _dry_run_output(skill, exercise_format, language):
    labels = _DRY_RUN_LABEL[language]
    if exercise_format == "multi_questions":
        return {
            "content": {
                "question": labels["draft_story"](skill),
                "sub_questions": [
                    {"question": labels["sub_q"](i), "answer": labels["answer"], "explanation": labels["explanation"]}
                    for i in (1, 2, 3)
                ],
            },
        }
    return {
        "content": {
            "question": labels["draft_exercise"](skill),
            "answer": labels["answer"],
            "explanation": labels["explanation"],
        },
    }


def _parse_json_response(raw_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_exercise(
    source, level_code, subject_code, domain, skill, exercise_format, difficulty="en_cours", grading_mode="auto"
):
    """Returns (GenerationRun, Exercise) — the Exercise is a 'draft' pending
    validate()/publish(), never published by this function itself."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    language = LANGUAGE_BY_SUBJECT[subject_code]
    language_name = LANGUAGE_NAMES[language]

    run = GenerationRun(
        source_id=source.id,
        model_provider="anthropic",
        model_name=MODEL_NAME if api_key else "dry-run",
        prompt_template_version=PROMPT_TEMPLATE_VERSION,
        status="success",
    )

    if api_key:
        import anthropic

        # Domain/skill metadata (curriculum labels) is only ever authored in
        # French/Arabic — used here purely to brief the model on what to
        # write about, never as content itself, so it's fine to describe an
        # English-subject exercise using its French/Arabic domain label.
        if exercise_format == "multi_questions":
            prompt = MULTI_QUESTIONS_PROMPT_TEMPLATE.format(
                inspiration=(source.content_snapshot or "")[:2000],
                level=level_code,
                subject=subject_code,
                domain_name=domain["name_fr"],
                domain_name_alt=domain["name_ar"],
                skill_name=skill["name_fr"],
                difficulty=difficulty,
                language_name=language_name,
            )
        else:
            visual_instruction = VISUAL_INSTRUCTION if skill["code"] in VISUAL_REQUIRED_SKILLS else ""
            prompt = PROMPT_TEMPLATE.format(
                inspiration=(source.content_snapshot or "")[:2000],
                level=level_code,
                subject=subject_code,
                domain_name=domain["name_fr"],
                domain_name_alt=domain["name_ar"],
                skill_name=skill["name_fr"],
                exercise_format=exercise_format,
                difficulty=difficulty,
                visual_instruction=visual_instruction,
                language_name=language_name,
            )
        client = anthropic.Anthropic(api_key=api_key)
        try:
            message = client.messages.create(
                model=MODEL_NAME,
                max_tokens=2048,
                output_config={"effort": "medium"},
                messages=[{"role": "user", "content": prompt}],
            )
            raw_text = next((b.text for b in message.content if b.type == "text"), "")
            run.raw_model_output = raw_text
            parsed = _parse_json_response(raw_text)
        except anthropic.APIError as exc:
            run.status = "failed"
            run.raw_model_output = str(exc)
            db.session.add(run)
            db.session.commit()
            return run, None
        except (json.JSONDecodeError, IndexError):
            run.status = "flagged_for_review"
            parsed = _dry_run_output(skill, exercise_format, language)
    else:
        parsed = _dry_run_output(skill, exercise_format, language)
        run.raw_model_output = json.dumps(parsed, ensure_ascii=False)

    db.session.add(run)
    db.session.flush()

    exercise = Exercise(
        generation_run_id=run.id,
        source_id=source.id,
        subject_code=subject_code,
        level_code=level_code,
        trimester=source.trimester_hint or "T1",
        domain_code=domain["domain"],
        skill_code=skill["code"],
        exercise_format=exercise_format,
        difficulty=difficulty,
        language=language,
        content=parsed["content"],
        grading_mode=grading_mode,
        license="SmartProf",
        review_status="pending_human_review",
        status="draft",
        curriculum_schema_version="v1",
    )
    db.session.add(exercise)
    db.session.commit()
    return run, exercise
