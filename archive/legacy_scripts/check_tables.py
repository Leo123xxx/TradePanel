import sys
import os
from pathlib import Path

# Set repo root explicitly
REPO_ROOT = r"f:\REPOS\leo123xxx\TradePanel"
sys.path.insert(0, REPO_ROOT)

from data.db_client import DBClient

def main():
    db = DBClient()
    res = db.execute_query("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    print(res)

if __name__ == "__main__":
    main()
