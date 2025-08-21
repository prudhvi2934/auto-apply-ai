# src/auto_apply_ai/api/main.py
from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Depends
from typing import Optional, List, AsyncGenerator
from contextlib import asynccontextmanager
from pydantic import BaseModel
import csv, io, uuid
from datetime import datetime,timezone

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from auto_apply_ai.api.schemas import ImportResult, ImportRowWarning, ImportRowError, JobListResponse, JobPostingOut
from auto_apply_ai.core.db import AsyncSessionLocal, engine, Base
from auto_apply_ai.core.models import JobPosting
from auto_apply_ai.ingest.normalizers import normalize_capture_row
from auto_apply_ai.ingest.validators import validate_row
from auto_apply_ai.core.repo import create_capture, upsert_job_posting_for_capture

# ---- Utilities ----

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session: # type: ignore
        yield session

def _now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0)

def parse_captured_at(value: str | None) -> datetime:
    if not value:  # missing in CSV
        return _now_utc()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)

# ---- Startup (dev convenience; keep Alembic for real migrations) ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Auto Apply AI", lifespan=lifespan)

# ---- Endpoints ----

@app.post("/import/csv", response_model=ImportResult)
async def import_csv(
    file: UploadFile = File(...),
    dry_run: bool = Query(False),
    import_batch_id: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    """
    Accepts a CSV with columns:
    source_site, source_url, job_title, company, location, apply_url_hint,
    seniority_hint, compensation_hint, tags, notes, captured_at
    """
    content = await file.read()
    text = content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    accepted = 0
    quarantined = 0
    warnings_by_row: List[ImportRowWarning] = []
    errors_by_row: List[ImportRowError] = []

    batch_id = import_batch_id or str(uuid.uuid4())

    # async with get_session() as session:
    async with session.begin():
        for idx, raw in enumerate(reader):
            # Normalize
            row = normalize_capture_row(raw)
            # Ensure captured_at exists
            row["captured_at"] = parse_captured_at(row.get("captured_at"))
            row["import_batch_id"] = batch_id

            # Validate
            hard, soft = validate_row(row)
            if hard:
                quarantined += 1
                errors_by_row.append(ImportRowError(row_index=idx, errors=hard))
                if soft:
                    warnings_by_row.append(ImportRowWarning(row_index=idx, warnings=soft))
                continue  # skip hard-error rows

            if soft:
                warnings_by_row.append(ImportRowWarning(row_index=idx, warnings=soft))

            if dry_run:
                accepted += 1
                continue

            # Persist capture
            capture_id = await create_capture(session, row)
            # Upsert/merge posting
            await upsert_job_posting_for_capture(session, capture_id, row)
            accepted += 1

        # end transaction

    return ImportResult(
        accepted=accepted,
        quarantined=quarantined,
        warnings_by_row=warnings_by_row,
        errors_by_row=errors_by_row,
        batch_id=batch_id,
    )

@app.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    status: Optional[str] = Query(default=None),
    company: Optional[str] = Query(default=None),
    host: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    cursor: Optional[str] = Query(default=None, description="Opaque cursor = last seen posting id"),
    session: AsyncSession = Depends(get_session)
):
    """
    Cursor pagination:
    - Sort by id desc (string UUID works well-enough here)
    - If cursor provided, return rows with id < cursor in that ordering
    """
   
    where = []
    if status:
        where.append(JobPosting.status == status)
    if company:
        where.append(JobPosting.company.ilike(f"%{company}%"))
    if host:
        where.append(JobPosting.source_host == host)

    stmt = select(JobPosting)
       
    if where:
        stmt = stmt.where(and_(*where))
    stmt = stmt.order_by(desc(JobPosting.id)).limit(limit + 1)

    if cursor:
        # string compare on UUIDs is fine for ordering consistency within same generation scheme
        stmt = stmt.where(JobPosting.id < cursor)

    rows = (await session.execute(stmt)).scalars().all()

    next_cursor = None
    if len(rows) > limit:
        next_cursor = str(rows[limit].id)
        rows = rows[:limit]

    items = [
        JobPostingOut(
            id=getattr(r, "id"),
            canonical_url=getattr(r, "canonical_url"),
            company=getattr(r, "company"),
            job_title=getattr(r, "job_title"),
            location=getattr(r, "location"),
            source_host=getattr(r, "source_host"),
            status=getattr(r, "status"),
            next_action=getattr(r, "next_action"),
            ats_req_id=getattr(r, "ats_req_id"),
            ats=None
        )
        for r in rows
    ]
    return JobListResponse(items=items, next_cursor=next_cursor)

@app.get("/jobs/{job_id}", response_model=JobPostingOut)
async def get_job(job_id: str,session: AsyncSession = Depends(get_session)):
   
    res = await session.execute(select(JobPosting).where(JobPosting.id == job_id))
    r = res.scalar_one_or_none()
    if not r:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobPostingOut(
        id=getattr(r, "id"),
        canonical_url=getattr(r, "canonical_url"),
        company=getattr(r, "company"),
        job_title=getattr(r, "job_title"),
        location=getattr(r, "location"),
        source_host=getattr(r, "source_host"),
        status=getattr(r, "status"),
        next_action=getattr(r, "next_action"),
        ats_req_id=getattr(r, "ats_req_id"),
        ats=None
    )