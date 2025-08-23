# from __future__ import annotations
# from fastapi import APIRouter, Query, HTTPException, Depends, status
# from typing import Optional
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, and_, desc, delete

# from auto_apply_ai.schemas import JobListResponse, JobPostingOut
# from auto_apply_ai.api.deps import get_session
# from auto_apply_ai.models.entities import JobPosting, JobCapture, AtsResolution


# router = APIRouter(prefix="/jobs", tags=["jobs"])

# @router.get("", response_model=JobListResponse)
# async def list_jobs(
#     status: Optional[str] = Query(default=None),
#     company: Optional[str] = Query(default=None),
#     host: Optional[str] = Query(default=None),
#     limit: int = Query(default=50, ge=1, le=200),
#     cursor: Optional[str] = Query(default=None),
#     session: AsyncSession = Depends(get_session)
# ):
#     where = []
#     if status:
#         where.append(JobPosting.status == status)
#     if company:
#         where.append(JobPosting.company.ilike(f"%{company}%"))
#     if host:
#         where.append(JobPosting.source_host == host)

#     stmt = select(JobPosting)
#     if where:
#         stmt = stmt.where(and_(*where))
#     stmt = stmt.order_by(desc(JobPosting.id)).limit(limit + 1)
#     if cursor:
#         stmt = stmt.where(JobPosting.id < cursor)

#     rows = (await session.execute(stmt)).scalars().all()
#     next_cursor = None
#     if len(rows) > limit:
#         next_cursor = str(rows[limit].id)
#         rows = rows[:limit]

#     items = [
#         JobPostingOut(
#             id=getattr(r, "id"),
#             canonical_url=getattr(r, "canonical_url"),
#             company=getattr(r, "company"),
#             job_title=getattr(r, "job_title"),
#             location=getattr(r, "location"),
#             source_host=getattr(r, "source_host"),
#             status=getattr(r, "status"),
#             next_action=getattr(r, "next_action"),
#             ats_req_id=getattr(r, "ats_req_id"),
#             ats=None,
#         )
#         for r in rows
#     ]
#     return JobListResponse(items=items, next_cursor=next_cursor)

# @router.get("/{job_id}", response_model=JobPostingOut)
# async def get_job(job_id: str, session: AsyncSession = Depends(get_session)):
#     r = (await session.execute(select(JobPosting).where(JobPosting.id == job_id))).scalar_one_or_none()
#     if not r:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return JobPostingOut(
#         id=getattr(r, "id"),
#             canonical_url=getattr(r, "canonical_url"),
#             company=getattr(r, "company"),
#             job_title=getattr(r, "job_title"),
#             location=getattr(r, "location"),
#             source_host=getattr(r, "source_host"),
#             status=getattr(r, "status"),
#             next_action=getattr(r, "next_action"),
#             ats_req_id=getattr(r, "ats_req_id"),
#             ats=None,
#     )


# @router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_job(job_id: str, session: AsyncSession = Depends(get_session)):
#     # 1) load the posting
#     res = await session.execute(select(JobPosting).where(JobPosting.id == job_id))
#     posting = res.scalar_one_or_none()
#     if not posting:
#         raise HTTPException(status_code=404, detail="Job not found")

#     # 2) delete related JobCaptures (capture_ids lives on the posting as a JSON list)
#     capture_ids = posting.capture_ids or []
#     if isinstance(capture_ids, list) and len(capture_ids) > 0:
#         await session.execute(
#             delete(JobCapture).where(JobCapture.id.in_(capture_ids))
#         )

#     # 3) delete related AtsResolution (defensive; DB may already cascade)
#     await session.execute(
#         delete(AtsResolution).where(AtsResolution.posting_id == job_id)
#     )

#     # 4) delete the posting
#     await session.delete(posting)
#     await session.commit()
#     return None