"""Minimal session-cookie auth — no external auth framework needed at this scale.
Password hashing uses werkzeug (already a Flask dependency, no new package)."""

import hashlib
import secrets
import string
from datetime import datetime, timedelta

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models import PasswordResetToken, User

MIN_PASSWORD_LENGTH = 8
REFERRAL_CODE_ALPHABET = string.ascii_uppercase + string.digits
REFERRAL_CODE_LENGTH = 6
RESET_TOKEN_TTL_MINUTES = 60


def _generate_referral_code():
    while True:
        code = "".join(secrets.choice(REFERRAL_CODE_ALPHABET) for _ in range(REFERRAL_CODE_LENGTH))
        if User.query.filter_by(referral_code=code).first() is None:
            return code


def register_user(email, password, referred_by_code=None):
    email = (email or "").strip().lower()
    if "@" not in email or len(email) < 5:
        return None, "invalid_email"
    if not password or len(password) < MIN_PASSWORD_LENGTH:
        return None, "password_too_short"
    if User.query.filter_by(email=email).first() is not None:
        return None, "email_already_registered"

    referrer = None
    if referred_by_code:
        referrer = User.query.filter_by(referral_code=referred_by_code.strip().upper()).first()

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        referral_code=_generate_referral_code(),
        referred_by_user_id=referrer.id if referrer else None,
    )
    db.session.add(user)
    db.session.commit()
    return user, None


def authenticate(email, password):
    email = (email or "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password_hash, password or ""):
        return None
    return user


def login_user(user):
    session["user_id"] = user.id


def logout_user():
    session.pop("user_id", None)


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return User.query.get(user_id)


def _hash_reset_token(raw_token):
    return hashlib.sha256(raw_token.encode()).hexdigest()


def create_password_reset_token(email):
    """Returns the raw token to email, or None if no account matches --
    the caller must respond identically either way so a "forgot password"
    request can't be used to probe which emails are registered."""
    email = (email or "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user is None:
        return None, None

    raw_token = secrets.token_urlsafe(32)
    reset = PasswordResetToken(
        user_id=user.id,
        token_hash=_hash_reset_token(raw_token),
        expires_at=datetime.utcnow() + timedelta(minutes=RESET_TOKEN_TTL_MINUTES),
    )
    db.session.add(reset)
    db.session.commit()
    return user, raw_token


def reset_password(raw_token, new_password):
    if not new_password or len(new_password) < MIN_PASSWORD_LENGTH:
        return None, "password_too_short"

    reset = PasswordResetToken.query.filter_by(
        token_hash=_hash_reset_token(raw_token or ""), used_at=None
    ).first()
    if reset is None or reset.expires_at < datetime.utcnow():
        return None, "invalid_or_expired_token"

    user = User.query.get(reset.user_id)
    user.password_hash = generate_password_hash(new_password)
    reset.used_at = datetime.utcnow()
    db.session.commit()
    return user, None
