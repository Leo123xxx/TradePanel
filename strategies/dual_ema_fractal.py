import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class DualEMAFractal(BaseStrategy):
    """
    Dual EMA Fractal Breaker v3.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - Consecutive fractal confirmation: require 2 fractals in the same direction
      before the breakout is tradeable. A single fractal break is prone to fakeouts;
      two consecutive up-fractals (or down-fractals) signal a sustained swing structure.
    RR = 3:1 (tp_atr_mult=3.0, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ema_fast":              50,
                "ema_slow":             200,
                "ema_period":           200,
                "tp_atr_mult":            3.0,
                "sl_atr_mult":            1.0,
                "atr_period":            14,
                "adx_min":               20,   # loosened 25→20
                "rsi_period":            14,
                "rsi_long_min":          55,
                "rsi_short_max":         45,
                "vol_threshold_mult":     1.0, # loosened 1.2→1.0: allow average-vol setups
                "consecutive_fractals":   2,   # NEW: require N fractals in same direction
                "use_multi_tf_confirmation": False,
                "confirm_timeframe":    "H4"
            }
        super().__init__(
            name="Dual_EMA_Fractal",
            category="Trend Following",
            params=params,
            regime=["TRENDING"],
            timeframes=["H1", "D1"],
            pairs=["USDJPY", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        ema_fast_len    = self.params.get('ema_fast')
        ema_slow_len    = self.params.get('ema_slow', self.params.get('ema_period', 200))
        adx_min         = self.params.get("adx_min", 25)
        rsi_long_min    = self.params.get("rsi_long_min",  55)
        rsi_short_max   = self.params.get("rsi_short_max", 45)
        vol_mult        = self.params.get("vol_threshold_mult", 1.2)
        n_fractals      = self.params.get("consecutive_fractals", 2)

        # 1. EMA trend filter
        if ema_fast_len:
            df['ema_fast'] = ta.ema(df['close'], length=ema_fast_len)
            df['ema_slow'] = ta.ema(df['close'], length=ema_slow_len)
            df['trend_filter_up']   = df['ema_fast'] > df['ema_slow']
            df['trend_filter_down'] = df['ema_fast'] < df['ema_slow']
        else:
            df['ema_filter'] = ta.ema(df['close'], length=ema_slow_len)
            df['trend_filter_up']   = df['close'] > df['ema_filter']
            df['trend_filter_down'] = df['close'] < df['ema_filter']

        # 2. Fractal Detection (Bill Williams 5-bar, confirmed after 2 bars)
        df['up_fractal'] = (
            (df['high'] > df['high'].shift(1)) &
            (df['high'] > df['high'].shift(2)) &
            (df['high'] > df['high'].shift(-1)) &
            (df['high'] > df['high'].shift(-2))
        )
        df['down_fractal'] = (
            (df['low'] < df['low'].shift(1)) &
            (df['low'] < df['low'].shift(2)) &
            (df['low'] < df['low'].shift(-1)) &
            (df['low'] < df['low'].shift(-2))
        )

        # 3. Track last N confirmed fractal levels
        # Shift by 2 to confirm (need 2 right-hand bars)
        df['up_f_confirmed']   = df['up_fractal'].shift(2)
        df['down_f_confirmed'] = df['down_fractal'].shift(2)

        # Count consecutive confirmed fractals in same direction
        # For consecutive up fractals: rolling sum of up_f_confirmed over a window
        # A fractal occurs roughly every 5-10 bars, so look back 30 bars
        fractal_window = max(30, n_fractals * 15)
        df['consec_up']   = df['up_f_confirmed'].rolling(window=fractal_window).sum()
        df['consec_down'] = df['down_f_confirmed'].rolling(window=fractal_window).sum()

        # Most recent confirmed fractal level
        df['last_up_f']   = df['high'].where(df['up_fractal']).ffill().shift(2)
        df['last_down_f'] = df['low'].where(df['down_fractal']).ffill().shift(2)

        # 4. ADX filter
        try:
            adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 25.0
        trending = df['adx'] >= adx_min

        # 5. Signals
        df['signal'] = 0

        df.loc[
            trending &
            df['trend_filter_up'] &
            (df['consec_up'] >= n_fractals) &     # NEW: require N consecutive up fractals
            (df['close'] > df['last_up_f']) &
            (df['close'].shift(1) <= df['last_up_f']),
            'signal'
        ] = 1

        df.loc[
            trending &
            df['trend_filter_down'] &
            (df['consec_down'] >= n_fractals) &   # NEW: require N consecutive down fractals
            (df['close'] < df['last_down_f']) &
            (df['close'].shift(1) >= df['last_down_f']),
            'signal'
        ] = -1

        # 6. Meta-labeling (RSI + volume conviction)
        df = self.apply_meta_labeling(
            df,
            rsi_long=rsi_long_min,
            rsi_short=rsi_short_max,
            vol_mult=vol_mult
        )

        return df

    def validate_params(self) -> bool:
        return (self.params.get('ema_fast', 0) > 0 or self.params.get('ema_period', 0) > 0)
