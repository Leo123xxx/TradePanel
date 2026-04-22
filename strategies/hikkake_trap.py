import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class HikkakeTrap(BaseStrategy):
    """
    Hikkake Inside Bar Trap (Mean Reversion / Price Action)
    
    Logic:
    1. Detect Inside Bar (Bar 0).
    2. Bar +1 or +2 breaks out of Bar 0 (False breakout).
    3. Price then reverses and breaks the opposite side of Bar 0.
    4. Entry: On opposite breakout.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "lookback_bars": 3,
                "atr_period": 14,
                "tp_atr_mult": 2.0,
                "sl_atr_mult": 1.5
            }
        super().__init__(
            name="Hikkake_Trap",
            category="Mean Reversion",
            params=params,
            regime=["CHOPPY", "RANGING"],
            timeframes=["H4", "D1"],
            pairs=["BTCUSD", "ETHUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 1. Inside Bar Detection
        df['is_ib'] = (df['high'] < df['high'].shift(1)) & (df['low'] > df['low'].shift(1))
        
        # 2. Store IB levels
        df['ib_h'] = df['high'].where(df['is_ib']).ffill()
        df['ib_l'] = df['low'].where(df['is_ib']).ffill()
        
        # 3. Detect False Breakouts (Simplified Hikkake)
        # Hikkake Buy: IB high broken then price falls but stays above IB low? 
        # Actually standard Hikkake: 
        #   Bullish: IB -> Lower break -> Return and break High of IB.
        #   Bearish: IB -> Upper break -> Return and break Low of IB.
        
        # Check if we broke low of IB recently
        df['broke_l'] = (df['low'] < df['ib_l']) & (~df['is_ib'])
        df['broke_h'] = (df['high'] > df['ib_h']) & (~df['is_ib'])
        
        # Signal Buy: We broke Low within last 3 bars, now we broke High
        df['recent_broke_l'] = df['broke_l'].rolling(window=3).max().shift(1).fillna(0).astype(bool)
        df['recent_broke_h'] = df['broke_h'].rolling(window=3).max().shift(1).fillna(0).astype(bool)
        
        df['condition_buy'] = df['recent_broke_l'] & (df['close'] > df['ib_h'])
        df['condition_sell'] = df['recent_broke_h'] & (df['close'] < df['ib_l'])
        
        df['signal'] = 0
        df.loc[df['condition_buy'], 'signal'] = 1
        df.loc[df['condition_sell'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
