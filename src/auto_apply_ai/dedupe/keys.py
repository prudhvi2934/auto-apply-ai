# src/auto_apply_ai/dedupe/keys.py
from __future__ import annotations
from hashlib import sha1
from urllib.parse import urlparse
from typing import Tuple

def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""

def key_exact(url: str) -> str:
    return sha1(url.encode("utf-8")).hexdigest()

def key_company_title_host(company: str | None, title: str | None, host: str | None) -> str:
    c = (company or "").strip().lower()
    t = (title or "").strip().lower()
    h = (host or "").strip().lower()
    return sha1(f"{c}|{t}|{h}".encode("utf-8")).hexdigest()