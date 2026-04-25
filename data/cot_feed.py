"""
data/cot_feed.py — CFTC Commitments of Traders (COT) Data Pipeline
====================================================================
Fetches weekly COT reports from the CFTC's free public Socrata JSON API.
No API key required. Data released every Friday at ~3:30pm US/Eastern.

Instruments covered (mapped to TradePanel pairs):
  XAUUSD  ← Gold Futures         CFTC code 088691
  XAGUSD  ← Silver Futures        CFTC code 084691
  EURUSD  ← Euro FX Futures       CFTC code 099741
  GBPUSD  ← British Pound Futures  CFTC code 096742
  USDJPY  ← Japanese Yen Futures   CFTC code 097741

COT Index formula (3-year / 156-week lookback):
  net_commercial = commercial_longs - commercial_shorts
  cot_index = (current_net - min_net_156w) / (max_net_156w - min_net_156w) × 100

  Index > 80 → Commercials extremely long  → Bullish signal
  Index < 20 → Commercials extremely short → Bearish signal

Scheduler: runs every Friday at 21:00 UTC (after CFTC release at ~20:30 UTC).

Usage:
    python data/cot_feed.py                    # Fetch latest + store in DB
    python data/cot_feed.py --history          # Backfill 3 years of history
    python data/cot_feed.py --dry-run          # Fetch + print, skip DB write
"""

import sys
import os
import json
import argparse
import time
from datetime import datetime, date, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pandas as pd
from data.db_client import DBClient

# ── CFTC contract codes → TradePanel pair mapping ─────────────────────────────
CFTC_CONTRACTS = {
    "088691": "XAUUSD",   # Gold Futures (COMEX)
    "084691": "XAGUSD",   # Silver Futures (COMEX)
    "099741": "EURUSD",   # Euro FX Futures (CME)
    "096742": "GBPUSD",   # British Pound Futures (CME)
    "097741": "USDJPY",   # Japanese Yen Futures (CME)
}

# CFTC public Socrata JSON API — no authentication required.
# Dataset jun7-fc8e = "Legacy-Combined" (one record per contract per week).
# Avoid srt6-5q2f ("Legacy_All") — it mixes futures-only AND combined rows,
# producing duplicate dates that corrupt the COT Index rolling calculation.
LEGACY_ENDPOINT = "https://publicreporting.cftc.gov/resource/jun7-fc8e.json"

# COT Index lookback (weeks). 156 = 3 years, 52 = 1 year
COT_INDEX_LOOKBACK = 156

# Request settings
REQUEST_TIMEOUT  = 30   # seconds
MAX_RETRIES      = 3
RETRY_DELAY      = 5    # seconds


class COTFeed:
    """Fetches, processes, and stores CFTC COT data."""

    def __init__(self):
        self.db = DBClient()
        self._ensure_table()

    # ── DB schema ──────────────────────────────────────────────────────────────

    def _ensure_table(self):
        """Create the cot_data table if it doesn't exist."""
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS cot_data (
                cot_id          SERIAL PRIMARY KEY,
                pair            VARCHAR(10)  NOT NULL,
                report_date     DATE         NOT NULL,
                cftc_code       VARCHAR(10)  NOT NULL,
                comm_long       BIGINT,
                comm_short      BIGINT,
                noncomm_long    BIGINT,
                noncomm_short   BIGINT,
                net_commercial  BIGINT,
                net_noncomm     BIGINT,
                cot_index       NUMERIC(6,2),   -- 0–100 rolling index
                open_interest   BIGINT,
                updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (pair, report_date)
            )
        """)

    # ── API fetch ──────────────────────────────────────────────────────────────

    def _fetch_cftc(self, cftc_code: str, from_date: str, top: int = 200) -> list[dict]:
        """
        Fetch COT records for one contract from CFTC Socrata JSON API.

        Args:
            cftc_code: e.g. '099741' for Euro FX
            from_date: ISO date string 'YYYY-MM-DD'
            top:       Max records to return

        Returns:
            List of raw API record dicts (Socrata returns lowercase field names).
        """
        # Socrata SoQL — note lowercase field names and different param names vs OData
        params = {
            "$where":  (
                f"cftc_contract_market_code='{cftc_code}' "
                f"AND report_date_as_yyyy_mm_dd>='{from_date}'"
            ),
            "$order":  "report_date_as_yyyy_mm_dd ASC",
            "$limit":  top,
            "$select": (
                "report_date_as_yyyy_mm_dd,"
                "cftc_contract_market_code,"
                "comm_positions_long_all,"
                "comm_positions_short_all,"
                "noncomm_positions_long_all,"
                "noncomm_positions_short_all,"
                "open_interest_all"
            ),
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.get(
                    LEGACY_ENDPOINT, params=params, timeout=REQUEST_TIMEOUT
                )
                resp.raise_for_status()
                # Socrata returns a JSON array directly (not {"value": [...]})
                return resp.json()
            except requests.RequestException as e:
                print(f"  [COT] Attempt {attempt}/{MAX_RETRIES} failed for {cftc_code}: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
        print(f"  [COT] ERROR: All retries exhausted for {cftc_code}. Skipping.")
        return []

    # ── Processing ─────────────────────────────────────────────────────────────

    def _parse_records(self, raw: list[dict], pair: str, cftc_code: str) -> pd.DataFrame:
        """Convert raw CFTC API records to a clean DataFrame."""
        if not raw:
            return pd.DataFrame()

        rows = []
        for r in raw:
            try:
                # Socrata returns lowercase field names
                rows.append({
                    "pair":         pair,
                    "report_date":  r["report_date_as_yyyy_mm_dd"],
                    "cftc_code":    cftc_code,
                    "comm_long":    int(r.get("comm_positions_long_all", 0) or 0),
                    "comm_short":   int(r.get("comm_positions_short_all", 0) or 0),
                    "noncomm_long": int(r.get("noncomm_positions_long_all", 0) or 0),
                    "noncomm_short":int(r.get("noncomm_positions_short_all", 0) or 0),
                    "open_interest":int(r.get("open_interest_all", 0) or 0),
                })
            except (KeyError, TypeError, ValueError) as e:
                print(f"  [COT] Parse error on record: {e} — skipping row")
        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        df["report_date"]    = pd.to_datetime(df["report_date"]).dt.date
        df["net_commercial"] = df["comm_long"] - df["comm_short"]
        df["net_noncomm"]    = df["noncomm_long"] - df["noncomm_short"]
        df = df.sort_values("report_date").reset_index(drop=True)

        # Dedup safety: if a dataset returns multiple rows per date (e.g. Legacy_All
        # mixes futures-only and combined), keep the row with the largest open_interest
        # (combined report has higher OI than futures-only).
        before = len(df)
        df = df.sort_values("open_interest", ascending=False).drop_duplicates(
            subset=["pair", "report_date"], keep="first"
        ).sort_values("report_date").reset_index(drop=True)
        if len(df) < before:
            print(f"  [COT] Dedup removed {before - len(df)} duplicate date rows for {pair}")

        return df

    def _calculate_cot_index(self, df: pd.DataFrame,
                              lookback: int = COT_INDEX_LOOKBACK) -> pd.DataFrame:
        """
        Calculate the rolling COT Index (0–100) for the net_commercial column.

        COT Index = (net_commercial - rolling_min) / (rolling_max - rolling_min) × 100
        A high index (>80) means commercials are more long than usual → bullish.
        A low index (<20) means commercials are more short than usual → bearish.
        """
        net = df["net_commercial"]
        rolling_min = net.rolling(window=lookback, min_periods=max(4, lookback // 10)).min()
        rolling_max = net.rolling(window=lookback, min_periods=max(4, lookback // 10)).max()
        rng = rolling_max - rolling_min
        # Avoid div-by-zero when all values are the same
        cot_idx = ((net - rolling_min) / rng.replace(0, float("nan"))) * 100
        df["cot_index"] = cot_idx.round(2)
        return df

    # ── DB write ───────────────────────────────────────────────────────────────

    def _upsert_records(self, df: pd.DataFrame) -> int:
        """Upsert processed records into the cot_data table. Returns rows inserted."""
        if df.empty:
            return 0
        inserted = 0
        for _, row in df.iterrows():
            try:
                self.db.execute_query("""
                    INSERT INTO cot_data
                        (pair, report_date, cftc_code,
                         comm_long, comm_short, noncomm_long, noncomm_short,
                         net_commercial, net_noncomm, cot_index, open_interest,
                         updated_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (pair, report_date)
                    DO UPDATE SET
                        comm_long      = EXCLUDED.comm_long,
                        comm_short     = EXCLUDED.comm_short,
                        noncomm_long   = EXCLUDED.noncomm_long,
                        noncomm_short  = EXCLUDED.noncomm_short,
                        net_commercial = EXCLUDED.net_commercial,
                        net_noncomm    = EXCLUDED.net_noncomm,
                        cot_index      = EXCLUDED.cot_index,
                        open_interest  = EXCLUDED.open_interest,
                        updated_at     = EXCLUDED.updated_at
                """, (
                    row["pair"],
                    row["report_date"],
                    row["cftc_code"],
                    int(row["comm_long"]),
                    int(row["comm_short"]),
                    int(row["noncomm_long"]),
                    int(row["noncomm_short"]),
                    int(row["net_commercial"]),
                    int(row["net_noncomm"]),
                    None if pd.isna(row["cot_index"]) else float(row["cot_index"]),
                    int(row["open_interest"]),
                    datetime.now(),
                ))
                inserted += 1
            except Exception as e:
                print(f"  [COT] DB write error for {row['pair']} {row['report_date']}: {e}")
        return inserted

    # ── Public API ─────────────────────────────────────────────────────────────

    def fetch_latest(self, dry_run: bool = False) -> dict:
        """
        Fetch the most recent 8 weeks of COT data for all tracked pairs.
        Suitable for the weekly Friday scheduler job.

        Returns: dict of {pair: rows_inserted}
        """
        from_date = (date.today() - timedelta(weeks=10)).isoformat()
        return self._run(from_date, dry_run=dry_run, label="latest")

    def fetch_history(self, years: int = 3, dry_run: bool = False) -> dict:
        """
        Backfill full COT history (default 3 years = 156 weeks).
        Run once on initial setup to populate the DB for backtesting.

        Returns: dict of {pair: rows_inserted}
        """
        from_date = (date.today() - timedelta(weeks=years * 52)).isoformat()
        return self._run(from_date, dry_run=dry_run, label=f"{years}y history",
                         top=years * 52 + 20)

    def _run(self, from_date: str, dry_run: bool,
             label: str, top: int = 20) -> dict:
        """Internal runner used by fetch_latest and fetch_history."""
        results = {}
        print(f"\n[COT] Fetching {label} from {from_date} "
              f"({'DRY RUN — no DB write' if dry_run else 'writing to DB'})...")
        print(f"[COT] Pairs: {list(CFTC_CONTRACTS.values())}\n")

        for cftc_code, pair in CFTC_CONTRACTS.items():
            print(f"  [{pair}] Fetching CFTC code {cftc_code}...")
            raw = self._fetch_cftc(cftc_code, from_date, top=top)
            if not raw:
                print(f"  [{pair}] No data returned — skipping")
                results[pair] = 0
                continue

            df = self._parse_records(raw, pair, cftc_code)
            if df.empty:
                print(f"  [{pair}] Parse returned empty DataFrame — skipping")
                results[pair] = 0
                continue

            # For history runs, need full lookback to calc index properly
            if top > 20:
                df = self._calculate_cot_index(df, lookback=min(COT_INDEX_LOOKBACK, len(df)))
            else:
                # For weekly updates, load existing history to calc rolling index
                df = self._calculate_index_with_db_history(df, pair)

            latest = df.iloc[-1]
            print(f"  [{pair}] {len(df)} records | "
                  f"Latest: {latest['report_date']} | "
                  f"Net Commercial: {int(latest['net_commercial']):+,} | "
                  f"COT Index: {latest['cot_index']:.1f}")

            if dry_run:
                results[pair] = len(df)
                continue

            n = self._upsert_records(df)
            print(f"  [{pair}] ✓ {n} rows upserted to DB")
            results[pair] = n

        total = sum(results.values())
        print(f"\n[COT] Complete. Total rows upserted: {total}")
        return results

    def _calculate_index_with_db_history(self, new_df: pd.DataFrame,
                                          pair: str) -> pd.DataFrame:
        """
        For weekly updates: load existing history from DB, append new rows,
        recalculate the rolling COT Index with full lookback, then return only
        the new rows (with freshly calculated index values).
        """
        try:
            rows = self.db.execute_query(
                """SELECT report_date, comm_long, comm_short, noncomm_long,
                          noncomm_short, open_interest
                   FROM cot_data WHERE pair = %s
                   ORDER BY report_date ASC""",
                (pair,)
            )
            if rows:
                hist_df = pd.DataFrame(rows, columns=[
                    "report_date", "comm_long", "comm_short",
                    "noncomm_long", "noncomm_short", "open_interest"
                ])
                hist_df["pair"]     = pair
                hist_df["cftc_code"] = new_df["cftc_code"].iloc[0]
                hist_df["net_commercial"] = hist_df["comm_long"] - hist_df["comm_short"]
                hist_df["net_noncomm"]    = hist_df["noncomm_long"] - hist_df["noncomm_short"]
                hist_df["report_date"] = pd.to_datetime(hist_df["report_date"]).dt.date

                # Merge: keep existing, overlay with new
                combined = pd.concat([hist_df, new_df], ignore_index=True)
                combined = combined.drop_duplicates("report_date", keep="last")
                combined = combined.sort_values("report_date").reset_index(drop=True)
            else:
                combined = new_df.copy()
        except Exception as e:
            print(f"  [COT] Could not load history for {pair}: {e} — using new data only")
            combined = new_df.copy()

        combined = self._calculate_cot_index(combined)
        # Return only the rows that were in new_df
        new_dates = set(new_df["report_date"])
        return combined[combined["report_date"].isin(new_dates)].reset_index(drop=True)

    def get_latest_signal(self, pair: str) -> dict | None:
        """
        Return the most recent COT signal for a pair.
        Used by the cot_sentiment strategy at signal generation time.

        Returns dict with keys: report_date, cot_index, net_commercial,
                                 net_noncomm, signal (1=BUY, -1=SELL, 0=NEUTRAL)
        """
        rows = self.db.execute_query(
            """SELECT report_date, cot_index, net_commercial, net_noncomm
               FROM cot_data WHERE pair = %s
               ORDER BY report_date DESC LIMIT 1""",
            (pair,)
        )
        if not rows:
            return None
        rdate, cot_idx, net_comm, net_nc = rows[0]
        cot_idx = float(cot_idx) if cot_idx is not None else None
        signal = 0
        if cot_idx is not None:
            if cot_idx >= 80:
                signal = 1   # Commercials extremely long → bullish
            elif cot_idx <= 20:
                signal = -1  # Commercials extremely short → bearish
        return {
            "report_date":    rdate,
            "cot_index":      cot_idx,
            "net_commercial": int(net_comm or 0),
            "net_noncomm":    int(net_nc or 0),
            "signal":         signal,
        }

    def print_summary(self) -> None:
        """Print current COT signal summary for all tracked pairs."""
        print("\n" + "=" * 60)
        print("COT SIGNAL SUMMARY")
        print("=" * 60)
        for pair in CFTC_CONTRACTS.values():
            sig = self.get_latest_signal(pair)
            if not sig:
                print(f"  {pair:8} — No data (run --history to backfill)")
                continue
            idx  = sig["cot_index"]
            icon = "🟢 BULLISH" if sig["signal"] == 1 \
                else "🔴 BEARISH" if sig["signal"] == -1 \
                else "⬜ NEUTRAL"
            age = (date.today() - sig["report_date"]).days if sig["report_date"] else "?"
            print(f"  {pair:8} | COT Index: {idx:5.1f} | {icon:12} "
                  f"| Net Comm: {sig['net_commercial']:+9,} | {age}d old")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="CFTC COT data pipeline — fetch and store weekly COT reports"
    )
    parser.add_argument("--history",  action="store_true",
                        help="Backfill 3 years of historical COT data (run once on setup)")
    parser.add_argument("--years",    type=int, default=3,
                        help="Years of history to backfill (default 3, used with --history)")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Fetch and print data without writing to DB")
    parser.add_argument("--summary",  action="store_true",
                        help="Print current COT signals from DB (no fetch)")
    args = parser.parse_args()

    feed = COTFeed()

    if args.summary:
        feed.print_summary()
        return

    if args.history:
        print(f"\nBackfilling {args.years} years of COT history...")
        feed.fetch_history(years=args.years, dry_run=args.dry_run)
    else:
        feed.fetch_latest(dry_run=args.dry_run)
    feed.print_summary()


if __name__ == "__main__":
    main()
