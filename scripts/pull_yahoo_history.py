"""
scripts/pull_yahoo_history.py
==============================
Supplements MT5/Exness historical data for stock and index CFDs using
Yahoo Finance as a free secondary source.

WHY THIS EXISTS
---------------
Exness provides only 1-3 years of history for stock CFDs (NVDA, AMD, MSFT,
AAPL, US500, USTEC, USOIL).  This script pulls up to 729 days of H1 data
and 10+ years of D1 data from Yahoo Finance, resamples H1 into H2/H4, and
upserts everything into the market_data table.

Conflict strategy: ON CONFLICT DO NOTHING
  MT5/Exness bars always win.  Yahoo data fills only the historical gap that
  Exness cannot provide.  Running this script is always safe; it never
  overwrites broker-accurate data.

TYPICAL GAIN
------------
  Stock CFDs H4 bars:  ~200-400 (Exness)  ->  700+ after Yahoo fill
  D1 history:          1-3 years (Exness) ->  10+ years after Yahoo fill

USAGE
-----
  pip install yfinance --break-system-packages   # one-time setup

  python scripts/pull_yahoo_history.py                       # all pairs
  python scripts/pull_yahoo_history.py --pairs NVDA AAPL     # specific pairs
  python scripts/pull_yahoo_history.py --check-only          # coverage only
  python scripts/pull_yahoo_history.py --d1-years 15         # 15yr D1 history

SCHEDULING
----------
  Add as a weekly job in docker_jobs.py (Sunday 02:00 UTC, before overnight
  backtest) so the 729-day H1 window keeps rolling forward automatically.
"""

import sys
import os
import argparse
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from data.db_client import DBClient


# ---------------------------------------------------------------------------
# Symbol map: Exness CFD symbol  ->  Yahoo Finance ticker
# ---------------------------------------------------------------------------
YAHOO_SYMBOL_MAP = {
    "NVDA":  "NVDA",   # NVIDIA stock CFD
    "AMD":   "AMD",    # AMD stock CFD
    "MSFT":  "MSFT",   # Microsoft stock CFD
    "AAPL":  "AAPL",   # Apple stock CFD
    "US500": "^GSPC",  # S&P 500 index CFD  (Exness = US500)
    "USTEC": "^NDX",   # NASDAQ-100 CFD     (Exness = USTEC / NAS100)
    "USOIL": "CL=F",   # WTI Crude Oil futures (closest liquid proxy for Exness USOIL)
}

# Timeframes to derive from the H1 download
DERIVE_FROM_H1 = ["H1", "H2", "H4"]

# Pandas resample rules — mirrors data/resampler.py exactly
RESAMPLE_RULES = {
    "H1": "h",
    "H2": "2h",
    "H4": "4h",
    "D1": "D",
}

# Reporting threshold: H4 bars considered "good" for WFO training
MIN_H4_BARS_TARGET = 500

# Polite delay between Yahoo requests (avoid rate-limit)
REQUEST_DELAY_SECS = 1.5


# ---------------------------------------------------------------------------
# Yahoo Finance helpers
# ---------------------------------------------------------------------------

def _to_utc_naive(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a timezone-aware DatetimeIndex to UTC, then strip tz for Postgres."""
    if hasattr(df.index, "tz") and df.index.tz is not None:
        df.index = df.index.tz_convert("UTC").tz_localize(None)
    return df


def _normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise yfinance output to lowercase single-level columns.
    yfinance >=0.2 sometimes returns MultiIndex columns like ('Open', 'NVDA').
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0].lower() for col in df.columns]
    else:
        df.columns = [c.lower() for c in df.columns]
    return df


def _resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resample an OHLCV DataFrame to a lower frequency."""
    resampled = df.resample(rule).agg({
        "open":   "first",
        "high":   "max",
        "low":    "min",
        "close":  "last",
        "volume": "sum",
    }).dropna(subset=["open", "close"])
    # Drop the last (possibly incomplete) bar — it may still be forming
    if len(resampled) > 1:
        resampled = resampled.iloc[:-1]
    return resampled


def _to_insert_tuples(df: pd.DataFrame, pair: str, timeframe: str) -> list:
    """Convert a resampled DataFrame to the tuple format expected by insert_market_data."""
    tuples = []
    for ts, row in df.iterrows():
        tuples.append((
            pair,
            timeframe,
            ts,
            float(row["open"]),
            float(row["high"]),
            float(row["low"]),
            float(row["close"]),
            int(row.get("volume", 0)),
            0,          # spread — not available from Yahoo; costs modelled by backtest engine
        ))
    return tuples


def download_h1(yahoo_ticker: str) -> pd.DataFrame | None:
    """
    Download up to 729 days of hourly (H1) bars from Yahoo Finance.
    Yahoo caps intraday history at 730 days; 729 gives a safe buffer.

    Returns a UTC-naive OHLCV DataFrame or None on failure.
    """
    try:
        import yfinance as yf
    except ImportError:
        print("  ! yfinance not installed.  Run: pip install yfinance --break-system-packages")
        return None

    start = (datetime.now() - timedelta(days=729)).strftime("%Y-%m-%d")
    try:
        ticker = yf.Ticker(yahoo_ticker)
        df = ticker.history(start=start, interval="1h", auto_adjust=True)
        if df is None or df.empty:
            print(f"  ! No H1 data returned for {yahoo_ticker}")
            return None

        df = _normalise_columns(df)
        df = df[["open", "high", "low", "close", "volume"]].copy()
        df = _to_utc_naive(df)
        df = df[df["open"].notna() & df["close"].notna() & (df["open"] > 0)]
        df.index = pd.to_datetime(df.index)
        return df

    except Exception as exc:
        print(f"  ! H1 download error [{yahoo_ticker}]: {exc}")
        return None


def download_d1(yahoo_ticker: str, years: int = 10) -> pd.DataFrame | None:
    """
    Download `years` years of daily (D1) bars from Yahoo Finance.
    D1 history goes back 20+ years for US stocks and major indices.

    Returns a UTC-naive OHLCV DataFrame or None on failure.
    """
    try:
        import yfinance as yf
    except ImportError:
        return None

    start = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")
    try:
        ticker = yf.Ticker(yahoo_ticker)
        df = ticker.history(start=start, interval="1d", auto_adjust=True)
        if df is None or df.empty:
            print(f"  ! No D1 data returned for {yahoo_ticker}")
            return None

        df = _normalise_columns(df)
        df = df[["open", "high", "low", "close", "volume"]].copy()
        df = _to_utc_naive(df)
        df = df[df["open"].notna() & df["close"].notna() & (df["open"] > 0)]

        # Normalise D1 timestamps to midnight UTC so they align with MT5 D1 bars.
        # MT5 stores D1 bars as YYYY-MM-DD 00:00:00 (start of day, UTC).
        df.index = pd.to_datetime(df.index.date)

        return df

    except Exception as exc:
        print(f"  ! D1 download error [{yahoo_ticker}]: {exc}")
        return None


# ---------------------------------------------------------------------------
# Coverage reporting
# ---------------------------------------------------------------------------

def get_coverage(db: DBClient, pairs: list) -> dict:
    """Return {pair: {tf: {count, min_ts, max_ts}}} for H1/H2/H4/D1."""
    coverage = {}
    for pair in pairs:
        coverage[pair] = {}
        for tf in ["H1", "H2", "H4", "D1"]:
            rows = db.execute_query(
                "SELECT COUNT(*), MIN(timestamp), MAX(timestamp) "
                "FROM market_data WHERE pair = %s AND timeframe = %s",
                (pair, tf),
            )
            count  = rows[0][0] if rows else 0
            min_ts = rows[0][1] if rows else None
            max_ts = rows[0][2] if rows else None
            coverage[pair][tf] = {"count": count, "min": min_ts, "max": max_ts}
    return coverage


def print_coverage(coverage: dict, label: str = ""):
    if label:
        print(f"\n  {label}")
    header = f"  {'Pair':<10} {'TF':<6} {'Bars':>7}  {'From':<12}  {'To':<12}  Note"
    print(header)
    print("  " + "-" * 68)
    for pair in sorted(coverage):
        for tf, info in coverage[pair].items():
            count  = info["count"]
            min_ts = info["min"].strftime("%Y-%m-%d") if info["min"] else "-"
            max_ts = info["max"].strftime("%Y-%m-%d") if info["max"] else "-"
            note   = ""
            if tf == "H4":
                note = "[OK] GOOD" if count >= MIN_H4_BARS_TARGET else "[!] LOW (target >=500)"
            print(f"  {pair:<10} {tf:<6} {count:>7}  {min_ts:<12}  {max_ts:<12}  {note}")
    print()


# ---------------------------------------------------------------------------
# Per-pair processing
# ---------------------------------------------------------------------------

def process_pair(pair: str, yahoo_ticker: str, db: DBClient, d1_years: int) -> dict:
    """
    Download, resample, and upsert Yahoo data for one CFD pair.
    Returns a summary dict.
    """
    summary = {
        "pair":          pair,
        "ticker":        yahoo_ticker,
        "bars_inserted": {},
        "errors":        [],
    }

    print(f"\n  {'-' * 57}")
    print(f"  {pair}  <-  {yahoo_ticker}")
    print(f"  {'-' * 57}")

    # -- H1  ->  H1, H2, H4  -----------------------------------------------
    print(f"  Downloading H1 (729 days)... ", end="", flush=True)
    h1_df = download_h1(yahoo_ticker)

    if h1_df is not None and not h1_df.empty:
        print(f"{len(h1_df):,} raw hourly bars")

        for tf in DERIVE_FROM_H1:
            if tf == "H1":
                # Use H1 directly; still drop the last incomplete bar
                tf_df = h1_df.iloc[:-1].copy() if len(h1_df) > 1 else h1_df.copy()
            else:
                tf_df = _resample_ohlcv(h1_df, RESAMPLE_RULES[tf])

            if tf_df.empty:
                print(f"  - {tf}: no complete bars to insert")
                continue

            tuples = _to_insert_tuples(tf_df, pair, tf)
            try:
                db.insert_market_data(tuples)
                summary["bars_inserted"][tf] = len(tuples)
                print(f"  [OK] {tf}: {len(tuples):,} bars upserted  "
                      f"({tf_df.index[0].strftime('%Y-%m-%d')} -> "
                      f"{tf_df.index[-1].strftime('%Y-%m-%d')})")
            except Exception as exc:
                msg = f"{tf}: {exc}"
                summary["errors"].append(msg)
                print(f"  ! {msg}")
    else:
        print("FAILED — skipping H1/H2/H4")
        summary["errors"].append("H1 download failed")

    # -- D1  ->  stored directly  ------------------------------------------
    print(f"  Downloading D1 ({d1_years} years)... ", end="", flush=True)
    d1_df = download_d1(yahoo_ticker, years=d1_years)

    if d1_df is not None and not d1_df.empty:
        print(f"{len(d1_df):,} daily bars")
        tuples = _to_insert_tuples(d1_df, pair, "D1")
        try:
            db.insert_market_data(tuples)
            summary["bars_inserted"]["D1"] = len(tuples)
            print(f"  [OK] D1: {len(tuples):,} bars upserted  "
                  f"({d1_df.index[0].strftime('%Y-%m-%d')} -> "
                  f"{d1_df.index[-1].strftime('%Y-%m-%d')})")
        except Exception as exc:
            msg = f"D1: {exc}"
            summary["errors"].append(msg)
            print(f"  ! {msg}")
    else:
        print("FAILED")
        summary["errors"].append("D1 download failed")

    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(pairs_filter: list = None, d1_years: int = 10, check_only: bool = False):
    """Main entry point — called by CLI and scheduler."""

    target_pairs = {
        k: v for k, v in YAHOO_SYMBOL_MAP.items()
        if pairs_filter is None or k in [p.upper() for p in pairs_filter]
    }
    if not target_pairs:
        print(f"\n  ERROR: None of {pairs_filter} found in YAHOO_SYMBOL_MAP.")
        print(f"  Valid pairs: {list(YAHOO_SYMBOL_MAP.keys())}\n")
        sys.exit(1)

    print()
    print("=" * 62)
    print("  TradePanel — Yahoo Finance Historical Data Fill")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Pairs   : {', '.join(target_pairs.keys())}")
    print(f"  H1      : up to 729 days  ->  resampled to H1 / H2 / H4")
    print(f"  D1      : {d1_years} years of daily bars")
    print(f"  Conflict: ON CONFLICT DO NOTHING  (MT5 bars always win)")
    print("=" * 62)

    db = DBClient()

    # Coverage before
    coverage_before = get_coverage(db, list(target_pairs.keys()))
    print_coverage(coverage_before, label="Coverage BEFORE:")

    if check_only:
        print("  [check-only] Exiting without downloading.\n")
        return

    # Verify yfinance is available before starting
    try:
        import yfinance  # noqa: F401
    except ImportError:
        print("\n  ERROR: yfinance not installed.")
        print("  Fix:   pip install yfinance --break-system-packages")
        print("  Then re-run this script.\n")
        sys.exit(1)

    # Process each pair
    all_summaries = []
    for pair, yahoo_ticker in target_pairs.items():
        summary = process_pair(pair, yahoo_ticker, db, d1_years)
        all_summaries.append(summary)
        time.sleep(REQUEST_DELAY_SECS)

    # Coverage after
    coverage_after = get_coverage(db, list(target_pairs.keys()))
    print_coverage(coverage_after, label="Coverage AFTER:")

    # Insert totals table
    print("  Bars inserted this run:")
    print(f"  {'Pair':<10} {'H1':>7}  {'H2':>7}  {'H4':>7}  {'D1':>8}  Errors")
    print("  " + "-" * 60)
    total_inserted = 0
    for s in all_summaries:
        ins = s["bars_inserted"]
        run_total = sum(ins.values())
        total_inserted += run_total
        errs = " | ".join(s["errors"]) if s["errors"] else "-"
        print(
            f"  {s['pair']:<10}"
            f" {ins.get('H1', 0):>7,}"
            f"  {ins.get('H2', 0):>7,}"
            f"  {ins.get('H4', 0):>7,}"
            f"  {ins.get('D1', 0):>8,}"
            f"  {errs}"
        )
    print(f"\n  Total bars upserted across all pairs/TFs: {total_inserted:,}")
    print()
    print("=" * 62)
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 62)
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Fill historical data gaps for CFD pairs using Yahoo Finance.\n"
            "Uses ON CONFLICT DO NOTHING — safe to re-run, MT5 data always wins."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/pull_yahoo_history.py\n"
            "  python scripts/pull_yahoo_history.py --pairs NVDA AAPL US500\n"
            "  python scripts/pull_yahoo_history.py --check-only\n"
            "  python scripts/pull_yahoo_history.py --d1-years 15\n"
        ),
    )
    parser.add_argument(
        "--pairs", nargs="+", default=None, metavar="PAIR",
        help=(
            "Exness pair names to process "
            f"(default: all — {list(YAHOO_SYMBOL_MAP.keys())})"
        ),
    )
    parser.add_argument(
        "--d1-years", type=int, default=10,
        help="Years of D1 history to pull from Yahoo (default: 10, max ~20).",
    )
    parser.add_argument(
        "--check-only", action="store_true",
        help="Print current bar coverage without downloading anything.",
    )
    args = parser.parse_args()

    run(
        pairs_filter=args.pairs,
        d1_years=args.d1_years,
        check_only=args.check_only,
    )
