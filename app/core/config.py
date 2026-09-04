import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure paths are resolved relative to the user's home directory for portability
USER_HOME = Path(os.path.expanduser("~"))
APP_DATA_DIR = USER_HOME / ".aria_quant"

class Settings(BaseSettings):
    # Application Mode
    LIVE_TRADING_ENABLED: bool = False
    ENVIRONMENT: str = "development"

    # API Keys
    GEMINI_API_KEY: str = ""

    # Database Paths
    STATE_DB_PATH: str = "data/databases/aria_state_v2.db"
    MEMORY_DB_PATH: str = "data/databases/aria_memory.db"
    MARKET_DATA_PATH: str = "data/parquet/"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(APP_DATA_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_state_db_url(self) -> str:
        db_path = APP_DATA_DIR / self.STATE_DB_PATH
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite+aiosqlite:///{db_path}"

    def get_memory_db_url(self) -> str:
        db_path = APP_DATA_DIR / self.MEMORY_DB_PATH
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite+aiosqlite:///{db_path}"

settings = Settings()
