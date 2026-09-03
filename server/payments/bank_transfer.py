"""The one payment provider that needs zero external account or API key --
just your own business bank account. No instant confirmation is possible
(no webhook), so this is a two-step flow: a parent requests a transfer and
gets a reference + your bank's RIB to complete it themselves, then an admin
manually matches the resulting bank statement line to that reference and
confirms it here, which is the only thing that actually grants access.

Bank RIB comes from an env var, not hardcoded, since it's real banking
information. BANK_TRANSFER_RIB / BANK_TRANSFER_BANK_NAME / BANK_TRANSFER_HOLDER
are unset by default -- request() still works (a real reference is created),
it just tells the caller the RIB isn't configured yet rather than lying.
"""

import os
import secrets
from datetime import datetime, timedelta

from db import db
from models import Entitlement, Payment

REFERENCE_PREFIX = "SP"


def _generate_reference():
    # short, human-typeable, unique enough for manual bank-statement
    # matching (not a security token) -- retried on the rare collision.
    for _ in range(10):
        candidate = f"{REFERENCE_PREFIX}-{secrets.token_hex(3).upper()}"
        if not Payment.query.filter_by(reference=candidate).first():
            return candidate
    raise RuntimeError("could not generate a unique payment reference")


def bank_details():
    """None for any field the admin hasn't configured yet -- the request
    endpoint still creates a real, trackable Payment row either way; it's
    the frontend's job to tell the parent "transfer details coming soon"
    if these are empty rather than pretending a fake RIB is real."""
    return {
        "bank_name": os.environ.get("BANK_TRANSFER_BANK_NAME"),
        "rib": os.environ.get("BANK_TRANSFER_RIB"),
        "account_holder": os.environ.get("BANK_TRANSFER_HOLDER"),
    }


def create_request(user_id, subject_code, level_code, billing_cycle="annual"):
    payment = Payment(
        user_id=user_id,
        subject_code=subject_code,
        level_code=level_code,
        billing_cycle=billing_cycle,
        provider="bank_transfer",
        status="pending_verification",
        reference=_generate_reference(),
    )
    db.session.add(payment)
    db.session.commit()
    return payment


def verify(payment, verified_by, amount_tnd=None):
    """The only function allowed to turn a pending bank transfer into real
    access -- grants or extends the matching Entitlement. Idempotent: a
    payment that's already confirmed is returned unchanged rather than
    stacking a second entitlement period on top."""
    if payment.status == "confirmed":
        return payment

    payment.status = "confirmed"
    payment.verified_by = verified_by
    payment.verified_at = datetime.utcnow()
    if amount_tnd is not None:
        payment.amount_tnd = amount_tnd

    entitlement = Entitlement.query.filter_by(
        user_id=payment.user_id, subject_code=payment.subject_code, level_code=payment.level_code
    ).first()
    expires_at = (
        datetime.utcnow() + timedelta(days=365) if payment.billing_cycle == "annual" else None
    )
    if entitlement is None:
        entitlement = Entitlement(
            user_id=payment.user_id,
            subject_code=payment.subject_code,
            level_code=payment.level_code,
            source="bank_transfer",
            expires_at=expires_at,
        )
        db.session.add(entitlement)
    else:
        # Renewal: extend from whichever is later (now, or the current
        # expiry if it hasn't lapsed yet) rather than always resetting from
        # today -- a parent renewing a week early shouldn't lose that week.
        base = entitlement.expires_at if (entitlement.expires_at and entitlement.expires_at > datetime.utcnow()) else datetime.utcnow()
        entitlement.expires_at = base + timedelta(days=365) if payment.billing_cycle == "annual" else None
        entitlement.source = "bank_transfer"

    db.session.commit()
    return payment
