"""
RSI Extremes Scalp - 1m/5m mean reversion scalping
Quick entries on RSI oversold/overbought with bounce confirmation.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class RSIExtremesScalp(BaseStrategy):
    """Scalps RSI extremes for mean reversion on lower timeframes."""
    
    def __init__(self, params=None):
        params = params or {
            "rsi_period": 10,        # Shorter for 1m/5m
            "oversold": 25,          # Aggressive extremes
            "overbought": 75,
            "atr_period": 14,
            "tp_atr_mult": 0.85,
            "sl_atr_mult": 0.4,
            "min_rsi_move": 3,       # RSI must move 3 points from extreme
        }
        super().__init__(
            name="rsi_extremes_scalp",
            category="Scalping",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )
    
    def generate_signals(self, data):
        """Generate signals on RSI extremes bounce."""
        df = data.copy()
        
        # RSI
        df['rsi'] = ta.rsi(df['close'], self.params["rsi_period"])
        
        # ATR for stops/targets
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], 
                           self.params["atr_period"])
        
        # Detect bounces from extremes
        df['prev_rsi'] = df['rsi'].shift(1)
        
        # Signal generation
        df['signal'] = 0
        
        # BUY: RSI oversold bounce (RSI was low, now recovering)
        buy_signal = (
            (df['prev_rsi'] < self.params["oversold"]) &
            (df['rsi'] > df['prev_rsi']) &
            (df['rsi'] > (self.params["oversold"] + self.params["min_rsi_move"]))
        )
        df.loc[buy_signal, 'signal'] = 1
        
        # SELL: RSI overbought bounce (RSI was high, now declining)
        sell_signal = (
            (df['prev_rsi'] > self.params["overbought"]) &
            (df['rsi'] < df['prev_rsi']) &
            (df['rsi'] < (self.params["overbought"] - self.params["min_rsi_move"]))
        )
        df.loc[sell_signal, 'signal'] = -1
        
        return df[['signal']]

