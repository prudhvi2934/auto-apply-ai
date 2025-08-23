# src/auto_apply_ai/api/app.py
from __future__ import annotations
from fastapi import FastAPI
from contextlib import asynccontextmanager

from auto_apply_ai.db.engine import engine, Base  # Base imported from models/entities via engine
from auto_apply_ai.api.routers import job_intake

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev-only; use Alembic in real deployments
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    app = FastAPI(title="Auto Apply AI", lifespan=lifespan)
    app.include_router(job_intake.router)
    return app

app = create_app()