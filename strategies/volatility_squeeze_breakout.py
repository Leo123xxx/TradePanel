"""
strategies/volatility_squeeze_breakout.py
==========================================
Volatility Squeeze Breakout — BB Width Compression → Momentum Expansion.

Works on any asset where volatility contracts before a large directional move.
Particularly effective on:
  - BTCUSD / ETHUSD: pre-breakout consolidation before explosive trends
  - XAUUSD: gold regularly forms tight compression zones before ATR expansion

Signal logic (two-phase entry):
  Phase 1 — SQUEEZE: BB width < N% of price for at least `squeeze_bars` consecutive bars.
            This identifies a compression zone where volatility has contracted.
  Phase 2 — BREAKOUT: On the first bar where price closes outside the BB,
            with momentum confirmed by MACD histogram direction.

  Buy  (1):  Squeeze just ended + close > BB upper + MACD histogram positive (expanding)
  Sell (-1): Squeeze just ended + close < BB lower + MACD histogram negative (expanding)
  Hold (0):  Inside bands, or no momentum confirmation

Why MACD histogram (not MACD crossover)?
  The histogram shows the RATE OF CHANGE of the MACD line. A positive and growing
  histogram means momentum is accelerating in the direction of the breakout.
  A breakout with accelerating momentum = higher probability of follow-through.

Why BB width threshold?
  BB width (upper - lower) as a % of price = normalised volatility.
  When this contracts below `squeeze_pct` for several consecutive bars,
  it signals energy compression — a breakout is imminent.
  This avoids trading random BB touches during already-volatile conditions.
"""

import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD", "GBPUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class VolatilitySqueezeBreakoutStrategy(BaseStrategy):
    """
    Bollinger Band width compression → momentum breakout entry.
    Works on crypto (H4/D1) and high-volatility metals.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "bb_period":      20,
                "bb_deviation":    2.0,
                "squeeze_pct":     0.03,   # BB width / price < 3% = squeeze (normalised)
                "squeeze_bars":    3,      # Must be in squeeze for this many bars
                "macd_fast":      12,
                "macd_slow":      26,
                "macd_signal":     9,
                "atr_period":     14,
                "tp_atr_mult":     3.0,   # Wide TP — squeeze breakouts can run far
                "sl_atr_mult":     1.5,
            }
        super().__init__(
            name="Volatility_Squeeze_Breakout",
            category="Breakout",
            params=params,
            regime=["ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Detects BB compression zones and fires on the first breakout bar
        with MACD histogram momentum confirmation.
        """
        df = data.copy()

        bb_p       = self.params.get("bb_period",    20)
        bb_std     = self.params.get("bb_deviation",  2.0)
        sq_pct     = self.params.get("squeeze_pct",   0.03)
        sq_bars    = self.params.get("squeeze_bars",   3)
        macd_fast  = self.params.get("macd_fast",    12)
        macd_slow  = self.params.get("macd_slow",    26)
        macd_sig   = self.params.get("macd_signal",   9)

        # ── Bollinger Bands ───────────────────────────────────────────────────
        bb_df      = ta.bbands(df['close'], length=bb_p, std=bb_std)
        df['bb_lower'] = bb_df[f"BBL_{bb_p}_{bb_std}"]
        df['bb_upper'] = bb_df[f"BBU_{bb_p}_{bb_std}"]
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['close']  # normalised

        # ── MACD histogram ────────────────────────────────────────────────────
        macd_df       = ta.macd(df['close'], fast=macd_fast, slow=macd_slow, signal=macd_sig)
        hist_col      = f"MACDh_{macd_fast}_{macd_slow}_{macd_sig}"
        df['macd_hist'] = macd_df[hist_col]

        # ── Squeeze detection ─────────────────────────────────────────────────
        # A bar is "in squeeze" if BB width (normalised) < squeeze_pct
        df['in_squeeze'] = df['bb_width'] < sq_pct

        # Count consecutive squeeze bars using a rolling window
        # True = 1, False = 0; if rolling sum == squeeze_bars, we had sq_bars consecutive squeeze bars
        df['squeeze_count'] = df['in_squeeze'].astype(int).rolling(window=sq_bars).sum()

        # The bar IMMEDIATELY AFTER a squeeze (squeeze just ended this bar)
        # = previous bar was still in squeeze, but current bar is NOT in squeeze
        prior_squeeze     = df['squeeze_count'].shift(1) >= sq_bars
        squeeze_just_ended = prior_squeeze & ~df['in_squeeze']

        # ── Breakout + momentum ───────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            squeeze_just_ended &
            (df['close'] > df['bb_upper']) &
            (df['macd_hist'] > 0) &              # histogram positive (bullish momentum)
            (df['macd_hist'] > df['macd_hist'].shift(1))  # histogram growing (accelerating)
        )

        short_cond = (
            squeeze_just_ended &
            (df['close'] < df['bb_lower']) &
            (df['macd_hist'] < 0) &              # histogram negative (bearish momentum)
            (df['macd_hist'] < df['macd_hist'].shift(1))  # histogram more negative (accelerating)
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return (
            self.params.get("bb_deviation", 0) > 0 and
            self.params.get("squeeze_pct", 0) > 0 and
            self.params.get("squeeze_bars", 0) >= 2 and
            self.params.get("macd_fast", 0) < self.params.get("macd_slow", 999)
        )
