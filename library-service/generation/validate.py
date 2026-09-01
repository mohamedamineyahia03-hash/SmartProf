"""Stage 5: structural validation + a cheap anti-similarity guard against the
source text — the automated half of the originality/legal safety net (the
human review in publish.py is the other half)."""

import re

REQUIRED_KEYS = {"question", "answer"}
MAX_SOURCE_OVERLAP = 0.6  # share of the question's words also found in the source


def _tokenize(text):
    return set(re.findall(r"\w+", (text or "").lower()))


def _overlap_ratio(question, source_text):
    q_tokens = _tokenize(question)
    if not q_tokens:
        return 0.0
    return len(q_tokens & _tokenize(source_text)) / len(q_tokens)


def validate(exercise, source):
    """Mutates exercise.review_status/status on failure and returns the list
    of issues found (empty list = passed)."""
    issues = []

    for lang_key in ("content_fr", "content_ar"):
        content = getattr(exercise, lang_key) or {}
        missing = REQUIRED_KEYS - content.keys()
        if missing:
            issues.append(f"{lang_key} missing keys: {sorted(missing)}")
        if not str(content.get("question", "")).strip():
            issues.append(f"{lang_key} has an empty question")

    fr_question = (exercise.content_fr or {}).get("question", "")
    overlap = _overlap_ratio(fr_question, source.content_snapshot if source else "")
    if overlap > MAX_SOURCE_OVERLAP:
        issues.append(f"question too similar to source ({overlap:.0%} word overlap)")

    if issues:
        exercise.review_status = "rejected"
        exercise.status = "retired"

    return issues
