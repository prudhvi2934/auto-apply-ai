from __future__ import annotations
import csv
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from auto_apply_ai.schemas.job_intake_scm import ImportRowWarning, ImportRowError
from auto_apply_ai.services.job_intake.ingest.normalizers import normalize_capture_row
from auto_apply_ai.services.job_intake.ingest.validators import validate_row
from auto_apply_ai.db.repository import create_capture, upsert_job_posting_for_capture
from auto_apply_ai.utils.time import parse_captured_at

async def process_csv_reader(
    reader: csv.DictReader,
    session: AsyncSession,
    dry_run: bool,
    batch_id: str,
) -> Tuple[int, int, List[ImportRowWarning], List[ImportRowError]]:
    accepted = 0
    quarantined = 0
    warnings_by_row: List[ImportRowWarning] = []
    errors_by_row: List[ImportRowError] = []

    async with session.begin():
        for idx, raw in enumerate(reader):
            row = normalize_capture_row(raw)
            row["captured_at"] = parse_captured_at(row.get("captured_at"))
            row["import_batch_id"] = batch_id

            hard, soft = validate_row(row)
            if hard:
                quarantined += 1
                errors_by_row.append(ImportRowError(row_index=idx, errors=hard))
                if soft:
                    warnings_by_row.append(ImportRowWarning(row_index=idx, warnings=soft))
                continue

            if soft:
                warnings_by_row.append(ImportRowWarning(row_index=idx, warnings=soft))

            if dry_run:
                accepted += 1
                continue

            capture_id = await create_capture(session, row)
            await upsert_job_posting_for_capture(session, capture_id, row)
            accepted += 1

    return accepted, quarantined, warnings_by_row, errors_by_row