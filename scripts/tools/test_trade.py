import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

import MetaTrader5 as mt5
from mt5_bridge.connector import MT5Connector
from mt5_bridge.order_manager import OrderManager

def test_trade():
    connector = MT5Connector()
    if not connector.connect():
        print("Failed to connect to MT5")
        return

    om = OrderManager()
    symbol = "ETHUSD"
    direction = "BUY"
    lot = 0.1

    
    print(f"Attempting to open a test position: {direction} {lot} on {symbol}...")
    res, msg = om.open_position(
        symbol, direction, lot, 
        sl_points=100, tp_points=200, 
        comment="TEST_DRY_RUN",
        magic=999999
    )
    
    if res and res.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"SUCCESS: Trade opened! Ticket: {res.order}")
        # Close it immediately
        print(f"Closing test position {res.order}...")
        c_res, c_msg = om.close_position(res.order, "TEST_DRY_RUN_CLOSE")
        if c_res and c_res.retcode == mt5.TRADE_RETCODE_DONE:
            print("SUCCESS: Trade closed!")
        else:
            print(f"FAILED to close: {c_msg}")
    else:
        print(f"FAILED to open: {msg}")
        if res:
            print(f"Result details: {res}")

    connector.disconnect()

if __name__ == "__main__":
    test_trade()
