"""Stage 2: assigns a license_status. Real license detection from arbitrary
web pages is unreliable without a dedicated legal-metadata parser, so this
stays conservative on purpose: anything not explicitly and clearly marked as
open-licensed is 'unlicensed' — meaning it can only ever be used as
generation *inspiration*, never copied (see generation/generate_exercise.py
and models.py's generation_run_id NOT NULL constraint). This is the safe
default, not a gap to fix later."""

import re

from db import db

OPEN_LICENSE_MARKERS = [
    r"creative commons",
    r"cc[\s-]?by",
    r"domaine public",
    r"public domain",
    r"licence ouverte",
]


def classify_license(content_snapshot):
    text = (content_snapshot or "").lower()
    for pattern in OPEN_LICENSE_MARKERS:
        if re.search(pattern, text):
            return "explicit_open"
    return "unlicensed"


def classify(sources):
    for source in sources:
        source.license_status = classify_license(source.content_snapshot)
        source.status = "classified"
    db.session.commit()
    return sources
