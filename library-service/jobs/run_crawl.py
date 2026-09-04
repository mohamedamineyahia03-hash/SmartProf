"""Entry point: python jobs/run_crawl.py <level_code> <subject_code>
Orchestrates discover -> classify -> curriculum_match -> generate -> validate
-> automated review -> (auto-)publish for one (level, subject) combination,
pulling sources only from the curated allowlist and only generating for
domains/skills that actually exist in the Main App's curriculum.

No human review step (see generation/publish.py, 2026-09-04): a rejected
exercise gets regenerated in place, up to MAX_REGEN_ATTEMPTS times, before
being left as a permanent rejection.
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

MAX_REGEN_ATTEMPTS = 3


def generate_validate_publish(source, level_code, subject_code, domain, skill, exercise_format):
    """One skill/format slot, regenerated up to MAX_REGEN_ATTEMPTS times if
    validate() or the automated review rejects it. Returns
    (outcome, exercise) where outcome is "published" | "rejected" | "error"
    (generation itself failed, e.g. an API error) -- "error" stops retrying
    immediately since a broken API call won't fix itself on retry."""
    last_exercise = None
    for attempt in range(1, MAX_REGEN_ATTEMPTS + 1):
        _run, exercise = generate_exercise(source, level_code, subject_code, domain, skill, exercise_format)
        if exercise is None:
            return "error", last_exercise
        last_exercise = exercise

        issues = validate(exercise, source)
        if issues:
            print(f"    attempt {attempt}: rejected by validate() -- {issues}")
            continue

        published, reason = try_auto_publish(exercise, domain, skill)
        if published:
            return "published", exercise
        print(f"    attempt {attempt}: rejected by review -- {reason}")

    return "rejected", last_exercise


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

    generated = published = rejected_count = 0
    source = matched[0]

    for domain in domains:
        for skill in domain["skills"]:
            formats = skill["exercise_formats"] or ["qcm"]
            for exercise_format in formats:
                outcome, exercise = generate_validate_publish(source, level_code, subject_code, domain, skill, exercise_format)
                if exercise is not None:
                    generated += 1
                label = f"{domain['domain']}/{skill['code']}/{exercise_format}"
                if outcome == "published":
                    published += 1
                    print(f"  auto-published {label} (id={exercise.id})")
                elif outcome == "rejected":
                    rejected_count += 1
                    print(f"  permanently rejected {label} after {MAX_REGEN_ATTEMPTS} attempts (id={exercise.id if exercise else '?'})")
                else:
                    print(f"  generation error {label} -- skipped")

    print(f"\nDone: {generated} generated — {published} auto-published, {rejected_count} permanently rejected.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("(ran in dry-run mode — set ANTHROPIC_API_KEY for real generation)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python jobs/run_crawl.py <level_code> <subject_code>")
        sys.exit(1)
    with app.app_context():
        db.create_all()
        run(sys.argv[1], sys.argv[2])
