"""Transactional email sending. Dry-run by default (SMTP_HOST unset): every
email that would be sent is written to server/logs/emails.log instead of
being lost, so the account-confirmation / password-reset / receipt flows are
fully testable before real SMTP credentials exist -- same pattern already
used for ANTHROPIC_API_KEY in library-service.

Configure via env vars to actually send mail:
  SMTP_HOST, SMTP_PORT (default 587), SMTP_USER, SMTP_PASSWORD,
  SMTP_FROM (default SMTP_USER)

Any real provider with SMTP credentials works (a transactional-email service
or a plain mailbox) -- this module doesn't assume a specific one.
"""
import logging
import os
import smtplib
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler

_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

_logger = logging.getLogger("smartprof.email")
if not _logger.handlers:
    _handler = RotatingFileHandler(
        os.path.join(_LOG_DIR, "emails.log"), maxBytes=2_000_000, backupCount=5, encoding="utf-8"
    )
    _handler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)


def send_email(to, subject, body_text):
    """Returns True if actually sent over SMTP, False if dry-run (logged only)."""
    host = os.environ.get("SMTP_HOST")
    if not host:
        _logger.info("DRY-RUN to=%s subject=%r\n%s\n%s", to, subject, body_text, "-" * 60)
        return False

    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    sender = os.environ.get("SMTP_FROM") or user

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.set_content(body_text)

    with smtplib.SMTP(host, port, timeout=10) as server:
        server.starttls()
        if user and password:
            server.login(user, password)
        server.send_message(msg)

    _logger.info("SENT to=%s subject=%r", to, subject)
    return True
