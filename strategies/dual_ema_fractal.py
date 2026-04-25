import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class DualEMAFractal(BaseStrategy):
    """
    Dual EMA Fractal Breaker

    Logic:
    1. Filter: Price must be above/below a 200 EMA.
    2. Fractal: Bill Williams Fractal (2-2 pattern).
    3. Signal: Price breaks above the most recent UP fractal (Bullish) or below DOWN fractal (Bearish).
    4. ADX filter: Only signal when ADX >= adx_min (trending market).
    RR = 3:1 (tp_atr_mult=3.0, sl_atr_mult=1.0).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ema_period": 200,
                "tp_atr_mult": 3.0,   # RR 3:1 (was 1.33:1)
                "sl_atr_mult": 1.0,   # tighter SL
                "atr_period": 14,
                "adx_min": 20         # only signal when trend has momentum
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

        # 1. EMA 200 filter
        df['ema_filter'] = ta.ema(df['close'], length=self.params['ema_period'])

        # 2. Fractal Detection (Bill Williams 5-bar pattern)
        df['up_fractal'] = (df['high'] > df['high'].shift(1)) & \
                           (df['high'] > df['high'].shift(2)) & \
                           (df['high'] > df['high'].shift(-1)) & \
                           (df['high'] > df['high'].shift(-2))

        df['down_fractal'] = (df['low'] < df['low'].shift(1)) & \
                             (df['low'] < df['low'].shift(2)) & \
                             (df['low'] < df['low'].shift(-1)) & \
                             (df['low'] < df['low'].shift(-2))

        # Store most recent fractal levels (shift by 2 — need 2 bars AFTER to confirm)
        df['last_up_f'] = df['high'].where(df['up_fractal']).ffill().shift(2)
        df['last_down_f'] = df['low'].where(df['down_fractal']).ffill().shift(2)

        # 3. ADX filter — only trade trending markets
        adx_min = self.params.get("adx_min", 20)
        try:
            adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 25.0  # fallback: always pass if ADX unavailable
        trending = df['adx'] >= adx_min

        # 4. Signals
        df['signal'] = 0

        # Bullish: Price > EMA + ADX trending + fractal breakout
        df.loc[
            trending &
            (df['close'] > df['ema_filter']) &
            (df['close'] > df['last_up_f']) &
            (df['close'].shift(1) <= df['last_up_f']),
            'signal'
        ] = 1

        # Bearish: Price < EMA + ADX trending + fractal breakdown
        df.loc[
            trending &
            (df['close'] < df['ema_filter']) &
            (df['close'] < df['last_down_f']) &
            (df['close'].shift(1) >= df['last_down_f']),
            'signal'
        ] = -1

        return df

    def validate_params(self) -> bool:
        return self.params['ema_period'] > 0
