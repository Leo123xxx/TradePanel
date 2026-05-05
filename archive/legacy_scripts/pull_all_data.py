import MetaTrader5 as mt5
from mt5_bridge.connector import MT5Connector
from mt5_bridge.data_feed import MT5DataFeed
import sys

def main():
    symbol = "XAUUSD"
    if len(sys.argv) > 1:
        symbol = sys.argv[1]

    # Map of all reusable timeframes we want to log
    timeframes = [
        (mt5.TIMEFRAME_M1, 50000),   # 1 Minute
        (mt5.TIMEFRAME_M5, 20000),   # 5 Minutes
        (mt5.TIMEFRAME_M15, 10000),  # 15 Minutes
        (mt5.TIMEFRAME_H1, 5000),    # 1 Hour
        (mt5.TIMEFRAME_H4, 2000),    # 4 Hours
        (mt5.TIMEFRAME_D1, 1000),    # Daily
        (mt5.TIMEFRAME_W1, 500)      # Weekly
    ]

    print(f"========================================")
    print(f" STARTING FULL DATA PULL FOR {symbol}")
    print(f"========================================")

    conn = MT5Connector()
    if not conn.connect():
        print("Failed to connect to MT5.")
        return

    feed = MT5DataFeed()
    
    for tf_const, count in timeframes:
        feed.pull_latest_bars(symbol, tf_const, count)

    conn.disconnect()
    print("========================================")
    print(" ALL TIMEFRAMES PULLED SUCCESSFULLY")
    print("========================================")

if __name__ == "__main__":
    main()
