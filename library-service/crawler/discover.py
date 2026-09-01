"""Stage 1: turns curated allowlist entries into `source` rows with a real
fetched text snapshot. No open web search yet — Phase 2 starts from a
hand-verified allowlist (source_allowlist.py); swapping in a search API
later only touches this file."""

import re

import requests

from db import db
from models import CrawlJob, Source

FETCH_TIMEOUT = 10
MAX_SNAPSHOT_CHARS = 4000
USER_AGENT = "SmartProfBot/0.1 (+educational content discovery, contact: smartprof project)"


def _strip_html(html):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;|&amp;|&quot;|&#\d+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:MAX_SNAPSHOT_CHARS]


def fetch_snapshot(url):
    try:
        response = requests.get(url, timeout=FETCH_TIMEOUT, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        return _strip_html(response.text)
    except requests.RequestException as exc:
        return f"(fetch failed: {exc})"


def discover(entries, trigger="manual"):
    """entries: allowlist dicts (see source_allowlist.py). Creates one
    `source` row per entry with status='pending_classification'."""
    job = CrawlJob(trigger=trigger, sources_found=len(entries))
    db.session.add(job)
    db.session.flush()

    created = []
    for entry in entries:
        snapshot = fetch_snapshot(entry["url"])
        source = Source(
            url=entry["url"],
            title=entry.get("title"),
            crawl_job_id=job.id,
            license_status="unlicensed",  # classify() refines this
            subject_code=entry["subject_code"],
            level_code=entry["level_code"],
            region_scope=entry["region_scope"],
            content_snapshot=snapshot,
            status="pending_classification",
        )
        db.session.add(source)
        created.append(source)

    job.sources_accepted = len(created)
    db.session.commit()
    return created
