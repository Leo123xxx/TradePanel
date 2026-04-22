import MetaTrader5 as mt5
import os
from dotenv import load_dotenv

load_dotenv()

def test_mt5():
    if not mt5.initialize():
        print(f"FAILED: mt5.initialize() failed, error code: {mt5.last_error()}")
        return
    
    login = int(os.getenv("MT5_LOGIN"))
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    
    print(f"Connecting to {server}...")
    authorized = mt5.login(login, password=password, server=server)
    
    if authorized:
        print("SUCCESS: Authorized.")
        print(f"Account Info: {mt5.account_info()}")
    else:
        print(f"FAILED: Authorization failed, error code: {mt5.last_error()}")
    
    mt5.shutdown()

if __name__ == "__main__":
    test_mt5()
