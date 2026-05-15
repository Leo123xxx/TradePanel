import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from data.db_client import DBClient

def setup_wf_db():
    db = DBClient()
    query = """
    CREATE TABLE IF NOT EXISTS walk_forward_results (
        id              SERIAL PRIMARY KEY,
        strategy_id     INTEGER REFERENCES strategies(strategy_id),
        symbol          VARCHAR(20),
        timeframe       VARCHAR(10),
        window_index    INTEGER,
        is_start        TIMESTAMP,
        is_end          TIMESTAMP,
        oos_start       TIMESTAMP,
        oos_end         TIMESTAMP,
        best_params     JSONB,
        oos_sharpe      FLOAT,
        oos_profit_factor FLOAT,
        oos_trades      INTEGER,
        created_at      TIMESTAMP DEFAULT NOW()
    );
    """
    print("Creating walk_forward_results table...")
    db.execute_query(query)
    print("Table created successfully.")

if __name__ == "__main__":
    setup_wf_db()
