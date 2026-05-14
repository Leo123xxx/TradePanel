
import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.db_client import DBClient

def get_latest_wfo_params():
    db = DBClient()
    
    # Get strategy_id for rsi_pullback
    # Based on the code, it uses the strategy.name which is "RSI Pullback"
    # But let's find it by looking for it.
    
    query = """
    SELECT w.best_params, w.window_index, s.name, w.symbol, w.timeframe
    FROM walk_forward_results w
    JOIN strategies s ON w.strategy_id = s.strategy_id
    WHERE s.name = 'rsi_pullback'
    ORDER BY w.window_index DESC, w.symbol, w.timeframe
    LIMIT 10;
    """
    
    rows = db.execute_query(query)
    if not rows:
        print("No WFO results found for rsi_pullback")
        return
    
    for row in rows:
        best_params, window_index, strategy_name, symbol, timeframe = row
        print(f"Result for {strategy_name} ({symbol} {timeframe}):")
        print(f"Window Index: {window_index}")
        print(f"Best Params: {best_params}")
        print("-" * 20)

if __name__ == "__main__":
    get_latest_wfo_params()
