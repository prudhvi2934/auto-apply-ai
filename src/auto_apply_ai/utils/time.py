from __future__ import annotations
from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0)

def parse_captured_at(value: str | None) -> datetime:
    if not value:
        return now_utc()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)