"""
CLAIMSIGHT AI - Core Application Settings
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Security
    JWT_SECRET: str = "claimsight_super_secret_jwt_key_change_in_production_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "claimsight_ai"

    # Storage
    STORAGE_PROVIDER: str = "local"
    STORAGE_LOCAL_DIR: str = "storage/uploads"
    MAX_UPLOAD_SIZE_BYTES: int = 52428800  # 50MB

    # High-Impact Decision Guardrail (5 Lakhs INR)
    HIGH_IMPACT_THRESHOLD_INR: float = 500000.0

    # AI & Integrations
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    WEATHER_API_KEY: str = ""
    TELEMATICS_ENABLED: bool = True
    ENABLE_SYNTHETIC_BENCHMARKS: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
