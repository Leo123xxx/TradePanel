
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.db_client import DBClient

def check_table():
    db = DBClient()
    count = db.execute_query("SELECT COUNT(*) FROM walk_forward_results;")[0][0]
    print(f"Total rows in walk_forward_results: {count}")
    
    if count > 0:
        rows = db.execute_query("""
            SELECT s.name, w.symbol, w.timeframe, w.window_index 
            FROM walk_forward_results w 
            JOIN strategies s ON w.strategy_id = s.strategy_id 
            LIMIT 5;
        """)
        for row in rows:
            print(row)

if __name__ == "__main__":
    check_table()
