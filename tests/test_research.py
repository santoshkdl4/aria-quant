import pandas as pd
import numpy as np
from app.research.backtester import run_backtest

def test_backtester():
    # Create mock data
    dates = pd.date_range("2024-01-01", periods=10)
    # Price goes up steadily by 10% each day
    close = [100 * (1.1 ** i) for i in range(10)]
    
    df = pd.DataFrame({
        'timestamp': dates,
        'close': close,
        'signal': [1] * 10 # Always long
    })
    
    results = run_backtest(df)
    
    assert results.trades_count > 0
    assert results.total_return > 0
    assert results.win_rate == 1.0 # Every day is positive
