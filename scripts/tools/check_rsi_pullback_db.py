
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.db_client import DBClient

def check_rsi_pullback():
    db = DBClient()
    rows = db.execute_query("""
        SELECT s.name, w.symbol, w.timeframe, w.window_index, w.best_params 
        FROM walk_forward_results w 
        JOIN strategies s ON w.strategy_id = s.strategy_id 
        WHERE s.name ILIKE '%rsi_pullback%'
        ORDER BY w.window_index DESC;
    """)
    if not rows:
        print("No rsi_pullback results found")
        # Try finding any strategy with 'rsi' in the name
        rows = db.execute_query("SELECT DISTINCT name FROM strategies WHERE name ILIKE '%rsi%';")
        print(f"Found RSI strategies: {rows}")
        return

    for row in rows:
        print(f"Strategy: {row[0]}, Pair: {row[1]}, TF: {row[2]}, Window: {row[3]}")
        print(f"Params: {row[4]}")
        print("-" * 20)

if __name__ == "__main__":
    check_rsi_pullback()
