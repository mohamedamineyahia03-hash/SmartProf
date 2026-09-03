"""Back up both SQLite databases (app + library-service) to timestamped copies.

No automatic scheduling is set up by this script — it only performs one backup
run when invoked. Wire it to your OS scheduler once real hosting exists:

  Windows (Task Scheduler), daily at 03:00:
    schtasks /create /tn "SmartProf DB backup" /tr "python C:\\path\\to\\server\\scripts\\backup_db.py" /sc daily /st 03:00

  Linux/macOS (cron), daily at 03:00:
    0 3 * * * /usr/bin/python3 /path/to/server/scripts/backup_db.py

On a managed host (Postgres in production, per the roadmap), replace the
SQLite file copy below with the provider's own backup/snapshot mechanism —
this script is meant for the current SQLite-based setup.
"""
import shutil
import sys
from datetime import datetime
from pathlib import Path

KEEP_LAST = 14  # ~2 weeks of daily backups

SERVER_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVER_DIR.parent
BACKUP_DIR = REPO_ROOT / "backups"

SOURCES = {
    "smartprof": SERVER_DIR / "smartprof.db",
    "library": REPO_ROOT / "library-service" / "library.db",
}


def backup_one(name: str, src: Path) -> Path | None:
    if not src.exists():
        print(f"skip {name}: {src} does not exist")
        return None
    dest_dir = BACKUP_DIR / name
    dest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = dest_dir / f"{name}-{stamp}.db"
    shutil.copy2(src, dest)
    print(f"backed up {name}: {dest}")

    existing = sorted(dest_dir.glob(f"{name}-*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in existing[KEEP_LAST:]:
        old.unlink()
        print(f"pruned old backup: {old}")

    return dest


def main() -> int:
    BACKUP_DIR.mkdir(exist_ok=True)
    any_done = False
    for name, src in SOURCES.items():
        if backup_one(name, src) is not None:
            any_done = True
    if not any_done:
        print("no database files found to back up", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
