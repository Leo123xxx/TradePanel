
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.db_client import DBClient

def get_winning_params():
    db = DBClient()
    # Query for the latest window 5 result for rsi_pullback on EURUSD H4
    query = """
    SELECT s.name, w.symbol, w.timeframe, w.window_index, w.best_params, w.oos_end
    FROM walk_forward_results w 
    JOIN strategies s ON w.strategy_id = s.strategy_id 
    WHERE s.name ILIKE '%rsi_pullback%'
      AND w.symbol = 'EURUSD'
      AND w.timeframe = 'H4'
      AND w.window_index = 5
    ORDER BY w.oos_end DESC
    LIMIT 1;
    """
    rows = db.execute_query(query)
    if not rows:
        print("No rsi_pullback EURUSD H4 Window 5 results found")
        return

    name, symbol, tf, win, params, oos_end = rows[0]
    print(f"Latest WFO Winning Params for {name} ({symbol} {tf}):")
    print(f"OOS End Date: {oos_end}")
    print(f"Params: {params}")

if __name__ == "__main__":
    get_winning_params()
