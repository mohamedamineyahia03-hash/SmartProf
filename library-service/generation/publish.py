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
