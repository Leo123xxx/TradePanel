import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class ICTJudasSwing(BaseStrategy):
    """
    ICT Judas Swing Strategy (Institutional Flow)
    
    Logic:
    1. Identify the Asian Range (pre-London consolidation).
    2. Look for a "Stop Hunt" (Judas Swing) at London Open (Fakeout of Asian high/low).
    3. Reversal: Price breaks back into the range and reverses the move.
    4. Entry: Market Structure Break (MSB) on M5/M15 timeframe.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "ny_offset_hours": 7,
                "asian_range_start": 20,    # 8:00 PM NY
                "asian_range_end": 2,       # 2:00 AM NY (London Open)
                "judas_window_start": 2,    # 2:00 AM NY
                "judas_window_end": 5,      # 5:00 AM NY
                "fakeout_magnitude_pct": 0.001, 
                "atr_period": 14
            }
        super().__init__(
            name="ICT_Judas_Swing",
            category="SMC",
            params=params,
            regime=["LOW_VOL", "TRENDING"],
            timeframes=["M15", "H1"],
            pairs=["GBPUSD", "EURUSD", "USDJPY"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        offset = self.params.get("ny_offset_hours", 7)
        
        # 1. Define Sessions (Local Time)
        df['hour_ny'] = (df.index.hour - offset) % 24
        
        # 2. Asian Range High/Low
        # This is tricky in a vectorized way. We'll use a expanding max/min reset daily.
        df['date'] = df.index.date
        
        # Identify bars in Asian session
        df['is_asian'] = (df['hour_ny'] >= self.params['asian_range_start']) | (df['hour_ny'] < self.params['asian_range_end'])
        
        # Calculate daily Asian High/Low
        asian_high = df[df['is_asian']].groupby('date')['high'].max()
        asian_low = df[df['is_asian']].groupby('date')['low'].min()
        
        df['asian_h'] = df['date'].map(asian_high)
        df['asian_l'] = df['date'].map(asian_low)
        
        # 3. Judas Window (London Open)
        df['is_judas'] = (df['hour_ny'] >= self.params['judas_window_start']) & (df['hour_ny'] < self.params['judas_window_end'])
        
        vol_p  = self.params.get("vol_lookback", 20)
        vol_m  = self.params.get("vol_threshold_mult", 0.0) # 0 = disabled
        sweep  = self.params.get("liquidity_sweep_pips", 0) # Min pips penetration
        
        # 4. Volume Filter
        df['vol_ma'] = ta.sma(df['tick_volume'], length=vol_p)
        df['vol_ok'] = df['tick_volume'] > (df['vol_ma'] * vol_m) if vol_m > 0 else True
        
        # 5. Fakeout detection (with sweep depth)
        mask_buy = (df['low'] < df['asian_l'] - (sweep * 0.0001)) & (df['close'] > df['asian_l'])
        mask_sell = (df['high'] > df['asian_h'] + (sweep * 0.0001)) & (df['close'] < df['asian_h'])
        
        df['fake_buy'] = df['is_judas'] & mask_buy & df['vol_ok']
        df['fake_sell'] = df['is_judas'] & mask_sell & df['vol_ok']
        
        # 6. Signal
        df['signal'] = 0
        df.loc[df['fake_buy'], 'signal'] = 1
        df.loc[df['fake_sell'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
