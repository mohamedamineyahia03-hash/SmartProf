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
    cache. Safe to re-run: an already-cached exercise is just updated in place."""
    synced = 0
    cursor = 0

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
            row.content_fr = item["content_fr"]
            row.content_ar = item["content_ar"]
            row.license = item["license"]

        db.session.commit()
        synced += len(exercises)

        if not exercises or payload["next_cursor"] == cursor:
            break
        cursor = payload["next_cursor"]

    return synced


def main():
    with app.app_context():
        db.create_all()
        count = sync_once()
        print(f"Synced {count} exercises from library-service.")


if __name__ == "__main__":
    main()
