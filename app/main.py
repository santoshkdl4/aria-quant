import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import logger
from app.db.session import state_engine, memory_engine, Base

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
    Base.metadata.create_all(bind=state_engine)
    Base.metadata.create_all(bind=memory_engine)
    
    yield
    
    logger.info("ARIA QUANT system shutting down gracefully.")

app = FastAPI(
    title="ARIA QUANT API",
    description="Autonomous Research & Investment AI",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "paper_trading" if not settings.LIVE_TRADING_ENABLED else "LIVE"}

if __name__ == "__main__":
    logger.info("Starting ARIA QUANT Backend...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
