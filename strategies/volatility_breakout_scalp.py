"""
Volatility Breakout Scalp - 1m/5m scalping
Enters on ATR spike with momentum confirmation.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class VolatilityBreakoutScalp(BaseStrategy):
    """Scalps volatility breakouts on lower timeframes."""
    
    def __init__(self, params=None):
        params = params or {
            "atr_period": 10,
            "atr_multiplier": 1.5,   # Entry when ATR spikes
            "momentum_period": 5,
            "tp_atr_mult": 0.95,
            "sl_atr_mult": 0.45,
            "min_volatility_bars": 2,
        }
        super().__init__(
            name="volatility_breakout_scalp",
            category="Scalping",
            params=params,
            regime=["HIGH_VOL", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )
    
    def generate_signals(self, data):
        """Generate signals on volatility spike breakout."""
        df = data.copy()
        
        # ATR
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], 
                           self.params["atr_period"])
        df['atr_avg'] = df['atr'].rolling(20).mean()
        
        # Volatility spike detection
        df['vol_spike'] = df['atr'] > (df['atr_avg'] * self.params["atr_multiplier"])
        
        # Momentum
        df['momentum'] = df['close'] - df['close'].shift(self.params["momentum_period"])
        
        # Signal generation
        df['signal'] = 0
        
        # BUY: Volatility spike + positive momentum
        buy_signal = (
            (df['vol_spike']) &
            (df['momentum'] > 0) &
            (df['close'] > df['open'])
        )
        df.loc[buy_signal, 'signal'] = 1
        
        # SELL: Volatility spike + negative momentum
        sell_signal = (
            (df['vol_spike']) &
            (df['momentum'] < 0) &
            (df['close'] < df['open'])
        )
        df.loc[sell_signal, 'signal'] = -1
        
        return df[['signal']]

