import asyncio
import nest_asyncio
import signal
import sys
import os
import time
from datetime import datetime

# Allow nested event loops for concurrent scheduler/bot execution
nest_asyncio.apply()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.jobs import TradingScheduler

async def main():
    print("="*40)
    print("   MT5 TRADING PLATFORM - AUTOMATED MODE")
    print("   (Strategy Scheduler + Telegram Bot)")
    print("="*40)
    
    try:
        scheduler = TradingScheduler()
    except Exception as e:
        print(f"FAILED to initialize Scheduler: {e}")
        return

    print("Status: INITIALIZING COMPONENTS...")
    
    # 1. Start the Strategy Scheduler (Runs in its own background threads)
    scheduler.start()
    
    # 2. Initialize and Start the Telegram Bot Listener (Async)
    # We use the instance already created inside the scheduler
    bot = scheduler.notif_bot
    
    print("Status: STARTING TELEGRAM BOT LISTENER...")
    
    try:
        # Start bot polling
        await bot.start()
        
        print("-" * 40)
        print("SYSTEM ACTIVE AND POLLING")
        print("Press Ctrl+C to stop.")
        print("-" * 40)
        
        # Simple loop to keep the main task alive since polling is background
        while True:
            await asyncio.sleep(1)
            
    except (KeyboardInterrupt, SystemExit, asyncio.CancelledError):
        print("\nShutdown signal received. Stopping...")
    except Exception as e:
        print(f"CRITICAL ERROR in main loop: {e}")
    finally:
        print("Stopping scheduler...")
        scheduler.stop()
        print("Stopping bot...")
        await bot.stop()
        print("Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
