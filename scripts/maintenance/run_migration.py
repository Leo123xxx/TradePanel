"""
run_migration.py
----------------
Runs a SQL migration file against the trading_platform database using
the project's existing connection settings (reads from .env automatically).

Usage:
    python scripts/run_migration.py
    python scripts/run_migration.py --file scripts/migrate_backtest_runs.sql
"""

import os
import sys
import argparse
from pathlib import Path

# Make sure project root is on the path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
import psycopg2

load_dotenv()

DEFAULT_SQL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "migrate_backtest_runs.sql"
)


def run(sql_file: str):
    conn_params = {
        "host":     os.getenv("DB_HOST", "127.0.0.1"),
        "port":     os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "trading_platform"),
        "user":     os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
        "connect_timeout": 5,
    }

    print(f"\nConnecting to PostgreSQL at {conn_params['host']}:{conn_params['port']} "
          f"/ {conn_params['database']} as {conn_params['user']} ...")

    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True          # DDL statements need autocommit
    except Exception as e:
        print(f"\n  ERROR: Could not connect to database.\n  {e}")
        print("\n  Check your .env file has DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD set.")
        sys.exit(1)

    with open(sql_file, "r") as f:
        sql = f.read()

    print(f"  Running: {sql_file}\n")

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        print("  Migration applied successfully.\n")
    except Exception as e:
        print(f"\n  ERROR during migration:\n  {e}")
        conn.close()
        sys.exit(1)

    # Verify the table was created
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM backtest_runs;")
            count = cur.fetchone()[0]
        print(f"  backtest_runs table ready — {count} row(s) seeded.\n")
    except Exception as e:
        print(f"  Warning: could not verify table: {e}")

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a SQL migration file")
    parser.add_argument("--file", default=DEFAULT_SQL, help="Path to .sql file")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: SQL file not found: {args.file}")
        sys.exit(1)

    run(args.file)
