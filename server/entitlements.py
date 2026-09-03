"""Whether a user actually has access to a paid subject/level -- the piece
that was always missing behind is_subject_locked() in app.py (it used to
always return True for any non-free combination, since no Entitlement was
ever created by anything). Payments (bank_transfer.verify(), and later
Konnect/Flouci once integrated) are the only things that create/extend an
Entitlement; this module only ever reads them."""

from datetime import datetime

from models import Entitlement


def has_active_entitlement(user_id, subject_code, level_code):
    if user_id is None:
        return False
    entitlement = Entitlement.query.filter_by(
        user_id=user_id, subject_code=subject_code, level_code=level_code
    ).first()
    if entitlement is None:
        return False
    if entitlement.expires_at is None:
        return True  # one_time purchase, never expires
    # SQLite drops tzinfo on write, so expires_at comes back naive -- compare
    # against naive UTC too (datetime.now(timezone.utc) would raise
    # TypeError: can't compare offset-naive and offset-aware datetimes).
    return entitlement.expires_at > datetime.utcnow()
