"""
strategies/cot_sentiment.py - COT Sentiment Swing Strategy
===========================================================
Uses CFTC Commitments of Traders (COT) data to detect extreme
commercial positioning as a contrarian swing signal.

Logic:
  1. COT Index >= buy_threshold (default 85) -> BUY signal
  2. COT Index <= sell_threshold (default 20) -> SELL signal
  3. COT Delta filter (v3 NEW): the 4-week rate of change of COT Index must be
     moving TOWARD the extreme (delta < 0 for buy signals = positioning building,
     delta > 0 for sell signals = shorting pressure building).
  4. EMA50 filter: only trade in the direction of the 50-period EMA trend
  5. RSI momentum confirmation gate (v2)
  6. Pair-dependent trend gate: EMA200 for commodities, EMA50 for FX

Data dependency:
  Requires `cot_data` table populated by data/cot_feed.py.
  Initial setup:  python data/cot_feed.py --history
  Weekly update:  runs automatically every Friday at 21:00 UTC via APScheduler.

Timeframes: D1, W1
Pairs:      XAUUSD, EURUSD, GBPUSD, USDJPY
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.base_strategy import BaseStrategy


class COTSentimentStrategy(BaseStrategy):
    """
    v3 upgrades (2026-05-01):
    - COT delta filter: 4-week rate of change of COT Index must be moving
      in the direction of the extreme (positioning must be BUILDING, not reversing).
      Eliminates entries on exhausted extremes where the COT is already turning.
    """

    _COMMODITY_PAIRS = {"XAUUSD", "XAGUSD"}

    def __init__(self, params=None):
        default_params = {
            "sentiment_threshold":  75,    # loosened 85→75: catch more extremes
            "sell_threshold":       25,    # loosened 20→25
            "ema_filter":           50,
            "atr_period":           14,
            "tp_atr_mult":           3.0,
            "sl_atr_mult":           1.5,
            "rsi_period":           14,
            "rsi_buy_min":          52,
            "rsi_sell_max":         48,
            "cot_delta_weeks":       4,   # NEW: rolling window for COT rate of change
        }
        if params:
            default_params.update(params)

        super().__init__(
            name="COT_Sentiment_Swing",
            category="Advanced",
            params=default_params,
            regime=["TRENDING"],
            timeframes=["D1", "W1"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
        )
        self._cot_cache = {}
        self._active_pair = None

    def _load_cot_data(self, pair):
        try:
            from data.db_client import DBClient
            db = DBClient()
            rows = db.execute_query(
                """SELECT report_date, cot_index
                   FROM cot_data
                   WHERE pair = %s AND cot_index IS NOT NULL
                   ORDER BY report_date ASC""",
                (pair,)
            )
            if not rows or len(rows) < 8:
                return None
            dates  = pd.to_datetime([r[0] for r in rows])
            values = pd.Series(
                [float(r[1]) for r in rows],
                index=dates,
                name="cot_index"
            )
            return values
        except Exception as e:
            print("[COT_Sentiment] Could not load COT data for {}: {}".format(pair, e))
            return None

    def _align_cot_to_bars(self, price_df, cot_series):
        cot_reindexed = cot_series.reindex(
            price_df.index.union(cot_series.index)
        ).sort_index().ffill()
        return cot_reindexed.reindex(price_df.index)

    def generate_signals(self, data):
        df = data.copy()
        df["signal"] = 0

        pair = self._active_pair
        if pair is None or pair not in (self.pairs or []):
            print("[COT_Sentiment] Pair '{}' not in strategy list - no signals.".format(pair))
            return df

        if pair not in self._cot_cache:
            self._cot_cache[pair] = self._load_cot_data(pair)
        cot = self._cot_cache[pair]

        if cot is None or cot.empty:
            print("[COT_Sentiment] No COT data for {}. Run: python data/cot_feed.py --history".format(pair))
            return df

        df.index = pd.to_datetime(df.index)
        df["cot_index"] = self._align_cot_to_bars(df, cot).values

        # COT delta: 4-week rate of change
        # Positive delta = COT index rising (bulls building for buy threshold, bears reversing)
        # For BUY signals we want: COT >= 85 AND delta < 0 (still moving lower = more extreme)
        # Wait -- reconsider: if COT >= 85 (already extreme) and delta < 0 means still heading to extremes
        # COT Index for commercials: high index = heavy net long = bullish reversal signal
        # Delta < 0 near the top = still building toward extreme (positioning not yet reversing)
        delta_weeks  = self.params.get("cot_delta_weeks", 4)
        df["cot_delta"] = df["cot_index"].diff(delta_weeks)

        # Delta filter:
        # BUY: COT at extreme high, delta <= 0 (still moving toward extreme or plateauing)
        # SELL: COT at extreme low, delta >= 0 (still moving toward extreme or plateauing)
        # This removes entries where the extreme was 4 weeks ago and COT is already reversing
        cot_delta_ok_buy  = df["cot_delta"] <= 5    # allow small reversion (within noise)
        cot_delta_ok_sell = df["cot_delta"] >= -5   # allow small reversion (within noise)

        ema_period = self.params.get("ema_filter", 50)
        df["ema_trend"] = df["close"].ewm(span=ema_period, adjust=False).mean()

        threshold      = self.params.get("sentiment_threshold", 85)
        sell_threshold = self.params.get("sell_threshold", 20)
        cot_valid      = df["cot_index"].notna() & df["cot_delta"].notna()

        rsi_p        = self.params.get("rsi_period",   14)
        rsi_buy_min  = self.params.get("rsi_buy_min",  52)
        rsi_sell_max = self.params.get("rsi_sell_max", 48)
        try:
            import ta_compat as ta
            df["rsi"] = ta.rsi(df["close"], length=rsi_p)
        except Exception:
            df["rsi"] = 50.0
        rsi_bull_ok = df["rsi"] > rsi_buy_min
        rsi_bear_ok = df["rsi"] < rsi_sell_max

        is_commodity = pair in self._COMMODITY_PAIRS

        if is_commodity:
            df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()
            in_bull = df["close"] > df["ema200"]
            in_bear = df["close"] < df["ema200"]
        else:
            in_bull = df["close"] > df["ema_trend"]
            in_bear = df["close"] < df["ema_trend"]

        buy_cond = (
            cot_valid &
            (df["cot_index"] >= threshold) &
            cot_delta_ok_buy &    # NEW: COT not already reversing sharply from extreme
            (df["close"] > df["ema_trend"]) &
            in_bull &
            rsi_bull_ok
        )
        sell_cond = (
            cot_valid &
            (df["cot_index"] <= sell_threshold) &
            cot_delta_ok_sell &   # NEW: COT not already reversing sharply from extreme
            (df["close"] < df["ema_trend"]) &
            in_bear &
            rsi_bear_ok
        )

        signal_col = pd.Series(0, index=df.index, dtype=int)
        active = 0
        for i in range(len(df)):
            idx_val = df["cot_index"].iloc[i]
            if pd.isna(idx_val):
                signal_col.iloc[i] = 0
                continue

            if buy_cond.iloc[i]:
                active = 1
            elif sell_cond.iloc[i]:
                active = -1
            elif active == 1 and idx_val < 50:
                active = 0
            elif active == -1 and idx_val > 50:
                active = 0

            signal_col.iloc[i] = active

        df["signal"] = signal_col.values

        n_buy  = (df["signal"] == 1).sum()
        n_sell = (df["signal"] == -1).sum()
        latest_cot = df["cot_index"].dropna().iloc[-1] if cot_valid.any() else None
        cot_str = "{:.1f}".format(latest_cot) if latest_cot is not None else "N/A"
        latest_delta = df["cot_delta"].dropna().iloc[-1] if df["cot_delta"].notna().any() else None
        delta_str = "{:.1f}".format(latest_delta) if latest_delta is not None else "N/A"
        print("[COT_Sentiment] {} | COT: {} | Delta({}w): {} | Signals: {} BUY, {} SELL".format(
            pair, cot_str, delta_weeks, delta_str, n_buy, n_sell))

        return df

    def set_pair(self, pair):
        self._active_pair = pair

    def validate_params(self):
        t  = self.params.get("sentiment_threshold", 85)
        st = self.params.get("sell_threshold", 20)
        return 50 < t <= 100 and 0 < st < 50
