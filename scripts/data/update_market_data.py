"""
scripts/update_market_data.py
=============================
Incremental market data updater — tops up the PostgreSQL DB with the latest
bars from MT5 for all 7 trading pairs.

Delegates to data/ingestion.py (run_full_ingestion) which already handles
incremental sync:
  1. Checks the DB for the latest bar per pair
  2. Pulls from (last_bar + 1 min) to now via MT5
  3. Resamples M1 → M5, M15, M30, H1, H4, D1
  4. Runs gap checks on a representative sample of timeframes
  5. Prints a coverage summary table

Requirements:
  - MT5 terminal running and logged in on this machine
  - PostgreSQL running with market_data table present
  - .env with DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

Usage:
    python scripts/update_market_data.py
"""

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime
from data.ingestion import run_full_ingestion


def main():
    print()
    print("=" * 62)
    print("  TradePanel — Incremental Market Data Update")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)
    print()
    print("  Pairs   : XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD,")
    print("            BTCUSD, ETHUSD, GBPJPY, AUDUSD, USDCAD,")
    print("            USDZAR, USOIL, US500, USTEC, NVDA, AMD,")
    print("            MSFT, AAPL (18 total)")
    print("  Source  : MT5 terminal (must be running + logged in)")
    print("  Mode    : Incremental — only pulls bars newer than DB")
    print()

    try:
        run_full_ingestion()
    except Exception as e:
        print(f"\nFATAL ERROR during ingestion: {e}")
        sys.exit(1)

    print()
    print("=" * 62)
    print("  Market data update complete.")
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
