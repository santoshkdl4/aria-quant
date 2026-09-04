import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import logger
from app.db.session import state_engine, memory_engine, Base
from app.scheduler.scheduler import start_scheduler, stop_scheduler
from app.data.live import live_feed

# Import all models here so SQLAlchemy knows about them before create_all
from app.db.models_state import AgentState, ApprovalRequest
from app.db.models_memory import Experiment, Strategy, DecisionLog, SystemMemory

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ARIA QUANT system...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Live Trading Enabled: {settings.LIVE_TRADING_ENABLED}")
    
    # Initialize DB schemas
    logger.info("Checking database schemas...")
    logger.info("Initializing Memory Database...")
    async with state_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with memory_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Initialize trading engine state
    from app.api.trading import engine
    await engine.initialize()
    
    
    # Start Scheduler
    start_scheduler()
    
    yield
    
    # Shutdown
    stop_scheduler()
    logger.info("ARIA QUANT system shutting down gracefully.")

app = FastAPI(
    title="ARIA QUANT API",
    description="Autonomous Research & Investment AI",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api.health import router as health_router
from app.api.data import router as data_router
from app.api.research import router as research_router
from app.api.trading import router as trading_router
from app.api.ws import router as ws_router

# Include routers
app.include_router(health_router, prefix="/api/system", tags=["System"])
app.include_router(data_router, prefix="/api/data", tags=["Data"])
app.include_router(research_router, prefix="/api/research", tags=["Research"])
app.include_router(trading_router, prefix="/api/trading", tags=["Trading"])
app.include_router(ws_router, prefix="/api/ws", tags=["WebSockets"])

# Serve Frontend statically
frontend_dist = os.path.join(os.path.dirname(__file__), "dashboard", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        # Allow serving standard files from dist root (e.g. vite.svg, robots.txt)
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            response = FileResponse(file_path)
        else:
            response = FileResponse(os.path.join(frontend_dist, "index.html"))
        
        # Prevent caching of index.html so Vite bundle updates propagate immediately
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
else:
    logger.warning("Frontend dist folder not found. Running in API-only mode.")

if __name__ == "__main__":
    logger.info("Starting ARIA QUANT Backend...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
