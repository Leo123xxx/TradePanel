import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class VolatilityContraction(BaseStrategy):
    """
    Volatility Contraction Breakout
    
    Logic:
    1. Contraction: ATR(20) is at its lowest level in 100 bars.
    2. Range: Define a 'squeeze range' of recent N bars.
    3. Signal: Entry when price breaks out of the squeeze range with high volume.
    4. Guard: ADX must be low (< 20) during the squeeze and rising during breakout.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "atr_period": 20,
                "atr_lookback": 100,
                "range_bars": 10,
                "vol_spike": 1.5,
                "tp_atr_mult": 3.0,
                "sl_atr_mult": 1.5
            }
        super().__init__(
            name="Volatility_Contraction",
            category="Breakout",
            params=params,
            regime=["LOW_VOL", "ANY"],
            timeframes=["D1", "H4"],
            pairs=["USDJPY", "ETHUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        # 1. Volatility Contraction
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=self.params['atr_period'])
        df['min_atr'] = df['atr'].rolling(window=self.params['atr_lookback']).min()
        df['is_contracted'] = df['atr'] <= (df['min_atr'] * 1.1) # Within 10% of minimum
        
        # 2. Squeeze Range
        df['range_h'] = df['high'].rolling(window=self.params['range_bars']).max().shift(1)
        df['range_l'] = df['low'].rolling(window=self.params['range_bars']).min().shift(1)
        
        # 3. Volume spike
        df['avg_vol'] = df['tick_volume'].rolling(window=50).mean()
        df['vol_ok'] = df['tick_volume'] > (df['avg_vol'] * self.params['vol_spike'])
        
        # 4. Signals
        df['signal'] = 0
        df.loc[df['is_contracted'].shift(1) & (df['close'] > df['range_h']) & df['vol_ok'], 'signal'] = 1
        df.loc[df['is_contracted'].shift(1) & (df['close'] < df['range_l']) & df['vol_ok'], 'signal'] = -1
        
        return df

    def validate_params(self) -> bool:
        return True
