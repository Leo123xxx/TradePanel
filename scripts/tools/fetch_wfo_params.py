import sys
import os
sys.path.insert(0, os.getcwd())
from data.db_client import DBClient
import json

def fetch_params():
    db = DBClient()
    # Query for the latest window results for all strategies
    query = """
        WITH latest_windows AS (
            SELECT strategy_id, symbol, timeframe, MAX(window_index) as max_window
            FROM walk_forward_results
            GROUP BY strategy_id, symbol, timeframe
        )
        SELECT s.name, w.symbol, w.timeframe, w.best_params, w.oos_sharpe, w.oos_win_rate
        FROM walk_forward_results w
        JOIN strategies s ON w.strategy_id = s.strategy_id
        JOIN latest_windows lw ON w.strategy_id = lw.strategy_id 
            AND w.symbol = lw.symbol 
            AND w.timeframe = lw.timeframe 
            AND w.window_index = lw.max_window
        WHERE w.oos_sharpe > 1.5
        ORDER BY w.oos_sharpe DESC
    """
    rows = db.execute_query(query)
    print(json.dumps(rows, indent=2, default=str))

if __name__ == "__main__":
    fetch_params()
