import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class TTMSqueezeStrategy(BaseStrategy):
    """
    TTM Squeeze Strategy (John Carter's Squeeze)
    
    Logic:
      1. Squeeze ON: Bollinger Bands (20, 2.0) are INSIDE Keltner Channels (20, 1.5).
      2. Squeeze OFF: Bollinger Bands move outside Keltner Channels.
      3. Momentum: A smoothed momentum oscillator (linear regression of distance from HL2/SMA mean).
    
    Signals:
      - Long: Squeeze flips from ON to OFF AND Momentum is positive.
      - Short: Squeeze flips from ON to OFF AND Momentum is negative.
    
    Optimized for Crypto:
      - Squeezes on M15/H1 often lead to major breakouts.
      - High reward-to-risk (3:1 or 4:1) recommended.
    """

    def __init__(self, params: dict = None):
        defaults = {
            "bb_period": 20,
            "bb_std": 2.0,
            "kc_period": 20,
            "kc_mult": 1.5,
            "mom_period": 20,
            "mom_smoothing": 20,
            "tp_atr_mult": 3.0,
            "sl_atr_mult": 1.5,
        }
        if params:
            defaults.update(params)
        super().__init__(
            name="TTM_Squeeze",
            category="Breakout",
            params=defaults,
        )

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.params
        df = df.copy()
        df["signal"] = 0

        if len(df) < max(p["bb_period"], p["mom_period"]):
            return df

        # Bollinger Bands
        bb_df = ta.bbands(df["close"], length=p["bb_period"], std=p["bb_std"])
        df["bb_upper"] = bb_df[f"BBU_{p['bb_period']}_{p['bb_std']}"]
        df["bb_lower"] = bb_df[f"BBL_{p['bb_period']}_{p['bb_std']}"]

        # Keltner Channels
        # KC = SMA(period) +/- multiplier * ATR(period)
        df["sma"] = ta.sma(df["close"], length=p["kc_period"])
        df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=p["kc_period"])
        df["kc_upper"] = df["sma"] + (p["kc_mult"] * df["atr"])
        df["kc_lower"] = df["sma"] - (p["kc_mult"] * df["atr"])

        # Squeeze Detection
        df["in_squeeze"] = (df["bb_upper"] < df["kc_upper"]) & (df["bb_lower"] > df["kc_lower"])
        
        # Momentum (Classic TTM Squeeze Momentum)
        # mom = linreg(close - (sma + hl2)/2)
        hl2 = (df["high"] + df["low"]) / 2
        avg = (df["sma"] + hl2) / 2
        val = df["close"] - avg
        # Simple linear regression (slope or fit) -- here we use a simple smoothed version as a proxy
        df["mom"] = ta.sma(val, length=p["mom_period"]) 

        # Signal logic: Squeeze release
        # Current bar is NOT in squeeze, previous bar WAS in squeeze
        squeeze_release = (~df["in_squeeze"]) & (df["in_squeeze"].shift(1))
        
        df["signal"] = 0
        long_cond = squeeze_release & (df["mom"] > 0)
        short_cond = squeeze_release & (df["mom"] < 0)

        df.loc[long_cond, "signal"] = 1
        df.loc[short_cond, "signal"] = -1

        df["sl_distance"] = df["atr"] * p["sl_atr_mult"]
        df["tp_distance"] = df["atr"] * p["tp_atr_mult"]

        return df

    def validate_params(self) -> bool:
        return p["bb_period"] > 0 and p["kc_mult"] > 0
