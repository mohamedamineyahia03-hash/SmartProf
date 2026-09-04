"""Pull job: syncs published exercises from the external library-service into the
Main App's local cache. Never called synchronously from a student-facing request —
run this on a schedule (cron / task scheduler) so session_engine (Phase 3) only
ever reads from the local library_cache_exercise table.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # server/

import requests  # noqa: E402

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import LibraryCacheExercise  # noqa: E402

LIBRARY_SERVICE_URL = os.environ.get("LIBRARY_SERVICE_URL", "http://127.0.0.1:5001")
LIBRARY_SERVICE_API_KEY = os.environ.get("LIBRARY_SERVICE_API_KEY", "dev-local-key")


def sync_once(limit=500):
    """Pulls every published exercise page by page and upserts into the local
    cache, then reconciles: any cached row NOT seen in this pass is deleted.

    That reconciliation step matters for a reason beyond "the source
    unpublished/deleted it" (the obvious case): library-service's `exercise`
    table is a plain SQLite INTEGER PRIMARY KEY, not AUTOINCREMENT, so a
    deleted row's id gets reused by a later, unrelated insert. Without
    deleting stale cache rows, a future sync would silently overwrite an
    orphaned cache row with new content that happens to share the recycled
    id, which is harmless -- but until that next sync runs, the cache can
    hold a row whose library_exercise_id no longer corresponds to anything
    real. Found and root-caused 2026-09-04 (a manual cache write during that
    session's Dictee guidee rollout collided with recycled ids from an
    earlier, already-deleted test batch). This function was previously
    add/update-only ("never deletes"), which is what let that class of bug
    exist at all -- fixed here rather than only patching the specific rows
    it caused."""
    synced = 0
    cursor = 0
    seen_ids = set()

    while True:
        response = requests.get(
            f"{LIBRARY_SERVICE_URL}/api/v1/exercises/export",
            params={"since": cursor, "limit": limit, "status": "published"},
            headers={"X-Api-Key": LIBRARY_SERVICE_API_KEY},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        exercises = payload["exercises"]

        for item in exercises:
            seen_ids.add(item["id"])
            row = LibraryCacheExercise.query.filter_by(library_exercise_id=item["id"]).first()
            if row is None:
                row = LibraryCacheExercise(library_exercise_id=item["id"])
                db.session.add(row)

            row.level_code = item["level"]
            row.subject_code = item["subject"]
            row.trimester = item["trimester"]
            row.domain_code = item["domain"]
            row.skill_code = item["skill"]
            row.exercise_format = item["format"]
            row.difficulty = item["difficulty"]
            row.language = item["language"]
            row.content = item["content"]
            row.grading_mode = item.get("grading_mode", "auto")
            row.license = item["license"]

        db.session.commit()
        synced += len(exercises)

        if not exercises or payload["next_cursor"] == cursor:
            break
        cursor = payload["next_cursor"]

    # Guard: an empty seen_ids with existing cache rows means something went
    # wrong upstream (wrong URL, auth issue returning an empty-but-200 body,
    # library-service genuinely down) rather than "everything was
    # unpublished at once" -- reconciling against an empty set in that case
    # would wipe the entire cache. Skip reconciliation rather than risk it;
    # a real mass-unpublish is vanishingly unlikely and can be handled by
    # hand if it's ever actually intended.
    stale = []
    if seen_ids or LibraryCacheExercise.query.first() is None:
        stale = LibraryCacheExercise.query.filter(
            LibraryCacheExercise.library_exercise_id.notin_(seen_ids)
        ).all()
        for row in stale:
            db.session.delete(row)
        if stale:
            db.session.commit()
    elif synced == 0:
        print("! sync returned 0 exercises but the cache is non-empty -- skipping stale-row cleanup as a safety guard")

    return synced, len(stale)


def main():
    with app.app_context():
        db.create_all()
        count, removed = sync_once()
        print(f"Synced {count} exercises from library-service, removed {removed} stale cache row(s).")


if __name__ == "__main__":
    main()
