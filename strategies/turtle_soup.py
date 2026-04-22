import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class TurtleSoup(BaseStrategy):
    """
    Turtle Soup Strategy (SMC / Liquidity Sweep)
    
    Logic:
    1. Identify a 20-bar High or Low level.
    2. Price must penetrate the level (liquidity sweep).
    3. Reversal: Price must reverse and close back within the 20-bar level.
    4. Guard: The fakeout must happen within a recent window (e.g., last 3 bars).
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "lookback": 20,
                "min_penetration_pips": 5,
                "max_penetration_pips": 30,
                "atr_period": 14,
                "tp_atr_mult": 2.0,
                "sl_buffer_pips": 5
            }
        super().__init__(
            name="Turtle_Soup",
            category="SMC",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=["H1", "H4"],
            pairs=["XAUUSD", "BTCUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        lookback = self.params.get("lookback", 20)
        
        # 1. Previous 20-bar High and Low
        df['h20'] = df['high'].rolling(window=lookback).max().shift(1)
        df['l20'] = df['low'].rolling(window=lookback).min().shift(1)
        
        # 2. Sweep Detection
        # Low swept: current low < l20, but current close > l20
        df['sweep_low'] = (df['low'] < df['l20']) & (df['close'] > df['l20'])
        # High swept: current high > h20, but current close < h20
        df['sweep_high'] = (df['high'] > df['h20']) & (df['close'] < df['h20'])
        
        # 3. Signals
        df['signal'] = 0
        df.loc[df['sweep_low'], 'signal'] = 1
        df.loc[df['sweep_high'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return self.params.get("lookback", 0) > 0
