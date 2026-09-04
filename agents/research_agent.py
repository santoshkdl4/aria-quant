import os
import re
import pandas as pd
import numpy as np
import ta 
from app.core.logger import logger
from app.research.backtester import run_backtest
from app.research.memory_manager import MemoryManager
from app.db.duckdb_session import get_duckdb_connection
from app.core.config import settings

# Attempt to import google genai
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    logger.warning("google-genai not installed or import failed.")

class MockGeminiResearchAgent:
    def __init__(self):
        self.agent_id = "research_alpha"
        self.model_name = 'gemini-2.5-pro'
        
        if genai and settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            self.client = None
            logger.warning("Gemini Client not initialized. Please set GEMINI_API_KEY.")

    def extract_python_code(self, text: str) -> str:
        # Extracts code from markdown blocks
        match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1)
        return text # fallback

    def propose_and_test(self, symbol: str, max_retries: int = 3):
        logger.info(f"Research Agent waking up for {symbol}")
        
        # 1. Fetch Data
        con = get_duckdb_connection()
        try:
            df = con.execute(f"SELECT * FROM market_data WHERE symbol = '{symbol}' ORDER BY timestamp ASC").df()
            if df.empty:
                logger.warning(f"No data for {symbol}, aborting research.")
                return False
        except Exception as e:
            logger.error(f"DB Error: {e}")
            return False
            
        # 2. Get Graveyard
        graveyard = MemoryManager.get_graveyard_summary()
        failures = "\n".join([f"- ID: {g['id']}, Reason: {g['failure_reason']}, Sharpe: {g['sharpe_ratio']}" for g in graveyard])
        if not failures:
            failures = "None."
            
        exp_id = MemoryManager.create_experiment(self.agent_id, "Evolve a profitable strategy")
        
        feedback = ""
        
        for attempt in range(max_retries):
            logger.info(f"Attempt {attempt + 1}/{max_retries} for {symbol}...")
            
            # 3. Generate Prompt
            prompt = f"""
You are a quantitative researcher building trading strategies in Python.
Your objective is to maximize the Sharpe Ratio (target > 1.0) and Total Return.
The dataset is a Pandas DataFrame `df` with columns: timestamp, open, high, low, close, volume.

You must output a Python function EXACTLY matching this signature:
```python
def generate_signals(df):
    import ta
    import numpy as np
    import pandas as pd
    
    # YOUR LOGIC HERE
    
    # Must return a DataFrame with a 'signal' column. 1 = Long, -1 = Short, 0 = Neutral.
    return df
```

Past failed strategies you should avoid:
{failures}

{f"Previous Attempt Feedback: {feedback}" if feedback else ""}

Please provide ONLY the python code block containing the function.
"""
            # 4. Call LLM
            strategy_code = ""
            if self.client:
                try:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                    )
                    strategy_code = self.extract_python_code(response.text)
                except Exception as e:
                    logger.error(f"Gemini API Error: {e}")
                    feedback = f"API Error: {e}"
                    continue
            else:
                # Fallback to mock if API key isn't set
                strategy_code = """
def generate_signals(df):
    import ta
    import numpy as np
    df['sma_10'] = ta.trend.sma_indicator(df['close'], window=10)
    df['sma_30'] = ta.trend.sma_indicator(df['close'], window=30)
    df['signal'] = np.where(df['sma_10'] > df['sma_30'], 1, -1)
    df['signal'] = df['signal'].fillna(0)
    return df
"""

            # 5. Execute Code in Sandbox
            local_scope = {}
            try:
                exec(strategy_code, globals(), local_scope)
                generate_signals_func = local_scope['generate_signals']
                df_signaled = generate_signals_func(df.copy())
            except Exception as e:
                logger.error(f"Generated code failed to execute: {e}")
                feedback = f"Syntax or Execution Error: {e}"
                continue
                
            # 6. Backtest
            results = run_backtest(df_signaled)
            logger.info(f"Attempt {attempt + 1} Metrics: {results.to_dict()}")
            
            # 7. Evaluate
            status = "PROMOTED" if results.sharpe_ratio > 1.0 and results.total_return > 0 else "REJECTED"
            reason = "Metrics below threshold" if status == "REJECTED" else "Passed"
            
            MemoryManager.save_strategy_evaluation(
                experiment_id=exp_id,
                name=f"Evolved_Strategy_{attempt}",
                code=strategy_code,
                metrics=results.to_dict(),
                status=status,
                failure_reason=reason
            )
            
            if status == "PROMOTED":
                logger.info(f"SUCCESS! Found profitable strategy on attempt {attempt+1}")
                return True
                
            # If rejected, feed it back
            feedback = f"Code ran but yielded Return: {results.total_return:.2%}, Sharpe: {results.sharpe_ratio:.2f}. Failed requirement of Sharpe > 1.0. Try a different approach."
            
        logger.warning(f"Failed to find profitable strategy after {max_retries} attempts.")
        return False
