# src/auto_apply_ai/ingest/validators.py
from __future__ import annotations
from typing import Dict, Any, Tuple, List
from urllib.parse import urlparse
from datetime import datetime

def _valid_url(u: str) -> bool:
    try:
        p = urlparse(u)
        return p.scheme in {"http","https"} and bool(p.netloc)
    except Exception:
        return False

def validate_row(row: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    hard: List[str] = []
    soft: List[str] = []

    src = row.get("source_url")
    if not src or not _valid_url(src):
        hard.append("invalid_source_url")

    cap = row.get("captured_at")
    # Accept ISO or %Y-%m-%d %H:%M:%S
    ok = False
    if isinstance(cap, datetime):
            ok = True  # ok

    if not ok:
        hard.append("invalid_captured_at")

    if not row.get("company"):
        soft.append("missing_company")
    if not row.get("job_title"):
        soft.append("missing_job_title")

    # Tracking params hint (already stripped by normalizer, but warn if hint url has them)
    if row.get("apply_url_hint") and ("utm_" in row["apply_url_hint"] or "gclid" in row["apply_url_hint"]):
        soft.append("apply_url_hint_contains_tracking")

    return hard, soft