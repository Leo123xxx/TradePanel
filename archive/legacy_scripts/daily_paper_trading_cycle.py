#!/usr/bin/env python3
"""
scripts/daily_paper_trading_cycle.py — Orchestrates the daily paper trading cycle.
1. Runs the validation suite (backtest-based check of all 25 strategies).
2. Summarizes live paper trading performance from the database.
3. Updates the web dashboard with current metrics.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.daily_validation_suite import DailyValidationSuite
from data.db_client import DBClient
from notifications.telegram_bot import TelegramBot

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

def run_cycle():
    logger.info("=" * 60)
    logger.info("DAILY PAPER TRADING CYCLE START")
    logger.info("=" * 60)

    # 1. Run Validation Suite (Updates Dashboard JSON)
    logger.info("Step 1: Running Daily Validation Suite...")
    suite = DailyValidationSuite(quick_mode=True)
    val_results = suite.run_all_validations()
    
    # 2. Fetch Live Paper Trading Performance (from DB)
    logger.info("Step 2: Fetching Live Paper Performance...")
    db = DBClient()
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    perf_query = """
        SELECT 
            COUNT(*) as total_trades,
            SUM(CASE WHEN exit_price > entry_price THEN 1 ELSE 0 END) as wins,
            SUM(exit_price - entry_price) as total_pnl
        FROM trades 
        WHERE mode = 'PAPER' AND DATE(close_time) = %s
    """
    
    try:
        perf_data = db.execute_query(perf_query, (yesterday,))
        if perf_data and perf_data[0][0] > 0:
            total, wins, pnl = perf_data[0]
            wr = (wins / total) * 100
            logger.info(f"Yesterday's Performance: {total} trades, {wr:.1f}% WR, {pnl:.2f} PnL")
        else:
            logger.info("No paper trades found for yesterday.")
    except Exception as e:
        logger.warning(f"Could not fetch paper performance: {e}")

    # 3. Final Status Report
    logger.info("=" * 60)
    logger.info(f"CYCLE COMPLETE: {val_results['pass_rate']} strategies passed validation.")
    logger.info(f"Dashboard updated: {val_results['dashboard']['last_update']}")
    logger.info("=" * 60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("DRY RUN: Validation suite only.")
        suite = DailyValidationSuite(quick_mode=True)
        suite.run_all_validations()
    else:
        run_cycle()
