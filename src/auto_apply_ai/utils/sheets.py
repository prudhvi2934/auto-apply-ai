from __future__ import annotations
from urllib.parse import urlparse, parse_qs

def gsheet_to_csv_url(sheet_url: str) -> str:
    if not sheet_url:
        raise ValueError("sheet_url is required")
    if "export" in sheet_url and "format=csv" in sheet_url:
        return sheet_url
    p = urlparse(sheet_url)
    if p.netloc != "docs.google.com":
        raise ValueError("Not a Google Sheets URL")
    parts = p.path.strip("/").split("/")
    sheet_id = parts[2] if len(parts) >= 3 and parts[0] == "spreadsheets" and parts[1] == "d" else None
    if not sheet_id:
        raise ValueError("Unable to parse sheet id from URL")
    gid = None
    if p.fragment and p.fragment.startswith("gid="):
        gid = p.fragment.split("=", 1)[1]
    if not gid:
        qs = parse_qs(p.query)
        gid = (qs.get("gid", [None])[0]) or "0"
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"