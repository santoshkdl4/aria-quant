from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from app.data.fetchers import YFinanceFetcher
from app.db.duckdb_session import get_duckdb_connection

router = APIRouter()

class IngestRequest(BaseModel):
    symbol: str
    timeframe: str = "1d"
    start_date: str = "2020-01-01"
    end_date: Optional[str] = None

def _run_ingestion(req: IngestRequest):
    fetcher = YFinanceFetcher()
    # Add standard suffixes if missing
    sym = req.symbol
    if not sym.endswith(".NS") and not sym.endswith(".BO") and not "^" in sym:
        # Assume NSE if it's an Indian stock
        sym = f"{sym}.NS"
        
    fetcher.fetch_historical(sym, req.timeframe, req.start_date, req.end_date)

@router.post("/ingest")
def trigger_ingestion(req: IngestRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_ingestion, req)
    return {"message": f"Ingestion job queued for {req.symbol}"}

@router.get("/summary")
def get_data_summary():
    try:
        con = get_duckdb_connection()
        res = con.execute("""
            SELECT symbol, MIN(timestamp) as min_date, MAX(timestamp) as max_date, COUNT(*) as rows
            FROM market_data
            GROUP BY symbol
        """).df()
        
        # Convert to list of dicts
        records = res.to_dict('records')
        return {"status": "success", "datasets": records}
    except Exception as e:
        return {"status": "error", "message": str(e), "datasets": []}
