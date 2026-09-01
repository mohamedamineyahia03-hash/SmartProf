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

    content = exercise.content or {}
    if not str(content.get("question", "")).strip():
        issues.append("content has an empty question")

    sub_questions = content.get("sub_questions")
    if sub_questions is not None:
        # "récit à plusieurs questions" (multi_questions format): no
        # top-level answer, each sub-question carries its own instead.
        if not isinstance(sub_questions, list) or len(sub_questions) < 2:
            issues.append("content sub_questions must be a list of at least 2 items")
        else:
            for i, sub in enumerate(sub_questions):
                missing = REQUIRED_KEYS - sub.keys()
                if missing:
                    issues.append(f"content sub_questions[{i}] missing keys: {sorted(missing)}")
                if not str(sub.get("question", "")).strip():
                    issues.append(f"content sub_questions[{i}] has an empty question")
    else:
        missing = REQUIRED_KEYS - content.keys()
        if missing:
            issues.append(f"content missing keys: {sorted(missing)}")

    overlap = _overlap_ratio(content.get("question", ""), source.content_snapshot if source else "")
    if overlap > MAX_SOURCE_OVERLAP:
        issues.append(f"question too similar to source ({overlap:.0%} word overlap)")

    if issues:
        exercise.review_status = "rejected"
        exercise.status = "retired"

    return issues
