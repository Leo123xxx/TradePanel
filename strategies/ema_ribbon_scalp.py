"""
EMA Ribbon Scalp - 1m/5m scalping
Fast EMA crosses mid EMA while mid>slow confirms trend direction.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class EMARibbonScalp(BaseStrategy):
    """Scalps with EMA ribbon — entry on fast-cross-mid with trend confirmation."""

    def __init__(self, params=None):
        params = params or {
            "fast_ema":              5,
            "mid_ema":               10,
            "slow_ema":              20,
            "atr_period":            14,
            "tp_atr_mult":           2.0,
            "sl_atr_mult":           1.0,
            "min_ribbon_separation": 0.0,
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
        """Entry: fast EMA crosses mid EMA while mid > slow (trend established)."""
        df = data.copy()

        df['ema_fast'] = ta.ema(df['close'], self.params["fast_ema"])
        df['ema_mid']  = ta.ema(df['close'], self.params["mid_ema"])
        df['ema_slow'] = ta.ema(df['close'], self.params["slow_ema"])

        df['atr'] = ta.atr(df['high'], df['low'], df['close'],
                           self.params["atr_period"])

        df['ribbon_spread'] = (df['ema_fast'] - df['ema_slow']).abs() / df['close']
        spread_ok = df['ribbon_spread'] > self.params["min_ribbon_separation"]

        df['signal'] = 0

        # BUY: fast just crossed above mid, AND mid is above slow (uptrend confirmed)
        buy_signal = (
            (df['ema_fast'] > df['ema_mid']) &
            (df['ema_fast'].shift(1) <= df['ema_mid'].shift(1)) &
            (df['ema_mid'] > df['ema_slow']) &
            spread_ok
        )
        df.loc[buy_signal, 'signal'] = 1

        # SELL: fast just crossed below mid, AND mid is below slow (downtrend confirmed)
        sell_signal = (
            (df['ema_fast'] < df['ema_mid']) &
            (df['ema_fast'].shift(1) >= df['ema_mid'].shift(1)) &
            (df['ema_mid'] < df['ema_slow']) &
            spread_ok
        )
        df.loc[sell_signal, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("fast_ema", 0) > 0 and
                self.params.get("mid_ema", 0) > self.params.get("fast_ema", 0) and
                self.params.get("slow_ema", 0) > self.params.get("mid_ema", 0) and
                self.params.get("tp_atr_mult", 0) > 0)
