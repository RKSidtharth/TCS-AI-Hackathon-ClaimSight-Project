"""
CLAIMSIGHT AI - Core Application Settings
"""

import os
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel as BaseSettings
    def SettingsConfigDict(**kwargs):
        return kwargs

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

def get_storage_path(subfolder: str) -> str:
    """Returns a writable directory for storage, falling back to tempdir in serverless environments (e.g. Vercel)."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target = os.path.join(base_dir, "storage", subfolder)
    try:
        os.makedirs(target, exist_ok=True)
        test_file = os.path.join(target, ".test_write")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
        return target
    except (OSError, IOError, PermissionError):
        import tempfile
        tmp = os.path.join(tempfile.gettempdir(), "claimsight_storage", subfolder)
        os.makedirs(tmp, exist_ok=True)
        return tmp

