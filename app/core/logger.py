import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings, APP_DATA_DIR

# Configure structured logging
log_dir = APP_DATA_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# Remove default handler
logger.remove()

# Add console handler only if stderr exists (it is None in --noconsole Windows apps)
if sys.stderr:
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

# Add file handler with rotation
logger.add(
    str(log_dir / "aria_{time:YYYY-MM-DD}.log"),
    level=settings.LOG_LEVEL,
    rotation="00:00",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    enqueue=True, # Thread-safe
)

# Add JSON structured log for programmatic consumption
logger.add(
    str(log_dir / "aria_{time:YYYY-MM-DD}.jsonl"),
    level="INFO",
    rotation="00:00",
    retention="30 days",
    serialize=True,
    enqueue=True,
)

logger.info("Logger initialized.")
