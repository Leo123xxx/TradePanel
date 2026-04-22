#!/usr/bin/env python3
"""
scripts/start_telegram_bot.py — Starts the Telegram bot for command handling and notifications.

Usage:
    python scripts/start_telegram_bot.py

The bot will start polling for commands and remain active in the foreground.
For production, run as a background process:
    nohup python scripts/start_telegram_bot.py > logs/telegram_bot.log 2>&1 &
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging with UTF-8 encoding for console compatibility
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(PROJECT_ROOT / "logs" / "telegram_bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def main():
    """Start the Telegram bot."""
    from notifications.telegram_bot import TelegramBot

    logger.info("=" * 70)
    logger.info("TELEGRAM BOT STARTUP")
    logger.info("=" * 70)

    # Check for required environment variable
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("[ERROR] TELEGRAM_BOT_TOKEN not found in .env file")
        logger.error("   Please add: TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return False

    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        logger.warning("[WARNING] TELEGRAM_CHAT_ID not found in .env file")
        logger.warning("   Set it to receive alerts: TELEGRAM_CHAT_ID=your_chat_id")

    try:
        # Initialize and start bot
        bot = TelegramBot()
        logger.info("[BOT] Initializing Telegram bot...")
        logger.info(f"   Token: {token[:20]}...{token[-10:]}")
        logger.info(f"   Chat ID: {chat_id}")

        logger.info("[BOT] Starting bot polling...")
        await bot.start()

        logger.info("[SUCCESS] Bot is now active and listening for commands")
        logger.info("   Available commands:")
        logger.info("   /status   - System and account status")
        logger.info("   /balance  - Balance and equity")
        logger.info("   /active   - List open positions")
        logger.info("   /signals  - Recent strategy signals")
        logger.info("   /analysis - Multi-TF market summary")
        logger.info("   /risk     - Account drawdown and risk")
        logger.info("   /mode     - Operating mode and strategies")
        logger.info("   /health   - System health status")
        logger.info("   /help     - Show all commands")
        logger.info("")
        logger.info("[INFO] Press CTRL+C to stop the bot")
        logger.info("=" * 70)

        # Keep the bot running
        await asyncio.Event().wait()

    except KeyboardInterrupt:
        logger.info("\n[STOP] Shutting down bot...")
        await bot.stop()
        logger.info("[SUCCESS] Bot stopped")
        return True

    except Exception as e:
        logger.error(f"[ERROR] Error starting bot: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Bot shutdown by user")
        sys.exit(0)
