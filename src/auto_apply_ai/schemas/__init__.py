# src/auto_apply_ai/api/schemas.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any

class ImportRowWarning(BaseModel):
    row_index: int
    warnings: List[str] = []

class ImportRowError(BaseModel):
    row_index: int
    errors: List[str] = []

class ImportResult(BaseModel):
    accepted: int
    quarantined: int
    warnings_by_row: List[ImportRowWarning] = []
    errors_by_row: List[ImportRowError] = []
    batch_id: Optional[str] = None

class JobPostingOut(BaseModel):
    id: str
    canonical_url: str
    company: str
    job_title: str
    location: Optional[str] = None
    source_host: str
    status: str
    next_action: str
    ats_req_id: Optional[str] = None
    ats: Optional[dict] = None

class JobListResponse(BaseModel):
    items: List[JobPostingOut]
    next_cursor: Optional[str] = None