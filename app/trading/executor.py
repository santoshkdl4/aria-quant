import uuid
from datetime import datetime
from app.db.session import StateSessionLocal, MemorySessionLocal, state_engine, Base
from app.db.models_state import PortfolioState, ApprovalRequest
from app.db.models_memory import Strategy
from app.core.logger import logger

class PaperTradingEngine:
    def __init__(self):
        self.initial_capital = 1000000.0 # 10 Lakh INR
        Base.metadata.create_all(bind=state_engine)
        self._ensure_state_initialized()

    def _ensure_state_initialized(self):
        db = StateSessionLocal()
        try:
            state = db.query(PortfolioState).first()
            if not state:
                state = PortfolioState(
                    virtual_capital=self.initial_capital,
                    current_portfolio_value=self.initial_capital,
                    active_positions={},
                    trade_history=[]
                )
                db.add(state)
                db.commit()
        finally:
            db.close()

    def get_portfolio_status(self):
        db = StateSessionLocal()
        try:
            state = db.query(PortfolioState).first()
            return {
                "virtual_capital": state.virtual_capital,
                "portfolio_value": state.current_portfolio_value,
                "positions": state.active_positions,
                "history": state.trade_history
            }
        finally:
            db.close()

    def execute_mock_trade(self, symbol: str, side: str, qty: int, price: float):
        """
        Executes a mock trade and updates the state.
        Side: 'BUY' or 'SELL'
        """
        db = StateSessionLocal()
        try:
            state = db.query(PortfolioState).first()
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
                    # Very simple average price calculation
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
                realized_pnl = (price - avg_price) * qty
                state.virtual_capital += (cost) # Get cash back
                
                # Update Position
                pos[symbol]['qty'] -= qty
                if pos[symbol]['qty'] == 0:
                    del pos[symbol]
                state.active_positions = pos
            
            # Log Trade
            history = list(state.trade_history)
            trade = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "price": price
            }
            history.append(trade)
            state.trade_history = history
            
            # Update Total Value (simplified: just cash + (active pos * current price))
            # In a real engine, we'd fetch live prices. Here we assume price = current.
            total_pos_value = sum(p['qty'] * p['avg_price'] for p in state.active_positions.values())
            state.current_portfolio_value = state.virtual_capital + total_pos_value
            
            db.commit()
            logger.info(f"Executed MOCK TRADE: {side} {qty} {symbol} @ {price}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Paper trade failed: {e}")
            return False
        finally:
            db.close()
