import psycopg2
import MetaTrader5
import os
from dotenv import load_dotenv

load_dotenv()

def verify():
    # DB Check
    try:
        db_conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5433),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print(f"DB Connected: Success (Port {os.getenv('DB_PORT')})")
        db_conn.close()
    except Exception as e:
        print(f"DB Connection Failed: {e}")

    # MT5 Check
    try:
        mt5_init = MetaTrader5.initialize()
        if mt5_init:
            print("MT5 Initialized: Success")
            account = MetaTrader5.account_info()
            if account:
                print(f"MT5 Account Account: {account.login}")
            else:
                print("MT5 Account Info: Failure (Is MT5 logged in?)")
            MetaTrader5.shutdown()
        else:
            print(f"MT5 Initialization Failed: {MetaTrader5.last_error()}")
    except Exception as e:
        print(f"MT5 Error: {e}")

if __name__ == "__main__":
    verify()
