"""Builds an exam-style session: a fixed, varied batch of exercises for one
curriculum section (domain), all at once — never queries the external
library-service directly, only ever reads library_cache_exercise (kept fresh
by server/sync/library_sync.py), so a session stays fast and independent of
the library-service's own load/availability.

There is no live difficulty adaptation here (that "staircase" mode was
removed along with the old auto-start flow — see the section-tree redesign,
2026-09-02): a real exam doesn't get easier because you missed a question.
Variety instead comes from spreading the batch across the section's distinct
skills (round-robin) and, within that, across formats and difficulty tiers,
so two sessions from the same section rarely look identical.
"""

import random
from collections import defaultdict

from models import LibraryCacheExercise

SESSION_SIZE = 15


def build_exam_session(level_code, subject_code, domain_code, size=SESSION_SIZE):
    """Returns up to `size` exercises from this exact section (domain),
    round-robining across its distinct skills for variety. Degrades
    gracefully when the section's pool is thin — expected until the
    crawler/generation pipeline (Phase 2) has produced real volume — by
    simply returning fewer exercises; an empty list only when the section
    has nothing published yet."""
    candidates = LibraryCacheExercise.query.filter_by(
        level_code=level_code, subject_code=subject_code, domain_code=domain_code
    ).all()
    if not candidates:
        return []

    by_skill = defaultdict(list)
    for c in candidates:
        by_skill[c.skill_code].append(c)
    for bucket in by_skill.values():
        random.shuffle(bucket)

    skill_codes = list(by_skill.keys())
    random.shuffle(skill_codes)

    picked = []
    idx = 0
    remaining = sum(len(bucket) for bucket in by_skill.values())
    while len(picked) < size and remaining > 0:
        skill_code = skill_codes[idx % len(skill_codes)]
        bucket = by_skill[skill_code]
        if bucket:
            picked.append(bucket.pop())
            remaining -= 1
        idx += 1

    random.shuffle(picked)
    return picked


def build_academy_session(subject_code, size=SESSION_SIZE):
    """"L'Academie du Francais" / "The English Academy" (added 2026-09-04):
    a paid bundle that re-serves the WHOLE niveau 1 + niveau 2 curriculum
    for one subject as a single session pool, relabelled "Niveau 1"/
    "Niveau 2" by the frontend (LibraryCacheExercise.level_code on each
    returned row is exactly what to label it by -- no separate academy
    content exists, this is intentionally the same rows a normal niveau 1/2
    session would use, never duplicated). Round-robins across
    (level_code, domain_code, skill_code) buckets so a batch mixes both
    levels and several domains rather than exhausting one first."""
    candidates = LibraryCacheExercise.query.filter(
        LibraryCacheExercise.subject_code == subject_code,
        LibraryCacheExercise.level_code.in_(["1", "2"]),
    ).all()
    if not candidates:
        return []

    by_bucket = defaultdict(list)
    for c in candidates:
        by_bucket[(c.level_code, c.domain_code, c.skill_code)].append(c)
    for bucket in by_bucket.values():
        random.shuffle(bucket)

    bucket_keys = list(by_bucket.keys())
    random.shuffle(bucket_keys)

    picked = []
    idx = 0
    remaining = sum(len(bucket) for bucket in by_bucket.values())
    while len(picked) < size and remaining > 0:
        key = bucket_keys[idx % len(bucket_keys)]
        bucket = by_bucket[key]
        if bucket:
            picked.append(bucket.pop())
            remaining -= 1
        idx += 1

    random.shuffle(picked)
    return picked
