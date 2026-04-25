"""
strategies/cot_sentiment.py - COT Sentiment Swing Strategy
===========================================================
Uses CFTC Commitments of Traders (COT) data to detect extreme
commercial positioning as a contrarian swing signal.

Logic:
  1. COT Index >= buy_threshold (default 80) -> BUY signal
  2. COT Index <= sell_threshold (default 30) -> SELL signal
  3. EMA50 filter: only trade in the direction of the 50-period EMA trend
  4. Trend gate (pair-dependent):
       - Commodity pairs (XAUUSD, XAGUSD): hard EMA200 gate — never trade
         against the primary trend. Without this, COT "short" readings during
         pullbacks in a multi-year bull generated WR=27% and DD=209%.
       - Forex pairs (EURUSD, GBPUSD, USDJPY): EMA50 direction gate only —
         both trend directions are legitimate for FX; EMA200 is too slow and
         was blocking all sell signals during valid downtrend periods.
  5. Exit: when COT Index crosses back through 50 (neutral zone)

Data dependency:
  Requires `cot_data` table populated by data/cot_feed.py.
  Initial setup:  python data/cot_feed.py --history
  Weekly update:  runs automatically every Friday at 21:00 UTC via APScheduler.

Timeframes: D1, W1  (COT data is weekly - sub-daily TFs are not meaningful)
Pairs:      XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD
"""

import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.base_strategy import BaseStrategy


class COTSentimentStrategy(BaseStrategy):

    # Commodity pairs use a hard EMA200 trend gate — both buy and sell are gated
    # on the primary (200-period) trend direction.  For forex pairs only the
    # EMA50 directional filter applies; EMA200 is too slow and was blocking all
    # SELL signals on EURUSD / GBPUSD / USDJPY during valid downtrend periods.
    _COMMODITY_PAIRS = {"XAUUSD", "XAGUSD"}

    def __init__(self, params=None):
        default_params = {
            "sentiment_threshold": 80,
            # sell_threshold: COT index at or below which a SELL is triggered.
            # Default 30 (not 20 = 100-threshold) — commercial short extremes
            # are less frequent than long extremes for most pairs, so a slightly
            # looser threshold captures valid setups without over-trading.
            "sell_threshold":      30,
            "ema_filter":          50,
            "atr_period":          14,
            "tp_atr_mult":         3.0,
            "sl_atr_mult":         1.5,
        }
        if params:
            default_params.update(params)

        super().__init__(
            name="COT_Sentiment_Swing",
            category="Advanced",
            params=default_params,
            regime=["TRENDING"],
            timeframes=["D1", "W1"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
        )
        self._cot_cache = {}
        self._active_pair = None

    # ---- Data loading --------------------------------------------------------

    def _load_cot_data(self, pair):
        """
        Load COT index history for a pair from the DB.
        Returns a Series indexed by report_date (datetime), values = cot_index.
        Returns None if table missing or data unavailable.
        """
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
            if not rows or len(rows) < 4:
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
        """
        Forward-fill the weekly COT index onto the daily/weekly price bar index.
        CFTC data is released each Friday covering the prior Tuesday positions.
        Forward-filling means each bar uses the most recently available COT reading.
        """
        cot_reindexed = cot_series.reindex(
            price_df.index.union(cot_series.index)
        ).sort_index().ffill()
        return cot_reindexed.reindex(price_df.index)

    # ---- Signal generation ---------------------------------------------------

    def generate_signals(self, data):
        df = data.copy()
        df["signal"] = 0

        pair = self._active_pair
        if pair is None or pair not in (self.pairs or []):
            print("[COT_Sentiment] Pair '{}' not in strategy list - no signals. "
                  "Call strategy.set_pair(pair) before generate_signals().".format(pair))
            return df

        if pair not in self._cot_cache:
            self._cot_cache[pair] = self._load_cot_data(pair)
        cot = self._cot_cache[pair]

        if cot is None or cot.empty:
            print("[COT_Sentiment] No COT data for {}. "
                  "Run: python data/cot_feed.py --history".format(pair))
            return df

        df.index = pd.to_datetime(df.index)
        df["cot_index"] = self._align_cot_to_bars(df, cot).values

        ema_period = self.params.get("ema_filter", 50)
        df["ema_trend"] = df["close"].ewm(span=ema_period, adjust=False).mean()

        threshold      = self.params.get("sentiment_threshold", 80)
        sell_threshold = self.params.get("sell_threshold", 30)
        cot_valid      = df["cot_index"].notna()

        is_commodity = pair in self._COMMODITY_PAIRS

        if is_commodity:
            # Hard EMA200 gate: XAUUSD/XAGUSD are in long structural trends.
            # Without this, COT short readings during pullbacks in a multi-year
            # bull produced WR=27% and DD=209% on XAUUSD.
            df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()
            in_bull = df["close"] > df["ema200"]
            in_bear = df["close"] < df["ema200"]
        else:
            # Forex pairs: use EMA50 direction as the trend gate.
            # EMA200 was blocking all sell signals for EURUSD/GBPUSD/USDJPY
            # even during confirmed downtrend periods, because EMA200 lags
            # too far behind for daily swing trading.
            in_bull = df["close"] > df["ema_trend"]
            in_bear = df["close"] < df["ema_trend"]

        buy_cond = (
            cot_valid &
            (df["cot_index"] >= threshold) &
            (df["close"] > df["ema_trend"]) &
            in_bull
        )
        sell_cond = (
            cot_valid &
            (df["cot_index"] <= sell_threshold) &
            (df["close"] < df["ema_trend"]) &
            in_bear
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
        print("[COT_Sentiment] {} | Latest COT Index: {} | "
              "Signals generated: {} BUY, {} SELL".format(pair, cot_str, n_buy, n_sell))

        return df

    # ---- Helpers -------------------------------------------------------------

    def set_pair(self, pair):
        """
        Must be called before generate_signals() so the strategy knows
        which pair's COT data to load.
        Called automatically by the backtest engine and paper engine.
        """
        self._active_pair = pair

    def validate_params(self):
        t  = self.params.get("sentiment_threshold", 80)
        st = self.params.get("sell_threshold", 30)
        return 50 < t <= 100 and 0 < st < 50
