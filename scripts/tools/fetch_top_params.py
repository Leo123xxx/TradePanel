import sys
import os
sys.path.insert(0, os.getcwd())
from data.db_client import DBClient
import json

def fetch_params():
    db = DBClient()
    targets = [
        ('rsi_pullback', 'EURUSD', 'H4'),
        ('dual_ema_fractal', 'XAUUSD', 'H4'),
        ('gold_momentum_breakout', 'XAUUSD', 'H4'),
        ('supertrend', 'EURUSD', 'H4'),
        ('Dual_EMA_Fractal', 'XAUUSD', 'H4'),
        ('SuperTrend', 'EURUSD', 'H4'),
        ('Gold_Momentum_Breakout', 'XAUUSD', 'H4'),
        ('RSI_Pullback', 'EURUSD', 'H4')
    ]
    
    results = {}
    for name, symbol, tf in targets:
        query = """
            SELECT s.name, w.best_params, w.oos_sharpe
            FROM walk_forward_results w
            JOIN strategies s ON w.strategy_id = s.strategy_id
            WHERE s.name = %s AND w.symbol = %s AND w.timeframe = %s AND w.window_index = 5
        """
        rows = db.execute_query(query, (name, symbol, tf))
        if rows:
            results[f"{name}_{symbol}_{tf}"] = rows[0]
            
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    fetch_params()
