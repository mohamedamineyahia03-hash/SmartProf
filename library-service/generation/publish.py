"""Stage 6-7 — the review policy + the single function allowed to move an
exercise to 'published'. Policy (validated with the user): the first
AUTO_TRUST_THRESHOLD published exercises in each (level, subject, domain)
bucket need a human's explicit approval (api/admin.py); once a bucket has
that many published, newly generated exercises in the same bucket that pass
validate() publish automatically."""

from datetime import datetime, timezone

from db import db
from models import Exercise

AUTO_TRUST_THRESHOLD = 3


def published_count(level_code, subject_code, domain_code):
    return Exercise.query.filter_by(
        level_code=level_code, subject_code=subject_code, domain_code=domain_code, status="published"
    ).count()


def is_bucket_trusted(exercise):
    return published_count(exercise.level_code, exercise.subject_code, exercise.domain_code) >= AUTO_TRUST_THRESHOLD


def try_auto_publish(exercise):
    """Call right after validate() passes. Publishes immediately if this
    exercise's bucket already has enough human-approved history; otherwise
    leaves it as draft/pending_human_review for api/admin.py to act on."""
    if exercise.review_status == "rejected":
        return False
    if not is_bucket_trusted(exercise):
        return False

    exercise.review_status = "auto_passed_schema"
    exercise.status = "published"
    db.session.commit()
    return True


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
    exercise in the bucket is then auto-published, exactly like
    try_auto_publish() would do for newly generated content once the
    bucket is trusted -- this is the retroactive equivalent for content
    that was bulk-imported and never went through the generation
    pipeline's own validate()/try_auto_publish() call."""
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
