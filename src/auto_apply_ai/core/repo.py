# src/auto_apply_ai/core/repo.py
from __future__ import annotations
from typing import Dict, Any, Optional, Tuple, List
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from auto_apply_ai.core.models import JobPosting, JobCapture
from auto_apply_ai.dedupe.keys import key_exact, key_company_title_host, host_of

async def create_capture(session: AsyncSession, data: Dict[str, Any]) -> str:
    cap = JobCapture(**data)
    session.add(cap)
    await session.flush()
    return str(cap.id)

async def upsert_job_posting_for_capture(session: AsyncSession, capture_id: str, capture: Dict[str, Any]) -> str:
    """
    - Compute canonical_url (for now: cleaned source_url)
    - Compute dedupe keys
    - Merge with existing by exact URL or company+title+host
    """
    canonical_url = capture["source_url"]
    host = host_of(canonical_url)
    dk_exact = key_exact(canonical_url)
    dk_cth = key_company_title_host(capture.get("company"), capture.get("job_title"), host)

    # Try exact
    q = await session.execute(select(JobPosting).where(JobPosting.dedupe_key_exact == dk_exact))
    post = q.scalar_one_or_none()
    if post is None:
        # Try company-title-host
        q = await session.execute(select(JobPosting).where(JobPosting.dedupe_key_company_title_host == dk_cth))
        post = q.scalar_one_or_none()

    if post is None:
        # Create
        post = JobPosting(
            canonical_url=canonical_url,
            company=capture.get("company") or "",
            job_title=capture.get("job_title") or "",
            location=capture.get("location"),
            source_host=host,
            status="new",
            next_action="retry_fetch",
            capture_ids=[capture_id],
            dedupe_key_exact=dk_exact,
            dedupe_key_company_title_host=dk_cth,
            ats_req_id=None,
        )
        session.add(post)
        await session.flush()
        return str(post.id)

    # Merge
    merged_capture_ids = list({*(post.capture_ids or []), capture_id})
    if not getattr(post, "company", None) and capture.get("company"):
        post.company = capture["company"]
    if not getattr(post, "job_title", None) and capture.get("job_title"):
        post.job_title = capture["job_title"]
    if not getattr(post, "location", None) and capture.get("location"):
        post.location = capture["location"]
    # Ensure capture_ids is assigned a plain list of strings
    post.capture_ids = [str(cid) for cid in merged_capture_ids] # type: ignore
    await session.flush()
    return str(post.id)