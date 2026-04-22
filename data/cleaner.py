"""
data/cleaner.py
===============
Data quality checks for market_data in PostgreSQL.
Detects gaps, validates OHLC integrity, and flags anomalies
that would corrupt backtest results.
"""

import pandas as pd
from datetime import timedelta
from data.db_client import DBClient

# Expected bar interval per timeframe label
TIMEFRAME_DELTAS = {
    'M1':  timedelta(minutes=1),
    'M5':  timedelta(minutes=5),
    'M15': timedelta(minutes=15),
    'H1':  timedelta(hours=1),
    'H4':  timedelta(hours=4),
    'D1':  timedelta(days=1),
}

# Maximum allowed gap multiplier before flagging (gap > expected_delta × this)
# Weekends are filtered separately.
GAP_MULTIPLIER = 1.5


class DataCleaner:
    """
    Validates data quality for a given pair/timeframe.
    All checks read from the market_data table — no files involved.
    """

    def __init__(self):
        self.db = DBClient()

    # ------------------------------------------------------------------
    # GAP DETECTION
    # ------------------------------------------------------------------
    def find_gaps(self, symbol: str, timeframe: str) -> list:
        """
        Identifies time gaps in OHLCV data that exceed the expected bar interval.
        Weekends (Saturday/Sunday) and multi-day gaps are excluded.

        Args:
            symbol:    e.g. "XAUUSD"
            timeframe: e.g. "M1", "H1", "D1"

        Returns:
            List of (gap_start, gap_end, gap_duration) tuples.
        """
        expected_delta = TIMEFRAME_DELTAS.get(timeframe)
        if expected_delta is None:
            print(f"  WARN: Unknown timeframe '{timeframe}' — skipping gap check.")
            return []

        query = """
            SELECT timestamp
            FROM market_data
            WHERE pair = %s AND timeframe = %s
            ORDER BY timestamp
        """
        rows = self.db.execute_query(query, (symbol, timeframe))

        if not rows or len(rows) < 2:
            print(f"  INFO: Not enough data for gap check on {symbol} {timeframe}.")
            return []

        timestamps = [r[0] for r in rows]
        threshold = expected_delta * GAP_MULTIPLIER
        gaps = []

        for i in range(len(timestamps) - 1):
            t_curr = timestamps[i]
            t_next = timestamps[i + 1]
            delta = t_next - t_curr

            if delta <= threshold:
                continue

            # Skip weekend gaps (Friday close → Monday open)
            # Friday = weekday 4, Saturday = 5, Sunday = 6
            if t_curr.weekday() == 4 and t_next.weekday() == 0:
                continue  # Normal Friday-to-Monday gap
            if t_curr.weekday() in (5, 6) or t_next.weekday() in (5, 6):
                continue  # Any Saturday/Sunday transition

            # Skip standard D1 weekend (gap <= 3 days for D1)
            if timeframe == 'D1' and delta.days <= 3:
                continue

            gaps.append((t_curr, t_next, delta))

        if gaps:
            print(f"  WARN: {symbol} {timeframe} — {len(gaps)} gap(s) found")
        else:
            print(f"  OK:   {symbol} {timeframe} — no significant gaps")

        return gaps

    # ------------------------------------------------------------------
    # OHLC INTEGRITY CHECK
    # ------------------------------------------------------------------
    def check_ohlc_integrity(self, symbol: str, timeframe: str) -> list:
        """
        Checks for bars where High < Low, or Close/Open outside High/Low range.
        These are corrupt bars that will break indicator calculations.

        Returns:
            List of (timestamp, open, high, low, close) for invalid bars.
        """
        query = """
            SELECT timestamp, open, high, low, close
            FROM market_data
            WHERE pair = %s AND timeframe = %s
              AND (
                high < low
                OR close > high OR close < low
                OR open > high  OR open < low
              )
            ORDER BY timestamp
        """
        rows = self.db.execute_query(query, (symbol, timeframe))
        count = len(rows) if rows else 0

        if count > 0:
            print(f"  WARN: {symbol} {timeframe} — {count} OHLC integrity violation(s)")
        else:
            print(f"  OK:   {symbol} {timeframe} — OHLC integrity clean")

        return rows or []

    # ------------------------------------------------------------------
    # ZERO VOLUME CHECK
    # ------------------------------------------------------------------
    def check_zero_volume(self, symbol: str, timeframe: str) -> int:
        """
        Counts bars with zero tick volume (common in synthetic/derived data).
        High zero-volume count suggests a data quality issue.
        """
        query = """
            SELECT COUNT(*) FROM market_data
            WHERE pair = %s AND timeframe = %s AND tick_volume = 0
        """
        result = self.db.execute_query(query, (symbol, timeframe))
        count = result[0][0] if result else 0

        if count > 0:
            print(f"  INFO: {symbol} {timeframe} — {count:,} zero-volume bar(s) (normal for resampled TFs)")
        return count

    # ------------------------------------------------------------------
    # FULL VALIDATION REPORT
    # ------------------------------------------------------------------
    def validate(self, symbol: str, timeframe: str) -> dict:
        """
        Runs all checks for a pair/timeframe and returns a summary dict.
        """
        print(f"\n  Validating {symbol} {timeframe}...")
        gaps = self.find_gaps(symbol, timeframe)
        bad_ohlc = self.check_ohlc_integrity(symbol, timeframe)
        zero_vol = self.check_zero_volume(symbol, timeframe)

        return {
            "pair": symbol,
            "timeframe": timeframe,
            "gaps": len(gaps),
            "ohlc_violations": len(bad_ohlc),
            "zero_volume_bars": zero_vol,
            "clean": len(gaps) == 0 and len(bad_ohlc) == 0
        }


if __name__ == "__main__":
    cleaner = DataCleaner()

    PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
    TIMEFRAMES = ["M1", "H1", "D1"]

    print("Running data validation for all pairs...\n")
    for pair in PAIRS:
        for tf in TIMEFRAMES:
            cleaner.validate(pair, tf)
