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
PROMPT_TEMPLATE_VERSION = "v1"

PROMPT_TEMPLATE = """Tu es un pédagogue qui crée des exercices scolaires ORIGINAUX pour des élèves tunisiens du primaire.

Texte d'inspiration (ne JAMAIS le copier ni le paraphraser de près — il sert uniquement à comprendre le type de notion abordée) :
---
{inspiration}
---

Attention : cette source d'inspiration peut dater d'une année scolaire antérieure ({source_year_note}). Ne reprends aucun élément qui pourrait être obsolète (dates, années scolaires, anciens repères de programme, anciens formats d'examen). Base le contenu final uniquement sur le niveau/domaine/compétence ci-dessous, tels que définis dans le programme tunisien actuel.

Crée UN exercice original et différent du texte ci-dessus, pour :
- Niveau : {level}
- Matière : {subject}
- Domaine : {domain_name_fr} ({domain_name_ar})
- Compétence : {skill_name_fr}
- Format : {exercise_format}
- Difficulté : {difficulty}

Réponds STRICTEMENT avec ce JSON, rien d'autre, pas de texte avant/après :
{{"content_fr": {{"question": "...", "choices": ["...","...","..."], "answer": "...", "explanation": "..."}}, "content_ar": {{"question": "...", "choices": ["...","...","..."], "answer": "...", "explanation": "..."}}}}
"choices" est optionnel : ne l'inclus que pour un format à choix (qcm/selection). "explanation" doit enseigner le raisonnement, pas seulement donner la réponse.
"""


def _dry_run_output(skill):
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

        source_year_note = (
            f"détectée autour de {source.source_year}" if source.source_year else "année non déterminée, à traiter avec prudence"
        )
        prompt = PROMPT_TEMPLATE.format(
            inspiration=(source.content_snapshot or "")[:2000],
            source_year_note=source_year_note,
            level=level_code,
            subject=subject_code,
            domain_name_fr=domain["name_fr"],
            domain_name_ar=domain["name_ar"],
            skill_name_fr=skill["name_fr"],
            exercise_format=exercise_format,
            difficulty=difficulty,
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
            parsed = _dry_run_output(skill)
    else:
        parsed = _dry_run_output(skill)
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
