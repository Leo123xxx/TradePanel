import time
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging_.event_logger import EventLogger

def test_logs():
    logger = EventLogger()
    print("Testing Publication system...")
    
    # 1. System Start
    logger.log_event("SYSTEM_START", "INFO", "Testing real-time publication hub.")
    time.sleep(1)
    
    # 2. Backtest Simulation (Will trigger archival and NOTIFY)
    logger.log_event("BACKTEST_START", "INFO", "Simulating research backtest for EURUSD.", {"symbol": "EURUSD"})
    time.sleep(2)
    
    # 3. Connection Warning
    logger.log_event("MT5_BRIDGE", "WARNING", "Bridge latency detected: 250ms.")
    time.sleep(1)
    
    # 4. Backtest End (Metrics)
    logger.log_event("BACKTEST_END", "SUCCESS", "Simulated backtest completed.", {"net_pnl": 1250.50, "trades": 45})
    
    print("Events logged. Check the Dashboard (webapp/main.py) and D:\\Trade_training_data")

if __name__ == "__main__":
    test_logs()
