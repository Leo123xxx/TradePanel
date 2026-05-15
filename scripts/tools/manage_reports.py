import os
import shutil
import time
import logging
from datetime import datetime, timedelta
from notifications.telegram_bot import TelegramBot

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BASE_DIR = PROJECT_ROOT
RESULTS_DIR = os.path.join(BASE_DIR, "results", "overnight")
ARCHIVE_DIR = os.path.join(BASE_DIR, "results", "archive")

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def notify_failure(error_msg: str):
    """Sends a failure alert to Telegram."""
    try:
        bot = TelegramBot()
        bot.send_sync_message(f"🚨 *Report Management Failure*\n\n{error_msg}")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")

def run_management():
    """Archives reports older than 48 hours and cleans up."""
    try:
        if not os.path.exists(ARCHIVE_DIR):
            os.makedirs(ARCHIVE_DIR)

        now = time.time()
        cutoff = now - (48 * 3600)  # 48 hours
        
        archived_count = 0
        
        # Pattern matching for reports
        for filename in os.listdir(RESULTS_DIR):
            if not filename.endswith(".json") and not filename.endswith(".md"):
                continue
                
            file_path = os.path.join(RESULTS_DIR, filename)
            
            # Check if it's older than cutoff
            if os.path.getmtime(file_path) < cutoff:
                # Move to archive
                dest_path = os.path.join(ARCHIVE_DIR, filename)
                shutil.move(file_path, dest_path)
                archived_count += 1
                logger.info(f"Archived: {filename}")

        logger.info(f"Cleanup complete. Archived {archived_count} files.")
        return True, archived_count

    except Exception as e:
        error_info = f"Critical error in manage_reports.py: {str(e)}"
        logger.error(error_info)
        notify_failure(error_info)
        return False, str(e)

if __name__ == "__main__":
    run_management()
