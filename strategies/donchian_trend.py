import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class DonchianTrendStrategy(BaseStrategy):
    """
    Donchian Channel Trend Following (Turtle Style)
    
    Logic:
      1. Long: Close breaks above the N-bar High Donchian Channel.
      2. Short: Close breaks below the N-bar Low Donchian Channel.
      3. Exit: ATR-based Trailing Stop or N-bar Low/High crossover.
    
    Optimized for Crypto:
      - Uses longer periods (e.g., 20, 55) to capture major moves.
      - ADX filter to avoid choppy ranges.
    """

    def __init__(self, params: dict = None):
        defaults = {
            "donchian_period": 20,
            "adx_min": 25,
            "atr_period": 14,
            "tp_atr_mult": 4.0,  # High reward for trend following
            "sl_atr_mult": 1.5,
            "use_trailing_stop": True,
        }
        if params:
            defaults.update(params)
        super().__init__(
            name="Donchian_Trend",
            category="Trend Following",
            params=defaults,
        )

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.params
        df = df.copy()
        df["signal"] = 0

        if len(df) < p["donchian_period"]:
            return df

        # Donchian Channels
        df["donchian_high"] = df["high"].rolling(window=p["donchian_period"]).max().shift(1)
        df["donchian_low"]  = df["low"].rolling(window=p["donchian_period"]).min().shift(1)

        # ADX for trend strength
        adx_df = ta.adx(df["high"], df["low"], df["close"], length=14)
        df["adx"] = adx_df["ADX_14"]

        # Signals
        long_cond = (
            (df["close"] > df["donchian_high"]) & 
            (df["adx"] > p["adx_min"]) &
            (df["close"] > df["open"])  # NEW: Directional Close
        )
        short_cond = (
            (df["close"] < df["donchian_low"]) & 
            (df["adx"] > p["adx_min"]) &
            (df["close"] < df["open"])  # NEW: Directional Close
        )

        # Layer 2 — Body Ratio
        long_cond, short_cond = self.apply_body_ratio_filter(df, long_cond, short_cond)

        df.loc[long_cond, "signal"] = 1
        df.loc[short_cond, "signal"] = -1

        # Cleanup: Only first signal in a sequence
        df.loc[(df["signal"] == 1) & (df["signal"].shift(1) == 1), "signal"] = 0
        df.loc[(df["signal"] == -1) & (df["signal"].shift(1) == -1), "signal"] = 0

        df["sl_distance"] = ta.atr(df["high"], df["low"], df["close"], length=p["atr_period"]) * p["sl_atr_mult"]
        df["tp_distance"] = ta.atr(df["high"], df["low"], df["close"], length=p["atr_period"]) * p["tp_atr_mult"]

        return df

    def validate_params(self) -> bool:
        return self.params["donchian_period"] > 0 and self.params["adx_min"] >= 0
