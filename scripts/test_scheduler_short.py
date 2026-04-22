# scripts/test_scheduler_short.py
import time
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scheduler.jobs import TradingScheduler
from datetime import datetime

if __name__ == "__main__":
    print(f"[{datetime.now()}] Starting Scheduler for 2-minute test run...")
    try:
        ts = TradingScheduler()
        ts.start()
        print("Scheduler running. Waiting for 120 seconds...")
        time.sleep(120)
        ts.stop()
        print(f"[{datetime.now()}] Scheduler stopped. Check bot_health for heartbeats.")
    except Exception as e:
        print(f"Scheduler test FAILED: {e}")
