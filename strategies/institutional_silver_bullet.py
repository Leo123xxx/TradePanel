import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class InstitutionalSilverBullet(BaseStrategy):
    """
    ICT Silver Bullet Strategy (Institutional Flow)
    
    Logic:
    1. Timed Entry Window: 10:00-11:00 AM NY, 2:00-3:00 AM NY, or 2:00-3:00 PM NY.
    2. Liquidity Sweep: Price must sweep a recent high/low (liquidity pool).
    3. Market Structure Shift (MSS): Price must break the previous swing high/low in the reversal direction.
    4. Fair Value Gap (FVG): Entry on a retracement into a 5-minute or 15-minute FVG.
    
    Note: Time is adjusted based on 'ny_offset' parameter to align with server time.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ny_offset_hours": 7,      # Adjust based on broker server time (e.g., MT5 is usually UTC+2/3)
                "lookback_sweep": 20,      # Look back this many bars for liquidity pools
                "fvg_min_size_pct": 0.0001, # Minimum size of FVG as % of price
                "risk_reward": 2.0,        # Fixed RR for simplicity
                "atr_period": 14
            }
        super().__init__(
            name="Institutional_Silver_Bullet",
            category="SMC",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M5", "M15"],
            pairs=["XAUUSD", "GBPUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        offset = self.params.get("ny_offset_hours", 7)
        lookback = self.params.get("lookback_sweep", 20)
        
        # 1. Time Session Detection (Simplified to Hour of Day)
        # Assuming NY 10:00-11:00 is (10 + offset) in server time
        df['hour'] = df.index.hour
        
        # Silver Bullet Windows (NY Time): 
        # 02:00-03:00 (London), 10:00-11:00 (NY AM), 14:00-15:00 (NY PM)
        sb_windows = [2, 10, 14]
        df['is_sb_window'] = df['hour'].apply(lambda x: (x - offset) % 24 in sb_windows)

        # 2. Identify Liquidity Levels (High/Low of previous lookback)
        df['prev_high'] = df['high'].rolling(window=lookback).max().shift(1)
        df['prev_low'] = df['low'].rolling(window=lookback).min().shift(1)
        
        # 3. Detect Sweeps
        df['swept_high'] = df['high'] > df['prev_high']
        df['swept_low'] = df['low'] < df['prev_low']
        
        # 4. Market Structure Shift (Simplified: Reversal from sweep)
        # A buy signal happens if we swept low and then close above the previous bar's high
        df['mss_buy'] = (df['swept_low'].shift(1)) & (df['close'] > df['high'].shift(1))
        df['mss_sell'] = (df['swept_high'].shift(1)) & (df['close'] < df['low'].shift(1))
        
        # 5. Fair Value Gap (FVG)
        # Bullish FVG: Low of Bar 3 > High of Bar 1
        df['bull_fvg'] = (df['low'] > df['high'].shift(2))
        # Bearish FVG: High of Bar 3 < Low of Bar 1
        df['bear_fvg'] = (df['high'] < df['low'].shift(2))
        
        # 6. Final Signal
        df['signal'] = 0
        
        # Entry logic: Within SB window AND (MSS + FVG)
        df.loc[df['is_sb_window'] & df['mss_buy'] & df['bull_fvg'], 'signal'] = 1
        df.loc[df['is_sb_window'] & df['mss_sell'] & df['bear_fvg'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
