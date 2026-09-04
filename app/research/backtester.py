import pandas as pd
import numpy as np

class BacktestResult:
    def __init__(self, total_return, win_rate, max_drawdown, sharpe_ratio, trades_count):
        self.total_return = total_return
        self.win_rate = win_rate
        self.max_drawdown = max_drawdown
        self.sharpe_ratio = sharpe_ratio
        self.trades_count = trades_count
        
    def to_dict(self):
        return {
            "total_return": self.total_return,
            "win_rate": self.win_rate,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "trades_count": self.trades_count
        }

def run_backtest(df: pd.DataFrame, signal_col: str = 'signal', fee: float = 0.001) -> BacktestResult:
    """
    Runs a vectorized backtest on a DataFrame containing price data and a signal column.
    Signal should be 1 (Long), -1 (Short), or 0 (Neutral).
    Applies a standard fee (default 0.1%) on every position change.
    """
    if signal_col not in df.columns:
        raise ValueError(f"Column '{signal_col}' not found in DataFrame")
        
    df = df.copy()
    
    # Calculate daily returns
    df['returns'] = df['close'].pct_change()
    
    # Shift signal by 1 day to simulate buying at the next day's open
    # We use close-to-close returns here for simplicity, assuming execution at close.
    df['strategy_returns'] = df['returns'] * df[signal_col].shift(1)
    
    # Apply Transaction Costs
    df['position_change'] = df[signal_col].diff().abs()
    df['transaction_cost'] = df['position_change'] * fee
    # Fill NA for the first day to 0
    df['transaction_cost'] = df['transaction_cost'].fillna(0.0)
    df['strategy_returns'] = df['strategy_returns'] - df['transaction_cost']
    
    # Drop NAs
    df = df.dropna(subset=['strategy_returns'])
    
    if len(df) == 0:
        return BacktestResult(0.0, 0.0, 0.0, 0.0, 0)
        
    # Calculate metrics
    total_return = (1 + df['strategy_returns']).prod() - 1
    
    # Sharpe Ratio (Assuming 252 trading days, 0% risk free rate)
    mean_ret = df['strategy_returns'].mean()
    std_ret = df['strategy_returns'].std()
    sharpe_ratio = (mean_ret / std_ret) * np.sqrt(252) if std_ret > 0 else 0.0
    
    # Max Drawdown
    cumulative_returns = (1 + df['strategy_returns']).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    
    # Win Rate
    winning_days = len(df[df['strategy_returns'] > 0])
    losing_days = len(df[df['strategy_returns'] < 0])
    trades_count = winning_days + losing_days
    win_rate = winning_days / trades_count if trades_count > 0 else 0.0
    
    return BacktestResult(
        total_return=float(total_return),
        win_rate=float(win_rate),
        max_drawdown=float(max_drawdown),
        sharpe_ratio=float(sharpe_ratio),
        trades_count=trades_count
    )
