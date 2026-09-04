import uuid
from datetime import datetime
from sqlalchemy.future import select
from app.db.session import StateSessionLocal, MemorySessionLocal, state_engine, Base
from app.db.models_state import PortfolioState, Trade, ApprovalRequest
from app.db.models_memory import Strategy
from app.core.logger import logger

class PaperTradingEngine:
    def __init__(self):
        self.initial_capital = 1000000.0 # 10 Lakh INR

    async def initialize(self):
        # Base.metadata.create_all is sync, so we need to run it in a sync engine or use run_sync
        async with state_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await self._ensure_state_initialized()

    async def _ensure_state_initialized(self):
        async with StateSessionLocal() as db:
            result = await db.execute(select(PortfolioState).limit(1))
            state = result.scalars().first()
            if not state:
                state = PortfolioState(
                    virtual_capital=self.initial_capital,
                    current_portfolio_value=self.initial_capital,
                    active_positions={}
                )
                db.add(state)
                await db.commit()

    async def get_portfolio_status(self):
        async with StateSessionLocal() as db:
            # Fetch portfolio state
            result = await db.execute(select(PortfolioState).limit(1))
            state = result.scalars().first()
            
            # Fetch trades
            if state:
                trades_result = await db.execute(
                    select(Trade).where(Trade.portfolio_id == state.id).order_by(Trade.timestamp.desc())
                )
                trades = trades_result.scalars().all()
                trade_history = [{
                    "id": t.id,
                    "symbol": t.symbol,
                    "side": t.side,
                    "qty": t.qty,
                    "price": t.price,
                    "timestamp": t.timestamp.isoformat() if t.timestamp else None
                } for t in trades]
            else:
                trade_history = []
                
            if not state:
                return {}
                
            return {
                "virtual_capital": state.virtual_capital,
                "portfolio_value": state.current_portfolio_value,
                "positions": state.active_positions,
                "history": trade_history
            }

    async def execute_mock_trade(self, symbol: str, side: str, qty: int, price: float):
        """
        Executes a mock trade and updates the state atomically.
        """
        async with StateSessionLocal() as db:
            try:
                # Lock the row for update to prevent concurrent race conditions
                result = await db.execute(select(PortfolioState).with_for_update().limit(1))
                state = result.scalars().first()
                if not state:
                    return False
                    
                cost = qty * price
                
                if side == "BUY":
                    if state.virtual_capital < cost:
                        logger.warning(f"Insufficient virtual capital for BUY {qty} {symbol} @ {price}")
                        return False
                    
                    # Update Capital
                    state.virtual_capital -= cost
                    
                    # Update Positions
                    pos = dict(state.active_positions)
                    if symbol in pos:
                        old_qty = pos[symbol]['qty']
                        old_price = pos[symbol]['avg_price']
                        new_qty = old_qty + qty
                        pos[symbol] = {
                            'qty': new_qty, 
                            'avg_price': ((old_qty * old_price) + cost) / new_qty
                        }
                    else:
                        pos[symbol] = {'qty': qty, 'avg_price': price}
                    
                    state.active_positions = pos
                    
                elif side == "SELL":
                    pos = dict(state.active_positions)
                    if symbol not in pos or pos[symbol]['qty'] < qty:
                        logger.warning(f"Insufficient position for SELL {qty} {symbol}")
                        return False
                        
                    # Realize PnL and Update Capital
                    avg_price = pos[symbol]['avg_price']
                    state.virtual_capital += cost
                    
                    # Update Position
                    pos[symbol]['qty'] -= qty
                    if pos[symbol]['qty'] == 0:
                        del pos[symbol]
                    state.active_positions = pos
                
                # Log Trade relationally
                trade = Trade(
                    id=str(uuid.uuid4()),
                    portfolio_id=state.id,
                    symbol=symbol,
                    side=side,
                    qty=qty,
                    price=price
                )
                db.add(trade)
                
                # Update Total Value
                total_pos_value = sum(p['qty'] * p['avg_price'] for p in state.active_positions.values())
                state.current_portfolio_value = state.virtual_capital + total_pos_value
                
                await db.commit()
                logger.info(f"Executed MOCK TRADE: {side} {qty} {symbol} @ {price}")
                return True
            except Exception as e:
                await db.rollback()
                logger.error(f"Paper trade failed: {e}")
                return False
