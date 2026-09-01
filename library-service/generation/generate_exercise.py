"""Stage 4 — the ONLY place allowed to produce exercise content, and always
via generation_run -> exercise (models.py: exercise.generation_run_id is
NOT NULL, so no code path can store a source's text directly as an
exercise). Uses Claude when ANTHROPIC_API_KEY is set; otherwise runs in an
explicitly-labeled dry-run mode so the rest of the pipeline (validate,
review, publish, sync) stays fully testable without a live key. Dry-run
output always lands in review_status='pending_human_review' just like real
output, so it never slips through auto-publish.
"""

import json
import os

from db import db
from models import Exercise, GenerationRun

MODEL_NAME = "claude-opus-5"
PROMPT_TEMPLATE_VERSION = "v2"

PROMPT_TEMPLATE = """Tu es un pédagogue qui crée des exercices scolaires ORIGINAUX pour des élèves tunisiens du primaire.

Texte d'inspiration (ne JAMAIS le copier ni le paraphraser de près — il sert uniquement à comprendre le type de notion abordée) :
---
{inspiration}
---

Crée UN exercice original et différent du texte ci-dessus, pour :
- Niveau : {level}
- Matière : {subject}
- Domaine : {domain_name_fr} ({domain_name_ar})
- Compétence : {skill_name_fr}
- Format : {exercise_format}
- Difficulté : {difficulty}

Réponds STRICTEMENT avec ce JSON, rien d'autre, pas de texte avant/après :
{{"content_fr": {{"question": "...", "visual": "...", "choices": ["...","...","..."], "answer": "...", "explanation": "..."}}, "content_ar": {{"question": "...", "visual": "...", "choices": ["...","...","..."], "answer": "...", "explanation": "..."}}}}
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
- Domaine : {domain_name_fr} ({domain_name_ar})
- Compétence : {skill_name_fr}
- Difficulté : {difficulty}

Les 3 questions doivent porter sur des aspects différents du récit (ex: une information directe, un calcul à partir du récit, une comparaison ou un choix entre deux éléments du récit) — pas 3 fois la même chose reformulée.

Réponds STRICTEMENT avec ce JSON, rien d'autre, pas de texte avant/après :
{{"content_fr": {{"question": "<le récit>", "sub_questions": [{{"question": "...", "choices": ["...","..."], "answer": "...", "explanation": "..."}}, {{"question": "...", "answer": "...", "explanation": "..."}}, {{"question": "...", "answer": "...", "explanation": "..."}}]}}, "content_ar": {{"question": "<نفس القصة بالعربية>", "sub_questions": [...même structure en arabe...]}}}}
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
le champ "visual" est OBLIGATOIRE dans content_fr ET content_ar. Construis-le avec des emojis
(et "<br>" pour organiser une scène sur plusieurs lignes si besoin, par ex. pour montrer "dessus"/
"dessous") qui MONTRENT concrètement la situation — l'élève doit pouvoir regarder, observer, constater,
puis répondre. Ne décris jamais la scène seulement en texte dans "question" : "visual" doit la montrer."""


def _dry_run_output(skill, exercise_format):
    if exercise_format == "multi_questions":
        return {
            "content_fr": {
                "question": f"[Brouillon] Récit à générer pour la compétence « {skill['name_fr']} ».",
                "sub_questions": [
                    {
                        "question": "[Brouillon] Sous-question 1",
                        "answer": "?",
                        "explanation": "Contenu de test — remplacé dès qu'une clé ANTHROPIC_API_KEY est configurée.",
                    },
                    {
                        "question": "[Brouillon] Sous-question 2",
                        "answer": "?",
                        "explanation": "Contenu de test — remplacé dès qu'une clé ANTHROPIC_API_KEY est configurée.",
                    },
                    {
                        "question": "[Brouillon] Sous-question 3",
                        "answer": "?",
                        "explanation": "Contenu de test — remplacé dès qu'une clé ANTHROPIC_API_KEY est configurée.",
                    },
                ],
            },
            "content_ar": {
                "question": f"[مسودة] قصة يجب توليدها لمهارة « {skill['name_ar']} ».",
                "sub_questions": [
                    {"question": "[مسودة] سؤال 1", "answer": "؟", "explanation": "محتوى تجريبي."},
                    {"question": "[مسودة] سؤال 2", "answer": "؟", "explanation": "محتوى تجريبي."},
                    {"question": "[مسودة] سؤال 3", "answer": "؟", "explanation": "محتوى تجريبي."},
                ],
            },
        }
    return {
        "content_fr": {
            "question": f"[Brouillon] Exercice à générer pour la compétence « {skill['name_fr']} ».",
            "answer": "?",
            "explanation": "Contenu de test — remplacé par une vraie génération dès qu'une clé ANTHROPIC_API_KEY est configurée.",
        },
        "content_ar": {
            "question": f"[مسودة] تمرين يجب توليده لمهارة « {skill['name_ar']} ».",
            "answer": "؟",
            "explanation": "محتوى تجريبي — سيُستبدل بمحتوى حقيقي فور ضبط مفتاح ANTHROPIC_API_KEY.",
        },
    }


def _parse_json_response(raw_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_exercise(source, level_code, subject_code, domain, skill, exercise_format, difficulty="en_cours"):
    """Returns (GenerationRun, Exercise) — the Exercise is a 'draft' pending
    validate()/publish(), never published by this function itself."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    run = GenerationRun(
        source_id=source.id,
        model_provider="anthropic",
        model_name=MODEL_NAME if api_key else "dry-run",
        prompt_template_version=PROMPT_TEMPLATE_VERSION,
        status="success",
    )

    if api_key:
        import anthropic

        if exercise_format == "multi_questions":
            prompt = MULTI_QUESTIONS_PROMPT_TEMPLATE.format(
                inspiration=(source.content_snapshot or "")[:2000],
                level=level_code,
                subject=subject_code,
                domain_name_fr=domain["name_fr"],
                domain_name_ar=domain["name_ar"],
                skill_name_fr=skill["name_fr"],
                difficulty=difficulty,
            )
        else:
            visual_instruction = VISUAL_INSTRUCTION if skill["code"] in VISUAL_REQUIRED_SKILLS else ""
            prompt = PROMPT_TEMPLATE.format(
                inspiration=(source.content_snapshot or "")[:2000],
                level=level_code,
                subject=subject_code,
                domain_name_fr=domain["name_fr"],
                domain_name_ar=domain["name_ar"],
                skill_name_fr=skill["name_fr"],
                exercise_format=exercise_format,
                difficulty=difficulty,
                visual_instruction=visual_instruction,
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
            parsed = _dry_run_output(skill, exercise_format)
    else:
        parsed = _dry_run_output(skill, exercise_format)
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
        content_fr=parsed["content_fr"],
        content_ar=parsed["content_ar"],
        license="SmartProf",
        review_status="pending_human_review",
        status="draft",
        curriculum_schema_version="v1",
    )
    db.session.add(exercise)
    db.session.commit()
    return run, exercise
