"""Builds a 15-exercise session from the local library cache. Never queries the
external library-service directly — only ever reads library_cache_exercise, which
server/sync/library_sync.py keeps up to date in the background. This keeps a
session fast and independent of the library-service's own load/availability.
"""

import random

from models import LibraryCacheExercise

SESSION_SIZE = 15


def build_session(level_code, subject_code, trimester=None, weak_skill_codes=None):
    """Selects up to SESSION_SIZE exercises, weighted toward the child's weak
    skills when known. Widens the search (drops the trimester filter, then
    ignores weak-skill weighting) when the cache doesn't have enough matching
    exercises yet — expected early on, before the crawler/generation pipeline
    (Phase 2) has produced real volume."""
    weak_skill_codes = set(weak_skill_codes or [])

    query = LibraryCacheExercise.query.filter_by(level_code=level_code, subject_code=subject_code)
    if trimester:
        query = query.filter_by(trimester=trimester)
    candidates = query.all()

    if len(candidates) < SESSION_SIZE and trimester:
        candidates = LibraryCacheExercise.query.filter_by(
            level_code=level_code, subject_code=subject_code
        ).all()

    weak = [c for c in candidates if c.skill_code in weak_skill_codes]
    other = [c for c in candidates if c.skill_code not in weak_skill_codes]
    random.shuffle(weak)
    random.shuffle(other)

    selection = (weak + other)[:SESSION_SIZE]
    random.shuffle(selection)
    return selection
