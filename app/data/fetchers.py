import yfinance as yf
import pandas as pd
from typing import Optional
from app.core.logger import logger
from app.data.storage import save_to_parquet

class DataFetcher:
    def fetch_historical(self, symbol: str, timeframe: str, start: str, end: Optional[str] = None):
        raise NotImplementedError

class YFinanceFetcher(DataFetcher):
    def fetch_historical(self, symbol: str, timeframe: str, start: str, end: Optional[str] = None):
        logger.info(f"Fetching {symbol} from yfinance (timeframe: {timeframe}, start: {start})")
        # yfinance timeframe mapping
        yf_interval = "1d"
        if timeframe == "1m": yf_interval = "1m"
        elif timeframe == "5m": yf_interval = "5m"
        elif timeframe == "15m": yf_interval = "15m"
        elif timeframe == "1h": yf_interval = "1h"
        
        ticker = yf.Ticker(symbol)
        try:
            if end:
                df = ticker.history(interval=yf_interval, start=start, end=end)
            else:
                df = ticker.history(interval=yf_interval, start=start)
                
            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                return False
                
            # yfinance returns index as Date or Datetime
            df.index.name = 'timestamp'
            
            # Save via standard storage mechanism
            save_to_parquet(df, symbol, timeframe)
            logger.info(f"Successfully saved {len(df)} rows for {symbol}")
            return True
        except Exception as e:
            logger.error(f"Failed to fetch {symbol}: {e}")
            return False
