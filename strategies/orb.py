import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class ORBStrategy(BaseStrategy):
    """
    Opening Range Breakout (ORB)
    
    Logic:
    1. Define Opening Range (e.g., first 60 mins of London or NY session).
    2. Entry: Buy if price breaks above range high, Sell if price breaks below range low.
    3. Filter: Volume must be > 1.2x average volume.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ny_offset_hours": 7,
                "range_start_ny": 9.5,      # 9:30 AM NY Open
                "range_duration_mins": 60,
                "vol_filter": 1.2,
                "tp_atr_mult": 2.0,
                "sl_atr_mult": 1.0
            }
        super().__init__(
            name="Opening_Range_Breakout",
            category="Breakout",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M15", "H1"],
            pairs=["GBPUSD", "EURUSD", "XAUUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        offset = self.params.get("ny_offset_hours", 7)
        
        # 1. Define Sessions
        df['hour_ny'] = (df.index.hour - offset) + (df.index.minute / 60.0)
        df['date'] = df.index.date
        
        # 2. Identify Range Bars
        start = self.params['range_start_ny']
        end = start + (self.params['range_duration_mins'] / 60.0)
        
        df['is_range'] = (df['hour_ny'] >= start) & (df['hour_ny'] < end)
        
        # Range High/Low
        range_high = df[df['is_range']].groupby('date')['high'].max()
        range_low = df[df['is_range']].groupby('date')['low'].min()
        
        df['rh'] = df['date'].map(range_high)
        df['rl'] = df['date'].map(range_low)
        
        # 3. Post-Range Breakout
        df['is_post_range'] = (df['hour_ny'] >= end) & (df['hour_ny'] < (end + 4)) # Only trade within 4 hours after range
        
        # 4. Volume Filter
        df['avg_vol'] = df['tick_volume'].rolling(window=20).mean()
        df['vol_ok'] = df['tick_volume'] > (df['avg_vol'] * self.params['vol_filter'])
        
        # 5. Signals
        df['signal'] = 0
        df.loc[df['is_post_range'] & (df['close'] > df['rh']) & (df['close'].shift(1) <= df['rh']) & df['vol_ok'], 'signal'] = 1
        df.loc[df['is_post_range'] & (df['close'] < df['rl']) & (df['close'].shift(1) >= df['rl']) & df['vol_ok'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
