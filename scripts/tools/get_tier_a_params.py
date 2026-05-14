
import sys
import os
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.db_client import DBClient

def get_params_for_winners():
    db = DBClient()
    winners = [
        ('bb_squeeze_scalp', 'USDJPY', 'M15'),
        ('ema_ribbon_trend', 'AAPL', 'H4'),
        ('ema_ribbon_trend', 'USTEC', 'H4'),
        ('ema_ribbon_trend', 'US500', 'H4'),
        ('vwap_momentum', 'US500', 'M15'),
        ('ma_crossover', 'USDJPY', 'H4'),
        ('ma_crossover', 'GBPUSD', 'H4'),
    ]
    
    results = {}
    for strat, symbol, tf in winners:
        query = """
        SELECT w.best_params, w.window_index, s.name, w.symbol, w.timeframe
        FROM walk_forward_results w 
        JOIN strategies s ON w.strategy_id = s.strategy_id 
        WHERE s.name ILIKE %s
          AND w.symbol = %s
          AND w.timeframe = %s
        ORDER BY w.window_index DESC
        LIMIT 1;
        """
        rows = db.execute_query(query, (f"%{strat}%", symbol, tf))
        if rows:
            results[f"{strat}_{symbol}_{tf}"] = rows[0][0]
        else:
            # Try finding the best from a simple backtest if WFO is missing
            print(f"No WFO for {strat} {symbol} {tf}, checking latest backtest results...")
            
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    get_params_for_winners()
