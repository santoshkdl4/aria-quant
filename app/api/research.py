from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from agents.research_agent import MockGeminiResearchAgent
from app.research.memory_manager import MemoryManager

router = APIRouter()

class ExperimentRequest(BaseModel):
    symbol: str

def _run_experiment(symbol: str):
    agent = MockGeminiResearchAgent()
    agent.propose_and_test(symbol)

@router.post("/experiment")
def trigger_experiment(req: ExperimentRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_experiment, req.symbol)
    return {"message": f"AI Research Experiment queued for {req.symbol}"}

@router.get("/graveyard")
def get_graveyard():
    try:
        data = MemoryManager.get_graveyard_summary()
        return {"status": "success", "strategies": data}
    except Exception as e:
        return {"status": "error", "message": str(e), "strategies": []}
