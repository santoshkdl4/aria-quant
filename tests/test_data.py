import os
import pytest
from app.api.data import IngestRequest
from app.data.fetchers import YFinanceFetcher
from app.db.duckdb_session import get_duckdb_connection
from app.core.config import settings, APP_DATA_DIR

def test_yfinance_fetcher():
    # Only test a small timeframe to not block CI
    fetcher = YFinanceFetcher()
    # RELIANCE.NS for 5 days
    success = fetcher.fetch_historical("RELIANCE.NS", "1d", "2024-01-01", "2024-01-07")
    assert success is True
    
    # Verify the parquet file was created using Hive partitioning
    expected_path = APP_DATA_DIR / settings.MARKET_DATA_PATH / "symbol=RELIANCE_NS"
    assert expected_path.exists()

def test_duckdb_connection():
    # Verify duckdb can read the created file
    con = get_duckdb_connection()
    res = con.execute("SELECT * FROM market_data WHERE symbol = 'RELIANCE_NS'").df()
    assert not res.empty
    assert len(res) > 0
    assert 'timestamp' in res.columns
    assert 'close' in res.columns
