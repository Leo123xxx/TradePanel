
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.db_client import DBClient

def get_xau_params():
    db = DBClient()
    query = """
    SELECT w.best_params, w.window_index, s.name, w.symbol, w.timeframe
    FROM walk_forward_results w 
    JOIN strategies s ON w.strategy_id = s.strategy_id 
    WHERE s.name ILIKE '%rsi_pullback%'
      AND w.symbol = 'XAUUSD'
      AND w.timeframe = 'H4'
      AND w.window_index = 5
    LIMIT 1;
    """
    rows = db.execute_query(query)
    if rows:
        print(f"WFO Best Params for rsi_pullback XAUUSD H4 Window 5: {rows[0][0]}")

if __name__ == "__main__":
    get_xau_params()
