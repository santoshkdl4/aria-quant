import os
import pandas as pd
import numpy as np
import ta 
from app.core.logger import logger
from app.research.backtester import run_backtest
from app.research.memory_manager import MemoryManager
from app.db.duckdb_session import get_duckdb_connection

class MockGeminiResearchAgent:
    def __init__(self):
        self.agent_id = "research_alpha"
        
    def propose_and_test(self, symbol: str):
        logger.info(f"Research Agent waking up for {symbol}")
        
        # 1. Check Graveyard (Memory)
        graveyard = MemoryManager.get_graveyard_summary()
        logger.info(f"Agent analyzed {len(graveyard)} past failures.")
        
        # 2. Fetch Data
        con = get_duckdb_connection()
        try:
            df = con.execute(f"SELECT * FROM market_data WHERE symbol = '{symbol}' ORDER BY timestamp ASC").df()
            if df.empty:
                logger.warning(f"No data for {symbol}, aborting research.")
                return False
        except Exception as e:
            logger.error(f"DB Error: {e}")
            return False
            
        # 3. "Generate" Code (Mocking LLM output)
        strategy_code = """
def generate_signals(df):
    import ta
    import numpy as np
    df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
    df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
    
    # 1 for Golden Cross, -1 for Death Cross
    df['signal'] = np.where(df['sma_20'] > df['sma_50'], 1, -1)
    # Neutral if nan
    df['signal'] = df['signal'].fillna(0)
    return df
"""
        # 4. Execute Code in Sandbox
        local_scope = {}
        try:
            exec(strategy_code, globals(), local_scope)
            generate_signals_func = local_scope['generate_signals']
            df_signaled = generate_signals_func(df.copy())
        except Exception as e:
            logger.error(f"Generated code failed to execute: {e}")
            return False
            
        # 5. Backtest
        results = run_backtest(df_signaled)
        logger.info(f"Backtest Results for Mock SMA Strategy: {results.to_dict()}")
        
        # 6. Evaluate and Store
        exp_id = MemoryManager.create_experiment(self.agent_id, "Find a moving average crossover strategy")
        
        status = "PROMOTED" if results.sharpe_ratio > 1.0 and results.total_return > 0 else "REJECTED"
        reason = "Metrics below threshold" if status == "REJECTED" else "Passed"
        
        MemoryManager.save_strategy_evaluation(
            experiment_id=exp_id,
            name="SMA_20_50_Crossover",
            code=strategy_code,
            metrics=results.to_dict(),
            status=status,
            failure_reason=reason
        )
        
        return True
