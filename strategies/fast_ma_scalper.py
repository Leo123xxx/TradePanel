"""
Fast MA Crossover Scalper - 1m/5m scalping strategy
Trades quick moving average crossovers with tight stops.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta
import pandas as pd


class FastMAScalper(BaseStrategy):
    """Quick MA crossover scalping on 1m/5m timeframes."""

    def __init__(self, params=None):
        params = params or {
            "fast_period": 5,
            "slow_period": 12,
            "tp_atr_mult": 2.0,
            "sl_atr_mult": 1.0,
            "atr_period": 14,
            "min_adx": 22,
        }
        super().__init__(
            name="fast_ma_scalper",
            category="Scalping",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )

    def generate_signals(self, data):
        """Generate signals on MA crossover."""
        df = data.copy()

        df['fast_ma'] = ta.sma(df['close'], self.params["fast_period"])
        df['slow_ma'] = ta.sma(df['close'], self.params["slow_period"])

        # ADX -- ta_compat returns a DataFrame; extract the first column (ADX line)
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=self.params["atr_period"])
        df['adx'] = adx_df.iloc[:, 0]

        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=self.params["atr_period"])

        df['signal'] = 0

        buy_signal = (
            (df['fast_ma'] > df['slow_ma']) &
            (df['fast_ma'].shift(1) <= df['slow_ma'].shift(1)) &
            (df['adx'] > self.params["min_adx"])
        )
        df.loc[buy_signal, 'signal'] = 1

        sell_signal = (
            (df['fast_ma'] < df['slow_ma']) &
            (df['fast_ma'].shift(1) >= df['slow_ma'].shift(1)) &
            (df['adx'] > self.params["min_adx"])
        )
        df.loc[sell_signal, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("fast_period", 0) > 0 and
                self.params.get("slow_period", 0) > self.params.get("fast_period", 0) and
                self.params.get("tp_atr_mult", 0) > 0 and
                self.params.get("sl_atr_mult", 0) > 0)
