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
from notifications.email import send_email

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

    # The check above is only a fast path -- it can't stop two /verify calls
    # that race each other (a double-click, or two admins on the same stale
    # pending list) from both reading status="pending_verification" before
    # either writes. If that happened with a plain attribute assignment,
    # both requests would fall through to the entitlement code below and a
    # renewal would stack two 365-day extensions on top of each other.
    # Guard against it with a single atomic UPDATE ... WHERE status=
    # 'pending_verification': the database, not this process, decides which
    # caller (if any) actually gets to flip the row, and the loser's rowcount
    # comes back 0 so it can just return the winner's already-committed result.
    update_values = {
        "status": "confirmed",
        "verified_by": verified_by,
        "verified_at": datetime.utcnow(),
    }
    if amount_tnd is not None:
        update_values["amount_tnd"] = amount_tnd

    claimed = (
        Payment.query.filter_by(id=payment.id, status="pending_verification")
        .update(update_values, synchronize_session=False)
    )
    if claimed == 0:
        db.session.commit()
        db.session.refresh(payment)
        return payment

    for key, value in update_values.items():
        setattr(payment, key, value)

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

    send_email(
        payment.user.email,
        "Confirmation de votre paiement SmartProf",
        "Votre paiement a bien été confirmé.\n\n"
        f"Référence : {payment.reference}\n"
        f"Matière : {payment.subject_code} — Niveau {payment.level_code}\n"
        f"Montant : {payment.amount_tnd} TND\n"
        f"Formule : {'Annuelle' if payment.billing_cycle == 'annual' else 'Ponctuelle'}\n\n"
        "L'accès est actif dès maintenant depuis votre espace parent.\n\n"
        "L'équipe SmartProf",
    )
    return payment
