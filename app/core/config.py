import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure paths are resolved relative to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Application Mode
    LIVE_TRADING_ENABLED: bool = False
    ENVIRONMENT: str = "development"

    # API Keys
    GEMINI_API_KEY: str = ""

    # Database Paths
    STATE_DB_PATH: str = "data/databases/aria_state.db"
    MEMORY_DB_PATH: str = "data/databases/aria_memory.db"
    MARKET_DATA_PATH: str = "data/parquet/"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / "config" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_state_db_url(self) -> str:
        db_path = PROJECT_ROOT / self.STATE_DB_PATH
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"

    def get_memory_db_url(self) -> str:
        db_path = PROJECT_ROOT / self.MEMORY_DB_PATH
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"

settings = Settings()
