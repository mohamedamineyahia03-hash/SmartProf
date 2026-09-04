"""Stage 5b -- automated coherence review, replacing human review entirely
(the user has no time for manual approval, decided 2026-09-04). Runs right
after validate() passes, before an exercise is allowed to publish.

validate() only checks structure (required JSON keys, answer-in-choices,
anti-plagiarism overlap with the source). It cannot catch the defects found
by hand in the same-day T1 audit: content that doesn't actually match its
declared domain (e.g. a "fractions" exercise with no fraction in it), a
grammatically broken sentence, a wrong answer, or an explanation that's
empty/non-explanatory. review_exercise() asks a second, independent model
call (Opus 5 by default -- a different, stronger model than the one that
generated the exercise, so it isn't just asking the writer to grade its own
work) to judge exactly those things.

A rejected exercise is not corrected here (no code path may edit generated
content directly -- same rule as everywhere else in this pipeline); the
caller is expected to discard it and generate a fresh one.
"""

import json
import os

REVIEW_MODEL = os.environ.get("REVIEW_MODEL", "claude-opus-5")

REVIEW_PROMPT_TEMPLATE = """Tu es relecteur pedagogique strict. Verifie cet exercice scolaire genere pour un eleve tunisien du primaire -- ne le corrige jamais, juge-le seulement.

Exercice a verifier :
- Niveau : {level}
- Matiere : {subject}
- Domaine : {domain_name} ({domain_name_alt})
- Competence : {skill_name}
- Contenu JSON : {content_json}

Verifie ces points, dans l'ordre, et rejette (pass=false) des le premier defaut trouve :
1. Le contenu porte-t-il vraiment sur le domaine et la competence indiques -- pas un sujet generique ou hors-sujet (ex: une question d'addition presentee comme un exercice de "fractions") ?
2. La question est-elle grammaticalement correcte et sensee dans sa langue (pas de phrase incoherente, pas d'erreur d'accord) ?
3. La reponse est-elle correcte ? Si c'est un calcul, refais-le toi-meme.
4. Si "choices" existe : la reponse est-elle bien parmi les choix, sans doublon, sans distracteur absurde ?
5. L'explication ("explanation") enseigne-t-elle vraiment le raisonnement -- pas vide, pas une simple repetition de la reponse ?

Reponds STRICTEMENT avec ce JSON, rien d'autre, pas de texte avant/apres :
{{"pass": true, "reason": ""}}
"reason" reste vide si pass=true ; si pass=false, une phrase precise disant EXACTEMENT quel point (1 a 5) echoue et pourquoi.
"""


def _parse_json_response(raw_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def review_exercise(exercise, domain, skill):
    """Returns (passed: bool, reason: str).

    Dry-run mode (no ANTHROPIC_API_KEY): always passes, consistent with
    generate_exercise.py's dry-run convention -- draft content in dry-run is
    an intentional placeholder, not something the review should ever flag.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return True, "(dry-run: review skipped, no ANTHROPIC_API_KEY)"

    import anthropic

    prompt = REVIEW_PROMPT_TEMPLATE.format(
        level=exercise.level_code,
        subject=exercise.subject_code,
        domain_name=domain["name_fr"],
        domain_name_alt=domain["name_ar"],
        skill_name=skill["name_fr"],
        content_json=json.dumps(exercise.content, ensure_ascii=False),
    )
    client = anthropic.Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model=REVIEW_MODEL,
            max_tokens=512,
            output_config={"effort": "medium"},
            messages=[{"role": "user", "content": prompt}],
        )
        raw_text = next((b.text for b in message.content if b.type == "text"), "")
        parsed = _parse_json_response(raw_text)
        return bool(parsed.get("pass")), str(parsed.get("reason") or "")
    except Exception as exc:
        # A review-call failure (network error, malformed JSON, API error...)
        # must never silently pass an exercise through -- with no human
        # reviewer left in this pipeline, this call IS the only quality
        # gate. Treat any failure to get a clean verdict as a rejection.
        return False, f"review call failed: {exc}"
