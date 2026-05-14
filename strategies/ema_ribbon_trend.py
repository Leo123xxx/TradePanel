"""
strategies/ema_ribbon_trend.py
==============================
EMA Ribbon Trend — Multi-EMA Alignment Trend Follower.

Designed for high-volatility assets with strong directional trends: BTCUSD, ETHUSD,
and XAUUSD in trending regimes.

Signal logic:
  Buy  (1):  All 3 EMAs aligned bullish (fast > mid > slow) AND close > fast EMA
             AND ADX confirms trend strength AND RSI > 50 (momentum above midline)
             AND close > EMA200 (macro trend filter — v2 2026-04-29)
  Sell (-1): All 3 EMAs aligned bearish (fast < mid < slow) AND close < fast EMA
             AND ADX confirms trend strength AND RSI < 50
             AND close < EMA200 (macro trend filter — v2 2026-04-29)
  Hold (0):  No alignment or mixed signals

Why 3 EMAs?
  A single crossover (2 EMAs) generates many false entries in volatile markets.
  A 3-EMA ribbon requires all three to agree — much higher conviction entries.
  The close > fast EMA filter additionally confirms price is not in a pullback.

Crypto-specific notes:
  - 24/7 market: no session filter needed
  - Higher ATR multipliers than FX: default TP=3.0x, SL=1.5x
  - Wider fast/mid/slow gaps than FX: 9/21/55 captures crypto's explosive moves
  - Works on H4 (primary) and D1 (secondary for longer-term positions)
"""

import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD", "GBPUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class EMARibbonTrendStrategy(BaseStrategy):
    """
    Multi-EMA Ribbon Trend Follower.
    Primary application: BTCUSD, ETHUSD (crypto — 24/7 signal generation).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "fast_ema":           9,      # Short-term trend (reacts fast)
                "mid_ema":           21,      # Medium-term trend
                "slow_ema":          55,      # Long-term trend (ribbon spine)
                "adx_min":           28,      # raised to 28 for stronger trend filtering
                "rsi_period":        14,      # RSI for momentum filter
                "atr_period":        14,
                "tp_atr_mult":        3.0,    # Larger TP for crypto's bigger moves
                "sl_atr_mult":        1.0,    # was 1.5 — tighter SL lifts RR from 2:1 to 3:1
                "vol_threshold_mult": 0,      # disabled vol gate — killing too many setups
                "ema200_period":    200,      # Macro trend gate — added 2026-04-29
            }
        super().__init__(
            name="EMA_Ribbon_Trend",
            category="Trend Following",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        3-EMA ribbon alignment + RSI momentum + ADX trend strength.
        Entry fires only when all three filters agree.
        """
        df = data.copy()

        fast_p    = self.params.get("fast_ema",           9)
        mid_p     = self.params.get("mid_ema",            21)
        slow_p    = self.params.get("slow_ema",           55)
        adx_min   = self.params.get("adx_min",            28)
        rsi_p     = self.params.get("rsi_period",         14)
        vol_p     = self.params.get("vol_lookback",       20)
        vol_mult  = self.params.get("vol_threshold_mult",  0.0)  # 0 = disabled
        ema200_p  = self.params.get("ema200_period",     200)

        # ── EMA ribbon ────────────────────────────────────────────────────────
        df['ema_fast'] = ta.ema(df['close'], length=fast_p)
        df['ema_mid']  = ta.ema(df['close'], length=mid_p)
        df['ema_slow'] = ta.ema(df['close'], length=slow_p)

        # ── EMA200 macro trend gate ───────────────────────────────────────────
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # ── Supporting indicators ─────────────────────────────────────────────
        df['rsi']    = ta.rsi(df['close'], length=rsi_p)
        adx_df       = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx']    = adx_df["ADX_14"]

        df['atr']    = ta.atr(df['high'], df['low'], df['close'], length=14)
        df['atr_ma'] = ta.sma(df['atr'], length=vol_p)

        # ── Ribbon alignment filters ──────────────────────────────────────────
        bullish_ribbon = (
            (df['ema_fast'] > df['ema_mid']) &
            (df['ema_mid']  > df['ema_slow']) &
            (df['close']    > df['ema_fast'])   # price above the ribbon
        )
        bearish_ribbon = (
            (df['ema_fast'] < df['ema_mid']) &
            (df['ema_mid']  < df['ema_slow']) &
            (df['close']    < df['ema_fast'])   # price below the ribbon
        )

        trend_ok = df['adx'] >= adx_min
        vol_ok   = (df['atr'] >= df['atr_ma'] * vol_mult) if vol_mult > 0 else True

        # ── Signal generation — fire only on the bar the ribbon flips ─────────
        # Use shift(1) to detect a NEW alignment (first bar of ribbon agreement)
        prev_bullish = (
            (df['ema_fast'].shift(1) > df['ema_mid'].shift(1)) &
            (df['ema_mid'].shift(1)  > df['ema_slow'].shift(1))
        )
        prev_bearish = (
            (df['ema_fast'].shift(1) < df['ema_mid'].shift(1)) &
            (df['ema_mid'].shift(1)  < df['ema_slow'].shift(1))
        )

        # NEW bullish alignment = ribbon just turned bullish this bar
        new_bullish = bullish_ribbon & ~prev_bullish
        # NEW bearish alignment = ribbon just turned bearish this bar
        new_bearish = bearish_ribbon & ~prev_bearish

        df['signal'] = 0

        long_cond  = new_bullish & trend_ok & vol_ok & (df['rsi'] > 50) & macro_up
        short_cond = new_bearish & trend_ok & vol_ok & (df['rsi'] < 50) & macro_down

        # Layer 3 — ATR ceiling (ribbon flips during news spikes are high false-positive)
        df['atr_avg'] = ta.sma(df['atr'], length=vol_p)   # reuse existing atr / atr_ma
        long_cond, short_cond = self.apply_atr_ceiling(df, long_cond, short_cond,
                                                        atr_col='atr', avg_col='atr_avg')
        # Layer 5 — Prev-bar momentum (confirm ribbon flip is backed by directional bar)
        long_cond, short_cond = self.apply_prev_bar_momentum(df, long_cond, short_cond)

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        fast = self.params.get("fast_ema", 0)
        mid  = self.params.get("mid_ema",  0)
        slow = self.params.get("slow_ema", 0)
        return fast > 0 and fast < mid < slow
