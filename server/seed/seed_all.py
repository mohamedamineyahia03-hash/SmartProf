"""Runs every seed step needed for a standalone deployment of the Main App
(curriculum + the baked-in exercise snapshot) in one call — the deploy start
command runs this before gunicorn boots. Every step it calls is already
idempotent (checks for existing rows before inserting), so this is safe to
run on every restart, not just the first one.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # server/seed/

import seed_curriculum  # noqa: E402
import seed_exercises_snapshot  # noqa: E402

if __name__ == "__main__":
    seed_curriculum.main()
    seed_exercises_snapshot.main()
