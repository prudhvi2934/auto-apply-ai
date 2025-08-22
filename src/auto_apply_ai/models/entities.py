# src/auto_apply_ai/models/entities.py
from sqlalchemy import (
    Column, String, DateTime, Enum, Float, ForeignKey, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
import uuid
from auto_apply_ai.db.engine import Base

Status = ("new","alive","dead_link","login_wall","expired","needs_review","resolved_ats","no_ats_link","error")
NextAction = ("tailor_resume","review_details","retry_fetch","drop","none")
ATSTypes = ("workday","greenhouse","lever","smartrecruiters","icims","taleo","ashby","bamboohr","teamtailor","unknown")

def _uuid() -> str:
    return str(uuid.uuid4())

class JobCapture(Base):
    __tablename__ = "job_captures"
    id = Column(String, primary_key=True, default=_uuid)
    source_site = Column(String, nullable=True)
    source_url = Column(Text, nullable=False)
    job_title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    apply_url_hint = Column(Text, nullable=True)
    seniority_hint = Column(String, nullable=True)
    compensation_hint = Column(String, nullable=True)
    tags = Column(JSON, default=list)            # list[str]
    notes = Column(Text, nullable=True)
    captured_at = Column(DateTime, nullable=False)
    import_batch_id = Column(String, nullable=True)
    hard_errors = Column(JSON, default=list)     # list[str]
    soft_warnings = Column(JSON, default=list)   # list[str]

class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(String, primary_key=True, default=_uuid)
    canonical_url = Column(Text, nullable=False)
    company = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    location = Column(String, nullable=True)
    source_host = Column(String, nullable=False)
    status = Column(Enum(*Status, name="posting_status"), nullable=False, default="new")
    next_action = Column(Enum(*NextAction, name="posting_next_action"), nullable=False, default="retry_fetch")
    capture_ids = Column(JSON, default=list)     # list[str] of JobCapture ids
    dedupe_key_exact = Column(String, nullable=False)
    dedupe_key_company_title_host = Column(String, nullable=False)
    ats_req_id = Column(String, nullable=True)
    last_checked_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("canonical_url", name="uq_job_postings_canonical_url"),
        Index("ix_job_postings_dk_exact", "dedupe_key_exact"),
        Index("ix_job_postings_dk_cth", "dedupe_key_company_title_host"),
        Index("ix_job_postings_status", "status"),
        Index("ix_job_postings_company", "company"),
    )

class AtsResolution(Base):
    __tablename__ = "ats_resolutions"
    id = Column(String, primary_key=True, default=_uuid)
    posting_id = Column(String, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    ats_type = Column(Enum(*ATSTypes, name="ats_type"), nullable=False, default="unknown")
    ats_url = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False, default=0.0)
    method = Column(String, nullable=False, default="pattern")

    posting = relationship("JobPosting", backref="ats_resolution", uselist=False)
