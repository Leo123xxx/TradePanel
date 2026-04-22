import os
import psycopg2
from dotenv import load_dotenv
import MetaTrader5 as mt5

def check_postgres():
    load_dotenv()
    print("--- PostgreSQL Check ---")
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        print("SUCCESS: Connected to PostgreSQL container.")
        conn.close()
    except Exception as e:
        print(f"FAILED: Could not connect to PostgreSQL. Error: {e}")

def check_mt5():
    print("\n--- MT5 Check ---")
    if mt5.initialize():
        print("SUCCESS: MT5 terminal initiated.")
        # Print account info if already logged in
        account_info = mt5.account_info()
        if account_info:
            print(f"Logged into Account: {account_info.login}")
            print(f"Server: {account_info.server}")
        else:
            print("INFO: MT5 initialized but not logged into an account yet.")
        mt5.shutdown()
    else:
        print(f"FAILED: MT5 initialization failed. Error code: {mt5.last_error()}")

if __name__ == "__main__":
    check_postgres()
    check_mt5()
