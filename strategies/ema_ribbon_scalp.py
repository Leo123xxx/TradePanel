"""
EMA Ribbon Scalp - 1m/5m scalping
Uses 3 EMAs for quick trend confirmation.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class EMARibbonScalp(BaseStrategy):
    """Scalps with EMA ribbon for trend confirmation on lower timeframes."""
    
    def __init__(self, params=None):
        params = params or {
            "fast_ema": 5,
            "mid_ema": 10,
            "slow_ema": 20,
            "atr_period": 14,
            "tp_atr_mult": 0.85,
            "sl_atr_mult": 0.4,
            "min_ribbon_separation": 0.0005,  # Min separation as % of price
        }
        super().__init__(
            name="ema_ribbon_scalp",
            category="Scalping",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )
    
    def generate_signals(self, data):
        """Generate signals on EMA ribbon alignment."""
        df = data.copy()
        
        # EMA Ribbon
        df['ema_fast'] = ta.ema(df['close'], self.params["fast_ema"])
        df['ema_mid'] = ta.ema(df['close'], self.params["mid_ema"])
        df['ema_slow'] = ta.ema(df['close'], self.params["slow_ema"])
        
        # ATR for stops/targets
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], 
                           self.params["atr_period"])
        
        # Ribbon separation (wider = stronger trend)
        df['ribbon_spread'] = (
            (df['ema_fast'] - df['ema_slow']).abs() / df['close']
        )
        
        # Signal generation
        df['signal'] = 0
        
        # BUY: All EMAs aligned bullish, fast > mid > slow, ribbon spread > min
        buy_signal = (
            (df['ema_fast'] > df['ema_mid']) &
            (df['ema_mid'] > df['ema_slow']) &
            (df['ribbon_spread'] > self.params["min_ribbon_separation"]) &
            (df['close'] > df['ema_fast'])  # Price above ribbon
        )
        df.loc[buy_signal, 'signal'] = 1
        
        # SELL: All EMAs aligned bearish, fast < mid < slow, ribbon spread > min
        sell_signal = (
            (df['ema_fast'] < df['ema_mid']) &
            (df['ema_mid'] < df['ema_slow']) &
            (df['ribbon_spread'] > self.params["min_ribbon_separation"]) &
            (df['close'] < df['ema_fast'])  # Price below ribbon
        )
        df.loc[sell_signal, 'signal'] = -1
        
        return df[['signal']]

