"""Configuration settings for Quantum-N3BULA API."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    
    app_name: str = "Quantum-N3BULA API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_log_entries: int = int(os.getenv("MAX_LOG_ENTRIES", "1000"))


settings = Settings()
