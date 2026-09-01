"""Client for the Main App's curriculum-schema endpoint. The Library Service treats
curriculum taxonomy as owned by the Main App (business/pedagogical truth) and only
ever reads it — used by the Phase 2 crawler to know which domains/skills/formats to
source and generate exercises for."""

import os

import requests

MAIN_APP_URL = os.environ.get("MAIN_APP_URL", "http://127.0.0.1:5000")


def fetch_curriculum_schema(level=None, subject=None, timeout=10):
    params = {}
    if level:
        params["level"] = level
    if subject:
        params["subject"] = subject

    response = requests.get(f"{MAIN_APP_URL}/api/v1/curriculum-schema", params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()
