"""Stage 3: confirms a classified source's (level, subject) actually has
curriculum defined in the Main App before it's used for generation — keeps
the pipeline from generating exercises for a level/subject nobody has
authored a curriculum for yet."""

from db import db
from curriculum_client import fetch_curriculum_schema


def curriculum_match(sources):
    matched, rejected = [], []
    cache = {}
    for source in sources:
        key = (source.level_code, source.subject_code)
        if key not in cache:
            cache[key] = fetch_curriculum_schema(level=source.level_code, subject=source.subject_code)

        if not cache[key]:
            source.status = "rejected"
            rejected.append(source)
        else:
            source.status = "used_for_generation"
            matched.append(source)

    db.session.commit()
    return matched, rejected
