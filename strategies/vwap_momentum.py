import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class VWAPMomentum(BaseStrategy):
    """
    VWAP Momentum Shift (Mean Reversion)
    
    Logic:
    1. Calculate Daily VWAP.
    2. Overextended: Price deviates from VWAP by more than std_dev multiplier.
    3. Reversal: Price shows a reversal candle (High/Low of prev bar taken out).
    4. Target: Mean reversion to VWAP.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "std_dev_mult": 2.0,
                "atr_period": 14,
                "tp_atr_mult": 1.5,
                "sl_atr_mult": 1.5
            }
        super().__init__(
            name="VWAP_Momentum",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "HIGH_VOL"],
            timeframes=["M15", "M30"],
            pairs=["ETHUSD", "XAGUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 1. Daily VWAP Calculation
        df['date'] = df.index.date
        df['pv'] = df['close'] * df['tick_volume']
        
        # Calculate cumulative values per day
        df['cum_pv'] = df.groupby('date')['pv'].cumsum()
        df['cum_v'] = df.groupby('date')['tick_volume'].cumsum()
        df['vwap'] = df['cum_pv'] / df['cum_v']
        
        # 2. Standard Deviation from VWAP
        df['vwap_dist'] = df['close'] - df['vwap']
        df['vwap_std'] = df.groupby('date')['close'].transform(lambda x: x.expanding().std())
        
        # 3. Overextended conditions
        df['is_overbought'] = df['close'] > (df['vwap'] + self.params['std_dev_mult'] * df['vwap_std'])
        df['is_oversold'] = df['close'] < (df['vwap'] - self.params['std_dev_mult'] * df['vwap_std'])
        
        # 4. Signals
        df['signal'] = 0
        # Buy: Oversold + Reversal (prev high taken)
        df.loc[df['is_oversold'].shift(1) & (df['close'] > df['high'].shift(1)), 'signal'] = 1
        # Sell: Overbought + Reversal (prev low taken)
        df.loc[df['is_overbought'].shift(1) & (df['close'] < df['low'].shift(1)), 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
