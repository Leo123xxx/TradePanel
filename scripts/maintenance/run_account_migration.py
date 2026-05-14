"""
run_account_migration.py
Applies migrate_account_profiles.sql via psycopg2.
Usage: python scripts/run_account_migration.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

def main():
    sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrate_account_profiles.sql")
    with open(sql_path, "r") as f:
        sql = f.read()

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 5433)),
        dbname=os.getenv("DB_NAME", "trading_platform"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
    conn.autocommit = False
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print("Migration applied successfully.")
        cur.execute("SELECT account_id, account_name, account_type FROM account_profiles ORDER BY account_id")
        for row in cur.fetchall():
            print(f"  {row[0]:3d}  {row[1]:<30}  {row[2]}")
    except Exception as e:
        conn.rollback()
        print(f"Migration FAILED: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
