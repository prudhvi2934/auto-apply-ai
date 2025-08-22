# src/auto_apply_ai/core/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./auto_apply_ai.db"
    DEBUG: bool = True

settings = Settings()
