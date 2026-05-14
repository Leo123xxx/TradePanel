import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.db_client import DBClient

def run_migration():
    db = DBClient()
    sql_file = os.path.join(os.path.dirname(__file__), "20240512_add_account_metrics.sql")
    
    with open(sql_file, 'r') as f:
        sql = f.read()
    
    print(f"Applying migration from {sql_file}...")
    try:
        # DBClient.execute_query might not support multiple statements if it uses a simple cursor.execute
        # So we split by semicolon
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for stmt in statements:
            db.execute_query(stmt)
        print("Migration applied successfully.")
    except Exception as e:
        print(f"Error applying migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
