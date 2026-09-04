"""Stage 6-7 -- the functions allowed to move an exercise to 'published'.

Two paths exist:

1. try_auto_publish() -- the pipeline-time gate used by jobs/run_crawl.py
   and jobs/run_batch_from_besoin.py right after validate() passes. Policy
   changed 2026-09-04: the user has no time for manual review, so this now
   runs an automated Opus-5 coherence review (generation/review.py) instead
   of the original "first 3 per bucket need a human" trust threshold --
   there is no human gate left in the generation pipeline itself. A
   rejected exercise is marked review_status="rejected" and never
   published; the caller regenerates a fresh one instead of editing it in
   place.

2. approve() / reject() / bucket_sample() / bulk_approve_bucket() /
   bulk_reject_bucket() -- the manual admin API (library-service/app.py,
   /api/admin/...) kept for retroactive use: inspecting or bulk-clearing
   already-generated draft content (e.g. bulk-imported batches that never
   went through try_auto_publish() at all) without a human being required
   to touch every new generation going forward.
"""

from datetime import datetime, timezone

from db import db
from generation.review import review_exercise
from models import Exercise


def try_auto_publish(exercise, domain, skill):
    """Call right after validate() passes. Runs the automated coherence
    review and publishes only if it passes. Always returns (published: bool,
    reason: str) -- reason is empty on success, the review's rejection
    reason otherwise -- so the caller can log why and regenerate."""
    if exercise.review_status == "rejected":
        return False, "already rejected"

    passed, reason = review_exercise(exercise, domain, skill)
    if not passed:
        exercise.review_status = "rejected"
        db.session.commit()
        return False, reason

    exercise.review_status = "auto_passed_schema"
    exercise.status = "published"
    db.session.commit()
    return True, reason


def approve(exercise, reviewed_by="admin"):
    exercise.review_status = "approved"
    exercise.status = "published"
    exercise.reviewed_by = reviewed_by
    exercise.reviewed_at = datetime.now(timezone.utc)
    db.session.commit()
    return exercise


def reject(exercise, reviewed_by="admin"):
    exercise.review_status = "rejected"
    exercise.status = "retired"
    exercise.reviewed_by = reviewed_by
    exercise.reviewed_at = datetime.now(timezone.utc)
    db.session.commit()
    return exercise


def bucket_sample(level_code, subject_code, domain_code, sample_size=3):
    """The exercises a human should actually look at before approving a
    bucket -- the oldest ones (lowest id), same selection order approve/
    bulk_approve_bucket use, so what's shown is exactly what gets marked
    human-reviewed."""
    return (
        Exercise.query.filter_by(
            level_code=level_code, subject_code=subject_code, domain_code=domain_code, status="draft"
        )
        .order_by(Exercise.id)
        .limit(sample_size)
        .all()
    )


def bulk_approve_bucket(level_code, subject_code, domain_code, reviewed_by="admin", sample_size=3):
    """Applies the review policy documented at the top of this file to an
    entire (level, subject, domain) bucket at once: the first `sample_size`
    exercises (oldest first) are approved individually, as a real human
    review record (reviewed_by/reviewed_at) -- these must be the same ones
    a reviewer was actually shown (see bucket_sample). Every other draft
    exercise in the bucket is then auto-published -- this is the
    retroactive equivalent for content that was bulk-imported and never
    went through the generation pipeline's own validate()/try_auto_publish()
    call."""
    sample = bucket_sample(level_code, subject_code, domain_code, sample_size)
    for exercise in sample:
        approve(exercise, reviewed_by=reviewed_by)

    remaining = Exercise.query.filter_by(
        level_code=level_code, subject_code=subject_code, domain_code=domain_code, status="draft"
    ).all()
    for exercise in remaining:
        exercise.review_status = "auto_passed_schema"
        exercise.status = "published"
    db.session.commit()

    return {"approved_by_review": len(sample), "auto_published": len(remaining), "total": len(sample) + len(remaining)}


def bulk_reject_bucket(level_code, subject_code, domain_code, reviewed_by="admin"):
    """Rejects every remaining draft exercise in a bucket -- for when the
    sample shown to the reviewer was bad enough that nothing in the bucket
    should be trusted."""
    rows = Exercise.query.filter_by(
        level_code=level_code, subject_code=subject_code, domain_code=domain_code, status="draft"
    ).all()
    for exercise in rows:
        reject(exercise, reviewed_by=reviewed_by)
    return {"rejected": len(rows)}
