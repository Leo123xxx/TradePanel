import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy

class NakedPriceAction(BaseStrategy):
    """
    Naked Price Action (Engulfing at Support/Resistance)
    
    Logic:
    1. Support/Resistance: Identify recent swing highs and lows as levels.
    2. Confirmation: Wait for a bullish/bearish engulfing candle at These levels.
    3. Signal: Entry on engulfing close.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "level_lookback": 50,
                "engulf_buffer_pct": 0.05,
                "tp_atr_mult": 2.0,
                "sl_atr_mult": 1.5
            }
        super().__init__(
            name="Naked_Price_Action",
            category="Price Action",
            params=params,
            regime=["ANY", "RANGING"],
            timeframes=["H4", "D1"],
            pairs=["EURUSD", "GBPUSD", "XAUUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        lookback = self.params.get("level_lookback", 50)
        
        # 1. Identify S/R Levels (Horizontal)
        df['rolling_h'] = df['high'].rolling(window=lookback).max().shift(1)
        df['rolling_l'] = df['low'].rolling(window=lookback).min().shift(1)
        
        # 2. Engulfing Detection
        df['is_bull_engulfing'] = (df['close'] > df['open']) & \
                                   (df['open'] < df['close'].shift(1)) & \
                                   (df['close'] > df['open'].shift(1)) & \
                                   (df['open'].shift(1) > df['close'].shift(1))

        df['is_bear_engulfing'] = (df['close'] < df['open']) & \
                                    (df['open'] > df['close'].shift(1)) & \
                                    (df['close'] < df['open'].shift(1)) & \
                                    (df['open'].shift(1) < df['close'].shift(1))
                                    
        # 3. Signals (Engulfing at or near levels)
        # We define 'at level' as within 10% of ATR of the level
        import ta_compat as ta
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        df['at_support'] = (df['low'] - df['rolling_l']).abs() < (df['atr'] * 0.5)
        df['at_resistance'] = (df['high'] - df['rolling_h']).abs() < (df['atr'] * 0.5)
        
        df['signal'] = 0
        df.loc[df['at_support'] & df['is_bull_engulfing'], 'signal'] = 1
        df.loc[df['at_resistance'] & df['is_bear_engulfing'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
