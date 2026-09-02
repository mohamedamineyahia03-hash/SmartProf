"""Minimal session-cookie auth — no external auth framework needed at this scale.
Password hashing uses werkzeug (already a Flask dependency, no new package)."""

import secrets
import string

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models import User

MIN_PASSWORD_LENGTH = 8
REFERRAL_CODE_ALPHABET = string.ascii_uppercase + string.digits
REFERRAL_CODE_LENGTH = 6


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
