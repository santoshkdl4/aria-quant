from fastapi import APIRouter
from pydantic import BaseModel
from app.trading.executor import PaperTradingEngine

router = APIRouter()
engine = PaperTradingEngine()

class TradeRequest(BaseModel):
    symbol: str
    side: str
    qty: int
    price: float

@router.get("/portfolio")
def get_portfolio():
    return {"status": "success", "data": engine.get_portfolio_status()}

@router.post("/execute_mock")
def execute_mock(req: TradeRequest):
    success = engine.execute_mock_trade(req.symbol, req.side.upper(), req.qty, req.price)
    if success:
        return {"status": "success", "message": f"Executed {req.side} {req.qty} {req.symbol}"}
    return {"status": "error", "message": "Trade execution failed (insufficient funds/positions)"}
