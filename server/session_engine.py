"""Builds a session one exercise at a time from the local library cache, adapting
difficulty as the child answers — never queries the external library-service
directly, only ever reads library_cache_exercise (kept fresh by
server/sync/library_sync.py), so a session stays fast and independent of the
library-service's own load/availability.

Difficulty moves in a "staircase": one step up after a correct answer, one step
down after an incorrect one — never more than one step at a time, and never
straight from a wrong answer into something harder. This mirrors how adaptive
practice tools (Khan Academy mastery challenges, DreamBox) pace difficulty,
rather than a purely increasing ramp that would keep pushing a struggling child
into harder material right when they need to consolidate.
"""

import random

from models import LibraryCacheExercise

SESSION_SIZE = 15
DIFFICULTY_ORDER = ["decouverte", "en_cours", "maitrise"]
STARTING_DIFFICULTY = "en_cours"


def _difficulty_index(value):
    try:
        return DIFFICULTY_ORDER.index(value)
    except ValueError:
        return DIFFICULTY_ORDER.index(STARTING_DIFFICULTY)


def next_difficulty(current_difficulty, was_correct):
    idx = _difficulty_index(current_difficulty)
    idx = min(idx + 1, len(DIFFICULTY_ORDER) - 1) if was_correct else max(idx - 1, 0)
    return DIFFICULTY_ORDER[idx]


def _closest_to_difficulty(candidates, target_difficulty):
    if not candidates:
        return []
    target_idx = _difficulty_index(target_difficulty)
    best_distance = min(abs(_difficulty_index(c.difficulty) - target_idx) for c in candidates)
    return [c for c in candidates if abs(_difficulty_index(c.difficulty) - target_idx) == best_distance]


def pick_next_exercise(level_code, subject_code, trimester, target_difficulty, excluded_ids=None, weak_skill_codes=None):
    """Picks one exercise closest to target_difficulty, excluding ones already
    used in this session. Widens from the current trimester to the whole
    subject/level when the cache is too thin — expected until the crawler/
    generation pipeline (Phase 2) has produced real volume. Returns None when
    truly nothing new is left, so the caller can end the session gracefully
    instead of repeating a question the child has already seen and answered."""
    excluded_ids = set(excluded_ids or [])
    weak_skill_codes = set(weak_skill_codes or [])

    candidates = [
        c
        for c in LibraryCacheExercise.query.filter_by(
            level_code=level_code, subject_code=subject_code, trimester=trimester
        ).all()
        if c.id not in excluded_ids
    ]

    if not candidates:
        candidates = [
            c
            for c in LibraryCacheExercise.query.filter_by(
                level_code=level_code, subject_code=subject_code
            ).all()
            if c.id not in excluded_ids
        ]

    if not candidates:
        return None

    closest = _closest_to_difficulty(candidates, target_difficulty)
    weak_matches = [c for c in closest if c.skill_code in weak_skill_codes]
    pool = weak_matches or closest
    return random.choice(pool)
