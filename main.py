#!/usr/bin/env python3
"""
main.py — TradePanel Master Control Script

Unified entry point for all TradePanel operations with option flags.
Handles paper trading, validation, backtesting, Telegram bot, and more.

USAGE:
    python main.py --mode paper-trade          # Run paper trading cycle
    python main.py --mode validate             # Run validation suite
    python main.py --mode backtest --strategy range_breakout --pair XAUUSD
    python main.py --mode telegram             # Start Telegram bot
    python main.py --mode health               # System health check
    python main.py --mode full                 # Run everything (paper + telegram + validation)
    python main.py --mode scheduler            # Run scheduled tasks

For help:
    python main.py --help
"""

import os
import sys
import asyncio
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv()

# Configure logging
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            LOGS_DIR / "main.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
    ]
)
logger = logging.getLogger(__name__)


class TradePanel:
    """Master controller for all TradePanel operations."""

    def __init__(self):
        """Initialize TradePanel with all required modules."""
        self.project_root = PROJECT_ROOT
        self.logs_dir = self.project_root / "logs"
        self.results_dir = self.project_root / "results"
        self.logs_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)

    def verify_environment(self):
        """Verify all required environment variables and dependencies."""
        logger.info("=" * 70)
        logger.info("ENVIRONMENT VERIFICATION")
        logger.info("=" * 70)

        checks = {
            "MT5_LOGIN": "MT5 Login",
            "MT5_PASSWORD": "MT5 Password",
            "DB_HOST": "Database Host",
            "DB_NAME": "Database Name",
            "DB_USER": "Database User",
            "TELEGRAM_BOT_TOKEN": "Telegram Bot Token",
            "TELEGRAM_CHAT_ID": "Telegram Chat ID",
        }

        all_good = True
        for env_var, description in checks.items():
            value = os.getenv(env_var)
            if value:
                # Mask sensitive values
                if "PASSWORD" in env_var or "TOKEN" in env_var:
                    display = f"{value[:10]}...{value[-5:]}"
                else:
                    display = value
                logger.info(f"OK: {description}: {display}")
            else:
                logger.warning(f"WARN: {description} ({env_var}): NOT SET")
                all_good = False

        logger.info("=" * 70)
        return all_good

    def validate_config(self):
        """Validate configuration files."""
        logger.info("Validating configuration files...")
        try:
            from scripts.config_validator import validate_config
            config_file = self.project_root / "config" / "strategies.yaml"
            result = validate_config(config_file)
            if result:
                logger.info("OK: Config validation passed")
                return True
            else:
                logger.error("ERROR: Config validation failed")
                return False
        except Exception as e:
            logger.error(f"ERROR: Error validating config: {e}")
            return False

    async def run_paper_trade(self):
        """Run the paper trading cycle."""
        logger.info("=" * 70)
        logger.info("PAPER TRADING CYCLE")
        logger.info("=" * 70)
        try:
            from scripts.daily_paper_trading_cycle import run_cycle
            logger.info("Starting paper trading cycle...")
            run_cycle()
            logger.info("OK: Paper trading cycle complete")
            return True
        except Exception as e:
            logger.error(f"ERROR: Paper trading failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def run_validation(self):
        """Run the validation suite."""
        logger.info("=" * 70)
        logger.info("VALIDATION SUITE")
        logger.info("=" * 70)
        try:
            from scripts.daily_validation_suite import DailyValidationSuite
            logger.info("Running validation suite...")
            suite = DailyValidationSuite(quick_mode=True)
            results = suite.run_all_validations()
            logger.info(f"OK: Validation complete: {results['pass_rate']} pass rate")
            return True
        except Exception as e:
            logger.error(f"ERROR: Validation failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def run_backtest(self, strategy, pair, timeframe, limit=None):
        """Run backtest for a specific strategy."""
        logger.info("=" * 70)
        logger.info(f"BACKTEST: {strategy} on {pair} {timeframe}")
        logger.info("=" * 70)
        try:
            from scripts.run_backtest import run_backtest
            logger.info(f"Starting backtest: {strategy} on {pair} {timeframe}")
            run_backtest(strategy, pair, timeframe)
            logger.info("OK: Backtest complete")
            return True
        except Exception as e:
            logger.error(f"ERROR: Backtest failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def run_telegram_bot(self):
        """Start the Telegram bot."""
        logger.info("=" * 70)
        logger.info("TELEGRAM BOT")
        logger.info("=" * 70)

        # Guard: if running inside Docker the 'telegram' container already owns
        # the bot process. Starting a second instance from the host would cause
        # a conflict (same token, duplicate polling). Skip gracefully.
        if os.getenv("RUNNING_IN_DOCKER"):
            pass  # we ARE inside Docker — proceed normally
        else:
            logger.info("SKIP: Telegram bot is managed by the Docker 'telegram' container.")
            logger.info("      Run 'docker logs telegram' to view bot activity.")
            logger.info("      To run locally (no Docker): set RUNNING_IN_DOCKER=1 in .env")
            return True

        # Verify token is set
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            logger.error("ERROR: TELEGRAM_BOT_TOKEN not found in .env")
            return False

        try:
            from notifications.telegram_bot import TelegramBot
            bot = TelegramBot()
            logger.info("ROBOT: Starting Telegram bot...")
            logger.info(f"   Token: {token[:20]}...{token[-10:]}")
            logger.info(f"   Chat ID: {os.getenv('TELEGRAM_CHAT_ID', 'Not set')}")
            await bot.start()
            return True
        except KeyboardInterrupt:
            logger.info("Bot shutdown by user")
            return True
        except Exception as e:
            logger.error(f"ERROR: Telegram bot failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def run_health_check(self):
        """Run system health check."""
        logger.info("=" * 70)
        logger.info("SYSTEM HEALTH CHECK")
        logger.info("=" * 70)

        checks_passed = 0
        checks_total = 0

        # 1. Environment check
        checks_total += 1
        if self.verify_environment():
            checks_passed += 1

        # 2. Config validation
        checks_total += 1
        logger.info("\nValidating configuration...")
        if self.validate_config():
            checks_passed += 1

        # 3. Database check
        checks_total += 1
        logger.info("\nChecking database connection...")
        try:
            from data.db_client import DBClient
            db = DBClient()
            result = db.execute_query("SELECT 1")
            if result:
                logger.info("OK: Database connection: OK")
                checks_passed += 1
            else:
                logger.error("ERROR: Database connection: FAILED")
        except Exception as e:
            logger.error(f"ERROR: Database check failed: {e}")

        # 4. MT5 check
        checks_total += 1
        logger.info("\nChecking MT5 connection...")
        try:
            from mt5_bridge.connector import MT5Connector
            connector = MT5Connector()
            # Note: connect() returns True/False and sets self.connected
            if connector.connect():
                logger.info("OK: MT5 connection: OK")
                checks_passed += 1
            else:
                logger.warning("WARN: MT5 connection: Not ready")
        except Exception as e:
            logger.warning(f"WARN: MT5 check: {e}")

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info(f"HEALTH CHECK SUMMARY: {checks_passed}/{checks_total} passed")
        logger.info("=" * 70)

        return checks_passed == checks_total

    async def run_full(self):
        """Run full cycle: validation, paper trading, telegram."""
        logger.info("=" * 70)
        logger.info("FULL CYCLE: Validation + Paper Trading + Telegram")
        logger.info("=" * 70)

        results = {}

        # 1. Health check
        logger.info("\n[1/3] Running health check...")
        results['health'] = await self.run_health_check()

        # 2. Validation
        logger.info("\n[2/3] Running validation...")
        results['validation'] = await self.run_validation()

        # 3. Paper trading
        logger.info("\n[3/3] Running paper trading...")
        results['paper_trade'] = await self.run_paper_trade()

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("FULL CYCLE COMPLETE")
        for key, value in results.items():
            status = "OK" if value else "ERROR"
            logger.info(f"{status} {key.replace('_', ' ').title()}: {value}")
        logger.info("=" * 70)

        return all(results.values())

    async def run_scheduler(self):
        """Run scheduled tasks (for cron/scheduler integration)."""
        logger.info("=" * 70)
        logger.info("SCHEDULER MODE")
        logger.info("=" * 70)

        logger.info("Running scheduled tasks...")
        logger.info(f"Current time: {datetime.now()}")

        # Check what should run based on time
        now = datetime.now()

        # Daily validation at 1:00 AM UTC
        if now.hour == 1 and now.minute < 5:
            logger.info("Running daily cycle (1:00 AM UTC)...")
            return await self.run_full()

        # Otherwise just run validation
        logger.info("Running validation only...")
        return await self.run_validation()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TradePanel Master Control - Unified entry point for all operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python main.py --mode paper-trade
  python main.py --mode validate
  python main.py --mode backtest --strategy range_breakout --pair XAUUSD --timeframe H4
  python main.py --mode telegram
  python main.py --mode health
  python main.py --mode full
  python main.py --mode scheduler

MODES:
  paper-trade    Run paper trading cycle (daily validation + trading)
  validate       Run validation suite only
  backtest       Run backtest for specific strategy
  telegram       Start Telegram bot for commands
  health         System health check and diagnostics
  full           Run everything (validation + paper-trade)
  scheduler      Run scheduled tasks (for cron integration)
        """
    )

    parser.add_argument(
        "--mode",
        required=True,
        choices=["paper-trade", "validate", "backtest", "telegram", "health", "full", "scheduler"],
        help="Operation mode"
    )

    parser.add_argument(
        "--strategy",
        type=str,
        help="Strategy name (for backtest mode)"
    )

    parser.add_argument(
        "--pair",
        type=str,
        default="XAUUSD",
        help="Trading pair (for backtest mode)"
    )

    parser.add_argument(
        "--timeframe",
        type=str,
        default="H1",
        help="Timeframe (for backtest mode)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of bars (for backtest mode)"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console output (log to file only)"
    )

    args = parser.parse_args()

    # Initialize TradePanel
    panel = TradePanel()

    # Suppress console output if requested
    if args.quiet:
        logging.getLogger().handlers[0].setLevel(logging.WARNING)

    try:
        # Route to appropriate function
        if args.mode == "paper-trade":
            success = await panel.run_paper_trade()

        elif args.mode == "validate":
            success = await panel.run_validation()

        elif args.mode == "backtest":
            if not args.strategy:
                logger.error("❌ --strategy is required for backtest mode")
                sys.exit(1)
            success = await panel.run_backtest(args.strategy, args.pair, args.timeframe, args.limit)

        elif args.mode == "telegram":
            success = await panel.run_telegram_bot()

        elif args.mode == "health":
            success = await panel.run_health_check()

        elif args.mode == "full":
            success = await panel.run_full()

        elif args.mode == "scheduler":
            success = await panel.run_scheduler()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("\nSTOP: Shutting down...")
        sys.exit(0)

    except Exception as e:
        logger.error(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
