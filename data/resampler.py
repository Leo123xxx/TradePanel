"""
data/resampler.py
=================
Resamples M1 OHLCV data to higher timeframes and stores results in market_data.

Two methods:
  resample_and_store(symbol, tf)     — incremental: pulls new M1 bars, resamples,
                                       stores in market_data. Used by data/ingestion.py.
  resample_m1_to_higher(symbol, tfs) — legacy: re-resamples last N days, writes to
                                       market_data_resampled (separate table).
"""

import pandas as pd
from data.db_client import DBClient
from datetime import datetime


class DataResampler:
    def __init__(self, db: DBClient):
        self.db = db

    # ------------------------------------------------------------------
    # PRIMARY — Used by data/ingestion.py daily resample step
    # Writes to market_data (same table as M1), ON CONFLICT DO NOTHING.
    # Incremental: only resamples M1 bars newer than the latest stored TF bar.
    # ------------------------------------------------------------------
    def resample_and_store(self, symbol: str, target_tf: str) -> int:
        """
        Resamples new M1 bars from market_data to target_tf and stores back
        into market_data. Incremental — checks the latest existing bar for the
        target TF and only processes M1 bars newer than that.

        Args:
            symbol:    e.g. "XAUUSD"
            target_tf: e.g. "M5", "M15", "M30", "H1", "H4", "D1"

        Returns:
            Number of new bars inserted (0 if nothing new to process).
        """
        resample_rule = self._get_resample_rule(target_tf)
        if not resample_rule:
            print(f"  WARN: No resample rule for {target_tf} — skipping.")
            return 0

        # Find the latest bar already stored for this TF
        latest_q = (
            "SELECT MAX(timestamp) FROM market_data "
            "WHERE pair = %s AND timeframe = %s"
        )
        result = self.db.execute_query(latest_q, (symbol, target_tf))
        latest_ts = result[0][0] if result and result[0][0] else None

        # Pull M1 bars newer than the latest TF bar (or all M1 if TF has no data yet)
        if latest_ts:
            m1_q = (
                "SELECT timestamp, open, high, low, close, tick_volume "
                "FROM market_data "
                "WHERE pair = %s AND timeframe = 'M1' AND timestamp > %s "
                "ORDER BY timestamp"
            )
            rows = self.db.execute_query(m1_q, (symbol, latest_ts))
        else:
            m1_q = (
                "SELECT timestamp, open, high, low, close, tick_volume "
                "FROM market_data "
                "WHERE pair = %s AND timeframe = 'M1' "
                "ORDER BY timestamp"
            )
            rows = self.db.execute_query(m1_q, (symbol,))

        if not rows:
            print(f"  OK: {symbol} {target_tf} — no new M1 bars to resample")
            return 0

        df = pd.DataFrame(
            rows,
            columns=["timestamp", "open", "high", "low", "close", "tick_volume"]
        )
        df.set_index("timestamp", inplace=True)
        for col in ["open", "high", "low", "close", "tick_volume"]:
            df[col] = df[col].astype(float)

        resampled = df.resample(resample_rule).agg({
            "open":        "first",
            "high":        "max",
            "low":         "min",
            "close":       "last",
            "tick_volume": "sum",
        }).dropna()

        # Drop the most-recent (possibly incomplete) bar — it may still be forming
        if len(resampled) > 1:
            resampled = resampled.iloc[:-1]

        if resampled.empty:
            print(f"  OK: {symbol} {target_tf} — no complete bars to store yet")
            return 0

        # Build insert tuples — spread = 0 for resampled bars (not from broker)
        data_to_insert = [
            (
                symbol, target_tf, ts,
                float(row["open"]), float(row["high"]),
                float(row["low"]),  float(row["close"]),
                int(row["tick_volume"]), 0
            )
            for ts, row in resampled.iterrows()
        ]

        self.db.insert_market_data(data_to_insert)  # ON CONFLICT DO NOTHING
        print(f"  OK: {symbol} {target_tf} — {len(data_to_insert)} bar(s) resampled and stored")
        return len(data_to_insert)

    # ------------------------------------------------------------------
    # LEGACY — writes to market_data_resampled (separate table)
    # Kept for backward compatibility.
    # ------------------------------------------------------------------
    def resample_m1_to_higher(self, symbol: str, target_tfs=None, lookback_days=7):
        """
        Fetches M1 data for a symbol and resamples into target timeframes.
        Writes to market_data_resampled (NOT market_data).
        Use resample_and_store() for the primary ingestion pipeline.
        """
        if target_tfs is None:
            target_tfs = ["H1", "H4", "D1"]

        print(f"Resampling {symbol} from M1 into {target_tfs}...")

        query = """
            SELECT timestamp, open, high, low, close, tick_volume
            FROM market_data
            WHERE pair = %s AND timeframe = 'M1'
            AND timestamp > %s
            ORDER BY timestamp
        """
        start_date = datetime.now() - pd.Timedelta(days=lookback_days)
        rows = self.db.execute_query(query, (symbol, start_date))

        if not rows:
            print(f"  No M1 data found for {symbol} in the last {lookback_days} days.")
            return

        df = pd.DataFrame(
            rows,
            columns=["timestamp", "open", "high", "low", "close", "tick_volume"]
        )
        df.set_index("timestamp", inplace=True)

        for tf in target_tfs:
            resample_rule = self._get_resample_rule(tf)
            if not resample_rule:
                continue

            resampled = df.resample(resample_rule).agg({
                "open":        "first",
                "high":        "max",
                "low":         "min",
                "close":       "last",
                "tick_volume": "sum",
            }).dropna()

            self._upsert_resampled_data(symbol, tf, resampled)

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------
    def _get_resample_rule(self, tf: str) -> str:
        mapping = {
            "M5":  "5min",
            "M15": "15min",
            "M30": "30min",
            "H1":  "h",
            "H2":  "2h",    # 2-hour: bridges H1/H4, captures 2-session cycles
            "H4":  "4h",
            "H12": "12h",   # Half-day: fills gap between H4 and D1
            "D1":  "D",
            "W1":  "W",     # Weekly: macro context, used by COT strategy
        }
        return mapping.get(tf, "")

    def _upsert_resampled_data(self, symbol, timeframe, df):
        """Upserts into market_data_resampled (legacy table)."""
        insert_query = """
            INSERT INTO market_data_resampled
                (pair, timeframe, timestamp, open, high, low, close, tick_volume)
            VALUES %s
            ON CONFLICT (pair, timeframe, timestamp) DO UPDATE SET
                open        = EXCLUDED.open,
                high        = EXCLUDED.high,
                low         = EXCLUDED.low,
                close       = EXCLUDED.close,
                tick_volume = EXCLUDED.tick_volume
        """
        data_to_insert = [
            (
                symbol, timeframe, ts,
                float(row["open"]),  float(row["high"]),
                float(row["low"]),   float(row["close"]),
                int(row["tick_volume"])
            )
            for ts, row in df.iterrows()
        ]
        self.db.execute_batch(insert_query, data_to_insert)
        print(f"  OK: Upserted {len(data_to_insert)} bars for {timeframe}.")


if __name__ == "__main__":
    db = DBClient()
    resampler = DataResampler(db)
    resampler.resample_m1_to_higher("XAUUSD")
