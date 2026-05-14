import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

from data.db_client import DBClient

def main():
    db = DBClient()
    
    def print_rows(title, query):
        print(f"\n=== {title} ===")
        # Get columns if possible (not supported by DBClient.execute_query directly, but we can try)
        # DBClient.execute_query usually returns a list of tuples.
        rows = db.execute_query(query)
        if rows:
            for row in rows:
                print(row)
        else:
            print("No data found.")

    print_rows("Recent bot_health events", "SELECT * FROM bot_health ORDER BY timestamp DESC LIMIT 10;")
    
    print_rows("Recent signals (last 24h)", 
               "SELECT s.timestamp, st.name, s.pair, s.direction, s.timeframe, s.triggered_trade_id "
               "FROM signals s JOIN strategies st ON s.strategy_id = st.strategy_id "
               "WHERE s.timestamp > NOW() - INTERVAL '24 hours' "
               "ORDER BY s.timestamp DESC LIMIT 20;")

    print_rows("Recent trades (last 24h)", 
               "SELECT t.open_time, st.name, t.pair, t.direction, t.lot_size, t.status, t.mt5_ticket "
               "FROM trades t JOIN strategies st ON t.strategy_id = st.strategy_id "
               "WHERE t.open_time > NOW() - INTERVAL '24 hours' "
               "ORDER BY t.open_time DESC LIMIT 20;")

    print_rows("Latest Regime", "SELECT * FROM regime_log ORDER BY timestamp DESC LIMIT 5;")


if __name__ == "__main__":
    main()
