"""Application configuration."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Quantum-N3BULA"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./quantum_nebula.db"
    )

    # JWT Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "quantum-nebula-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://frontend:3000"]

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        extra = "ignore"


settings = Settings()
