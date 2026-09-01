"""Entry point: python jobs/run_crawl.py <level_code> <subject_code>
Orchestrates discover -> classify -> curriculum_match -> generate -> validate
-> (auto-)publish for one (level, subject) combination, pulling sources only
from the curated allowlist and only generating for domains/skills that
actually exist in the Main App's curriculum.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # library-service/

from app import app  # noqa: E402
from db import db  # noqa: E402
from crawler.classify import classify  # noqa: E402
from crawler.curriculum_match import curriculum_match  # noqa: E402
from crawler.discover import discover  # noqa: E402
from crawler.source_allowlist import SOURCES  # noqa: E402
from curriculum_client import fetch_curriculum_schema  # noqa: E402
from generation.generate_exercise import generate_exercise  # noqa: E402
from generation.publish import try_auto_publish  # noqa: E402
from generation.validate import validate  # noqa: E402


def run(level_code, subject_code):
    entries = [s for s in SOURCES if s["level_code"] == level_code and s["subject_code"] == subject_code]
    if not entries:
        print(f"No allowlist sources for level={level_code} subject={subject_code} — add some to crawler/source_allowlist.py")
        return

    sources = discover(entries, trigger="manual")
    sources = classify(sources)
    matched, rejected = curriculum_match(sources)
    print(f"Discovered {len(sources)} source(s), matched {len(matched)}, rejected {len(rejected)}")

    if not matched:
        print("No usable sources — stopping.")
        return

    domains = fetch_curriculum_schema(level=level_code, subject=subject_code)
    if not domains:
        print("No curriculum defined for this level/subject yet — nothing to generate.")
        return

    generated = published = pending = rejected_count = 0
    source = matched[0]

    for domain in domains:
        for skill in domain["skills"]:
            formats = skill["exercise_formats"] or ["qcm"]
            for exercise_format in formats:
                _run, exercise = generate_exercise(source, level_code, subject_code, domain, skill, exercise_format)
                if exercise is None:
                    continue
                generated += 1

                issues = validate(exercise, source)
                if issues:
                    rejected_count += 1
                    print(f"  rejected {domain['domain']}/{skill['code']}/{exercise_format}: {issues}")
                    continue

                if try_auto_publish(exercise):
                    published += 1
                    print(f"  auto-published {domain['domain']}/{skill['code']}/{exercise_format} (id={exercise.id})")
                else:
                    pending += 1
                    print(f"  pending review {domain['domain']}/{skill['code']}/{exercise_format} (id={exercise.id})")

    print(f"\nDone: {generated} generated — {published} auto-published, {pending} pending review, {rejected_count} rejected.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("(ran in dry-run mode — set ANTHROPIC_API_KEY for real generation)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python jobs/run_crawl.py <level_code> <subject_code>")
        sys.exit(1)
    with app.app_context():
        db.create_all()
        run(sys.argv[1], sys.argv[2])
