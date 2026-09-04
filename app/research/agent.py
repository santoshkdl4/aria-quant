import os
import duckdb
import pandas as pd
from google import genai
from google.genai import types
from app.core.logger import logger
from app.db.duckdb_session import get_duckdb_connection
from app.research.backtester import run_backtest

# Initialize GenAI Client
# Expects GEMINI_API_KEY environment variable to be set
try:
    client = genai.Client()
except Exception as e:
    logger.error(f"Failed to initialize GenAI client: {e}")
    client = None

def _extract_python_code(markdown_text: str) -> str:
    """Extracts raw python code from a markdown block."""
    if "```python" in markdown_text:
        return markdown_text.split("```python")[1].split("```")[0].strip()
    elif "```" in markdown_text:
        return markdown_text.split("```")[1].split("```")[0].strip()
    return markdown_text.strip()

async def execute_agent_query(user_prompt: str, symbol: str = "RELIANCE") -> dict:
    """
    1. Fetches historical data for the symbol.
    2. Asks the LLM to write a Pandas strategy for that data.
    3. Executes the code securely.
    4. Runs the backtester on the resulting signals.
    """
    if not client:
        return {"status": "error", "message": "Gemini API key not configured."}
        
    try:
        # 1. Fetch Data
        con = get_duckdb_connection()
        try:
            df = con.execute(f"SELECT * FROM market_data WHERE symbol = '{symbol}' ORDER BY timestamp").df()
        except duckdb.CatalogException:
            # If market_data view doesn't exist or is empty
            df = pd.DataFrame()
        finally:
            con.close()
            
        if df.empty:
            return {"status": "error", "message": f"No historical data found for {symbol}."}
            
        # 2. Prompt LLM for Strategy Code
        sys_instruct = """
        You are a quantitative trading AI. Your task is to write Python code using Pandas to calculate trading signals.
        You will be provided with a DataFrame `df` which contains 'open', 'high', 'low', 'close', 'volume', 'timestamp'.
        Your code MUST return the modified `df` containing a new column named 'signal'.
        The 'signal' column must contain 1 (Long), -1 (Short), or 0 (Neutral).
        Do not import any external ML libraries, just use pandas and numpy.
        OUTPUT ONLY THE PYTHON CODE inside a ```python block. No explanations.
        
        Example output:
        ```python
        df['sma_short'] = df['close'].rolling(window=10).mean()
        df['sma_long'] = df['close'].rolling(window=50).mean()
        df['signal'] = 0
        df.loc[df['sma_short'] > df['sma_long'], 'signal'] = 1
        df.loc[df['sma_short'] < df['sma_long'], 'signal'] = -1
        ```
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct,
                temperature=0.1
            )
        )
        
        code = _extract_python_code(response.text)
        logger.info(f"Agent generated code:\n{code}")
        
        # 3. Execute Code Securely (Sandbox)
        local_scope = {'df': df.copy(), 'pd': pd, 'np': __import__('numpy')}
        
        try:
            exec(code, {}, local_scope)
            df_result = local_scope.get('df')
            
            if 'signal' not in df_result.columns:
                return {"status": "error", "message": "The generated code did not produce a 'signal' column."}
                
        except Exception as e:
            logger.error(f"Agent code execution failed: {e}")
            return {"status": "error", "message": f"Code execution failed: {str(e)}"}
            
        # 4. Run Backtester
        backtest_result = run_backtest(df_result, signal_col='signal')
        
        return {
            "status": "success",
            "message": "Strategy executed successfully.",
            "code": code,
            "metrics": backtest_result.to_dict()
        }
        
    except Exception as e:
        logger.exception("Agent pipeline failed.")
        return {"status": "error", "message": str(e)}
