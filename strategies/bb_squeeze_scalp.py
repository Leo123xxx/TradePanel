"""
Bollinger Band Squeeze Scalp - 1m/5m scalping
Enters on BB squeeze breakout with tight stops.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class BBSqueezeScalp(BaseStrategy):
    """Scalps Bollinger Band squeezes on lower timeframes."""
    
    def __init__(self, params=None):
        params = params or {
            "bb_period": 15,
            "bb_std": 1.8,           # Tighter bands for scalping
            "atr_period": 14,
            "squeeze_bars": 2,       # Consecutive narrow bars
            "tp_atr_mult": 0.9,
            "sl_atr_mult": 0.35,
        }
        super().__init__(
            name="bb_squeeze_scalp",
            category="Scalping",
            params=params,
            regime=["ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )
    
    def generate_signals(self, data):
        """Generate signals on BB squeeze breakout."""
        df = data.copy()
        
        # Bollinger Bands
        sma = ta.sma(df['close'], self.params["bb_period"])
        std = df['close'].rolling(self.params["bb_period"]).std()
        df['bb_upper'] = sma + (std * self.params["bb_std"])
        df['bb_lower'] = sma - (std * self.params["bb_std"])
        df['bb_mid'] = sma
        
        # Band width
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_width_sma'] = df['bb_width'].rolling(20).mean()
        
        # ATR for entries
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], 
                           self.params["atr_period"])
        
        # Identify squeeze (narrow bands)
        df['is_squeeze'] = df['bb_width'] < (df['bb_width_sma'] * 0.7)
        
        # Signal generation
        df['signal'] = 0
        
        # BUY: Squeeze breakout above upper band
        buy_signal = (
            (df['is_squeeze'].shift(self.params["squeeze_bars"])) &
            (df['close'] > df['bb_upper']) &
            (df['close'].shift(1) <= df['bb_upper'].shift(1))
        )
        df.loc[buy_signal, 'signal'] = 1
        
        # SELL: Squeeze breakout below lower band
        sell_signal = (
            (df['is_squeeze'].shift(self.params["squeeze_bars"])) &
            (df['close'] < df['bb_lower']) &
            (df['close'].shift(1) >= df['bb_lower'].shift(1))
        )
        df.loc[sell_signal, 'signal'] = -1
        
        return df[['signal']]

