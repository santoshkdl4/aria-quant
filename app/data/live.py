import asyncio
import yfinance as yf
from app.core.logger import logger
from app.api.ws import manager

class LiveDataFeed:
    def __init__(self, symbols=None):
        self.symbols = symbols or ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
        self._running = False
        
    async def start(self):
        self._running = True
        logger.info(f"Starting LiveDataFeed for symbols: {self.symbols}")
        asyncio.create_task(self._poll_loop())
        
    async def stop(self):
        self._running = False
        logger.info("Stopping LiveDataFeed")
        
    async def _poll_loop(self):
        while self._running:
            try:
                # Use yfinance to download latest 1m data for the symbols
                # We use .NS for Indian stocks on Yahoo Finance
                tickers = yf.Tickers(" ".join(self.symbols))
                live_prices = {}
                
                for symbol in self.symbols:
                    try:
                        info = tickers.tickers[symbol].info
                        price = info.get('currentPrice') or info.get('regularMarketPrice')
                        if price:
                            # Strip .NS for our internal tracking
                            clean_symbol = symbol.replace(".NS", "")
                            live_prices[clean_symbol] = price
                    except Exception as e:
                        logger.warning(f"Failed to fetch live price for {symbol}: {e}")
                
                if live_prices:
                    await manager.broadcast({
                        "type": "live_prices",
                        "prices": live_prices
                    })
                    
            except Exception as e:
                logger.error(f"Live data polling failed: {e}")
                
            # Poll every 10 seconds to avoid rate limits
            await asyncio.sleep(10)

live_feed = LiveDataFeed()
