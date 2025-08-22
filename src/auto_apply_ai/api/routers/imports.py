from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, Query, HTTPException, Depends
from typing import Optional
import uuid, csv, io, httpx

from sqlalchemy.ext.asyncio import AsyncSession

from auto_apply_ai.schemas import ImportResult
from auto_apply_ai.api.deps import get_session
from auto_apply_ai.services.import_pipeline import process_csv_reader
from auto_apply_ai.utils.sheets import gsheet_to_csv_url

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/csv", response_model=ImportResult)
async def import_csv(
    file: UploadFile = File(...),
    dry_run: bool = Query(False),
    import_batch_id: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    text = (await file.read()).decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    batch_id = import_batch_id or str(uuid.uuid4())
    acc, qua, warns, errs = await process_csv_reader(reader, session, dry_run, batch_id)
    return ImportResult(accepted=acc, quarantined=qua, warnings_by_row=warns, errors_by_row=errs, batch_id=batch_id)

@router.post("/google_sheet", response_model=ImportResult)
async def import_google_sheet(
    sheet_url: str = Query(..., description="Google Sheet link (viewer link ok)"),
    dry_run: bool = Query(False),
    import_batch_id: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    batch_id = import_batch_id or str(uuid.uuid4())
    csv_url = gsheet_to_csv_url(sheet_url)
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        resp = await client.get(csv_url)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch sheet CSV: {resp.status_code}")
        text = resp.text
    reader = csv.DictReader(io.StringIO(text))
    acc, qua, warns, errs = await process_csv_reader(reader, session, dry_run, batch_id)
    return ImportResult(accepted=acc, quarantined=qua, warnings_by_row=warns, errors_by_row=errs, batch_id=batch_id)