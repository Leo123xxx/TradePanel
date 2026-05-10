import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class SuperTrendStrategy(BaseStrategy):
    """
    SuperTrend Strategy
    
    Logic:
      1. Calculate ATR (period N).
      2. Upper Band = (High + Low) / 2 + Multiplier * ATR
      3. Lower Band = (High + Low) / 2 - Multiplier * ATR
      4. Trend is UP if price stays above Lower Band, DOWN if below Upper Band.
    
    Signals:
      - Long: Price crosses above the current Upper Band (Trend flip to UP).
      - Short: Price crosses below the current Lower Band (Trend flip to DOWN).
    
    Optimized for Crypto:
      - Higher multipliers (3.0 - 5.0) to filter out noise.
      - Works well on H4 and D1 timeframes.
    """

    def __init__(self, params: dict = None):
        defaults = {
            "atr_period": 10,
            "multiplier": 3.0,
            "adx_min": 25,
            "tp_atr_mult": 4.0,
            "sl_atr_mult": 1.5,
        }
        if params:
            defaults.update(params)
        super().__init__(
            name="SuperTrend",
            category="Trend Following",
            params=defaults,
        )

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        p = self.params
        df = df.copy()
        df["signal"] = 0

        if len(df) < p["atr_period"]:
            return df

        # ATR calculation
        df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=p["atr_period"])
        
        # SuperTrend logic
        hl2 = (df["high"] + df["low"]) / 2
        basic_ub = (hl2 + (p["multiplier"] * df["atr"])).values
        basic_lb = (hl2 - (p["multiplier"] * df["atr"])).values
        close_arr = df["close"].values
        
        final_ub = np.zeros(len(df))
        final_lb = np.zeros(len(df))
        supertrend = np.zeros(len(df))
        trend = np.zeros(len(df)) # 1 for UP, -1 for DOWN

        for i in range(1, len(df)):
            try:
                # Final Upper Band
                if basic_ub[i] < final_ub[i-1] or close_arr[i-1] > final_ub[i-1]:
                    final_ub[i] = basic_ub[i]
                else:
                    final_ub[i] = final_ub[i-1]
                    
                # Final Lower Band
                if basic_lb[i] > final_lb[i-1] or close_arr[i-1] < final_lb[i-1]:
                    final_lb[i] = basic_lb[i]
                else:
                    final_lb[i] = final_lb[i-1]
                
                # SuperTrend
                if i == 1:
                    supertrend[i] = final_ub[i]
                    trend[i] = -1
                else:
                    if supertrend[i-1] == final_ub[i-1]:
                        if close_arr[i] > final_ub[i]:
                            supertrend[i] = final_lb[i]
                            trend[i] = 1
                        else:
                            supertrend[i] = final_ub[i]
                            trend[i] = -1
                    else:
                        if close_arr[i] < final_lb[i]:
                            supertrend[i] = final_ub[i]
                            trend[i] = -1
                        else:
                            supertrend[i] = final_lb[i]
                            trend[i] = 1
            except Exception as e:
                print(f"DEBUG ERROR at i={i}: {e}")
                raise e

        df["supertrend"] = supertrend
        df["trend"] = trend

        # ADX filter
        adx_df = ta.adx(df["high"], df["low"], df["close"], length=14)
        df["adx"] = adx_df["ADX_14"]

        # Signal generation (crossover)
        df["signal"] = 0
        long_cond = (df["trend"] == 1) & (df["trend"].shift(1) == -1) & (df["adx"] > p["adx_min"])
        short_cond = (df["trend"] == -1) & (df["trend"].shift(1) == 1) & (df["adx"] > p["adx_min"])
        
        df.loc[long_cond, "signal"] = 1
        df.loc[short_cond, "signal"] = -1

        df["sl_distance"] = df["atr"] * p["sl_atr_mult"]
        df["tp_distance"] = df["atr"] * p["tp_atr_mult"]

        return df

    def validate_params(self) -> bool:
        return self.params["atr_period"] > 0 and self.params["multiplier"] > 0
