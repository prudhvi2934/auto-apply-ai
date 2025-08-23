# src/auto_apply_ai/ingest/normalizers.py
from __future__ import annotations
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import Dict, Any, Iterable, List
import re

TRACKING_PARAMS = {
    "utm_source","utm_medium","utm_campaign","utm_term","utm_content",
    "gclid","fbclid","msclkid","mc_cid","mc_eid","igshid","utm_id","utm_reader"
}

def clean_url(u: str) -> str:
    """
    - lowercase host
    - strip common tracking params
    - remove empty query params
    - normalize trailing slash for path-only (leave if significant)
    - keep fragment only if not tracking-ish
    """
    if not u:
        return u
    p = urlparse(u.strip())
    host = (p.netloc or "").lower()
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=False) if k not in TRACKING_PARAMS]
    query.sort()
    new_query = urlencode(query, doseq=True)
    path = p.path or "/"
    # normalize: collapse multiple slashes (but not for http(s)://)
    path = re.sub(r"//+", "/", path)
    # strip trailing slash if path not root
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    frag = p.fragment
    if frag and frag.lower().startswith(("utm_", "ref")):
        frag = ""
    newp = p._replace(netloc=host, query=new_query, path=path, fragment=frag)
    return urlunparse(newp)

def normalize_text(s: str | None) -> str | None:
    if s is None:
        return None
    s = re.sub(r"\s+", " ", s.strip())
    return s or None

def normalize_tags(t: str | List[str] | None) -> List[str]:
    if t is None:
        return []
    if isinstance(t, list):
        vals = t
    else:
        vals = re.split(r"[;,|\n]+", t)
    out = sorted(set(filter(None, (x.strip().lower() for x in vals))))
    return out

def normalize_capture_row(row: Dict[str, Any]) -> Dict[str, Any]:
    row = dict(row)
    row["source_url"] = clean_url(row.get("source_url", ""))
    row["apply_url_hint"] = clean_url(row.get("apply_url_hint", "")) if row.get("apply_url_hint") else None
    for k in ("job_title","company","location","seniority_hint","compensation_hint","notes","source_site"):
        row[k] = normalize_text(row.get(k))
    row["tags"] = normalize_tags(row.get("tags"))
    return row