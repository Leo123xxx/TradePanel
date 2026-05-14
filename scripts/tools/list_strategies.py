
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.db_client import DBClient

def list_strategies():
    db = DBClient()
    rows = db.execute_query("SELECT strategy_id, name FROM strategies;")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}")

if __name__ == "__main__":
    list_strategies()
