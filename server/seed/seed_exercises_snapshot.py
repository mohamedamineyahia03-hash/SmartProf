"""Loads exercises_snapshot.json straight into library_cache_exercise, without
going through server/sync/library_sync.py (which needs a live library-service
to pull from). This is ONLY for a standalone deployment of the Main App by
itself (see the "just the main app, content baked in" testing-deployment
choice) — the real content pipeline is still library-service + sync; this
script exists so a deploy target that only runs server/ doesn't need a second
live service just to have exercises to serve.

The snapshot is a point-in-time export (exercises_snapshot.json, regenerate
with a one-off script reading LibraryCacheExercise if the local content
changes) — idempotent like every other seed script here, safe to run on
every boot.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # server/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import LibraryCacheExercise  # noqa: E402

SNAPSHOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exercises_snapshot.json")


def main():
    with app.app_context():
        db.create_all()

        if LibraryCacheExercise.query.first() is not None:
            print("Exercise cache already populated, skipping snapshot load.")
            return

        with open(SNAPSHOT_PATH, encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            db.session.add(LibraryCacheExercise(**item))

        db.session.commit()
        print(f"Loaded {len(items)} exercises from snapshot.")


if __name__ == "__main__":
    main()
