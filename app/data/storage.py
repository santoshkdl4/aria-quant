import os
import pandas as pd
from pathlib import Path
from app.core.config import settings, PROJECT_ROOT

def get_parquet_path(symbol: str, timeframe: str) -> Path:
    # Ensure safe filename
    safe_symbol = symbol.replace("^", "").replace(".", "_")
    base_dir = PROJECT_ROOT / settings.MARKET_DATA_PATH
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{safe_symbol}_{timeframe}.parquet"

def save_to_parquet(df: pd.DataFrame, symbol: str, timeframe: str):
    """
    Saves a normalized pandas DataFrame to a parquet file.
    Expected schema: timestamp, open, high, low, close, volume, open_interest, symbol
    """
    if df.empty:
        return
        
    path = get_parquet_path(symbol, timeframe)
    
    # Ensure standard columns
    if 'symbol' not in df.columns:
        df['symbol'] = symbol
        
    if 'open_interest' not in df.columns:
        df['open_interest'] = 0.0

    # Ensure timestamp is the index or a column
    if df.index.name == 'timestamp':
        df = df.reset_index()
    elif 'Date' in df.columns:
        df = df.rename(columns={'Date': 'timestamp'})
    elif 'Datetime' in df.columns:
        df = df.rename(columns={'Datetime': 'timestamp'})
        
    # Convert column names to lowercase for consistency
    df.columns = [c.lower() for c in df.columns]
        
    # Reorder columns to match standard schema
    cols = ['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
    # Keep only these columns if they exist, fill missing with 0 or NaN
    for col in cols:
        if col not in df.columns:
            if col == 'open_interest':
                df[col] = 0.0
            else:
                df[col] = float('nan')
                
    df = df[cols]
    
    # Save to parquet
    df.to_parquet(str(path), engine='pyarrow', compression='snappy', index=False)
