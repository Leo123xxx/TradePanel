import os
import sys
import subprocess
from datetime import datetime

def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def check_dependencies():
    print_header("CHECKING DEPENDENCIES")
    try:
        import MetaTrader5 as mt5
        print(f"✅ MT5 Library: {mt5.__version__}")
    except ImportError:
        print("❌ MT5 Library missing. Run: pip install MetaTrader5")
        return False

    try:
        import pandas as pd
        print(f"✅ Pandas: {pd.__version__}")
    except ImportError:
        print("❌ Pandas missing. Run: pip install pandas")
        return False
    
    return True

def init_db():
    print_header("INITIALIZING DATABASE")
    try:
        # Assuming scripts/setup_db.py exists and handles schema creation
        result = subprocess.run([sys.executable, "scripts/setup_db.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database schema initialized/verified.")
            return True
        else:
            print(f"❌ Database initialization failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running setup_db.py: {e}")
        return False

def check_mt5_connectivity():
    print_header("CHECKING MT5 CONNECTIVITY")
    import MetaTrader5 as mt5
    if not mt5.initialize():
        print(f"❌ MT5 Initialization failed: {mt5.last_error()}")
        return False
    
    account_info = mt5.account_info()
    if account_info:
        print(f"✅ Connected to Account: {account_info.login} ({account_info.company})")
        print(f"✅ Balance: {account_info.balance} {account_info.currency}")
    else:
        print("❌ Could not retrieve account info. Check MT5 login.")
        mt5.shutdown()
        return False
    
    mt5.shutdown()
    return True

def ingest_initial_data():
    print_header("INGESTING INITIAL DATA (XAUUSD)")
    try:
        # Pull 1000 bars of H4-D1 to verify data feed
        result = subprocess.run([sys.executable, "scripts/pull_all_data.py", "XAUUSD"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Initial data feed (XAUUSD) successful.")
            return True
        else:
            print(f"❌ Data ingestion failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running pull_all_data.py: {e}")
        return False

def main():
    print_header("TRADEPANEL UNIFIED SETUP")
    
    if not check_dependencies():
        sys.exit(1)
    
    if not init_db():
        print("⚠️ Warning: DB setup failed. Check your .env file.")
    
    if not check_mt5_connectivity():
        print("⚠️ Warning: MT5 connectivity issue. Ensure MT5 is running.")
    
    if not ingest_initial_data():
         print("⚠️ Warning: Initial data ingestion failed.")

    print_header("SETUP COMPLETE")
    print("Application is ready for backtesting and optimization.")
    print("Run 'python scripts/run_backtest.py --strategy range_breakout' to start.")

if __name__ == "__main__":
    main()
