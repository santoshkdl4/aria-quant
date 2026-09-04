import os
import psutil
import time
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings, APP_DATA_DIR

router = APIRouter()

# Record startup time for uptime calculation
START_TIME = time.time()

class SystemHealthResponse(BaseModel):
    status: str
    mode: str
    uptime_seconds: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_free_gb: float
    db_size_mb: float

@router.get("/health", response_model=SystemHealthResponse)
def get_system_health():
    cpu = psutil.cpu_percent(interval=0.1) # short block to get accurate reading
    mem = psutil.virtual_memory()
    
    # Get disk usage for the current directory
    try:
        disk = psutil.disk_usage(os.getcwd())
        disk_free_gb = disk.free / (1024 ** 3)
    except Exception:
        disk_free_gb = 0.0

    # Calculate Database Size
    db_size = 0.0
    data_dir = APP_DATA_DIR / "data"
    if data_dir.exists():
        for f in data_dir.glob("*.db"):
            db_size += f.stat().st_size
    db_size_mb = db_size / (1024 ** 2)

    return SystemHealthResponse(
        status="healthy",
        mode="paper_trading" if not settings.LIVE_TRADING_ENABLED else "LIVE",
        uptime_seconds=time.time() - START_TIME,
        cpu_percent=cpu,
        memory_percent=mem.percent,
        memory_used_mb=mem.used / (1024 ** 2),
        disk_free_gb=round(disk_free_gb, 2),
        db_size_mb=round(db_size_mb, 2)
    )
