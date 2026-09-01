"""Minimal session-cookie auth — no external auth framework needed at this scale.
Password hashing uses werkzeug (already a Flask dependency, no new package)."""

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models import User

MIN_PASSWORD_LENGTH = 8


def register_user(email, password):
    email = (email or "").strip().lower()
    if "@" not in email or len(email) < 5:
        return None, "invalid_email"
    if not password or len(password) < MIN_PASSWORD_LENGTH:
        return None, "password_too_short"
    if User.query.filter_by(email=email).first() is not None:
        return None, "email_already_registered"

    user = User(email=email, password_hash=generate_password_hash(password))
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
