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
            "atr_period":         10,
            "atr_multiplier":     1.1,   # Spike when ATR > 1.1x rolling avg
            "momentum_period":    5,
            "tp_atr_mult":        2.0,
            "sl_atr_mult":        1.0,
            "min_volatility_bars": 1,
            "adx_min":            25,
            "trend_period":       200,
            "stoch_k":            14,
            "stoch_d":            3,
            "atr_avg_p":          20,
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

        df['atr']     = ta.atr(df['high'], df['low'], df['close'],
                               self.params["atr_period"])
        df['atr_avg'] = df['atr'].rolling(self.params.get("atr_avg_p", 20)).mean()
        
        # Stochastic confirmation
        stoch = ta.stoch(df['high'], df['low'], df['close'], k=self.params.get("stoch_k", 14), d=self.params.get("stoch_d", 3))
        df['stoch_k'] = stoch.iloc[:, 0]
        df['stoch_d'] = stoch.iloc[:, 1]

        df['vol_spike'] = df['atr'] > (df['atr_avg'] * self.params["atr_multiplier"])

        df['momentum'] = df['close'] - df['close'].shift(self.params["momentum_period"])
        
        # ADX gate
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]
        
        # Trend filter
        df['trend_ma'] = ta.sma(df['close'], length=self.params.get("trend_period", 200))

        df['signal'] = 0

        buy_signal = (
            (df['vol_spike']) &
            (df['momentum'] > 0) &
            (df['close'] > df['open']) &
            (df['adx'] >= self.params.get("adx_min", 25)) &
            (df['close'] > df['trend_ma']) &
            (df['stoch_k'] > df['stoch_d']) &
            (df['atr'] > df['atr_avg'])
        )
        sell_signal = (
            (df['vol_spike']) &
            (df['momentum'] < 0) &
            (df['close'] < df['open']) &
            (df['adx'] >= self.params.get("adx_min", 25)) &
            (df['close'] < df['trend_ma']) &
            (df['stoch_k'] < df['stoch_d']) &
            (df['atr'] > df['atr_avg'])
        )

        # Layer 2 — Candle body ratio (critical for vol breakout — avoids wick spikes)
        buy_signal, sell_signal = self.apply_body_ratio_filter(df, buy_signal, sell_signal,
                                                               min_ratio=self.params.get('body_ratio_min', 0.60))
        # Layer 3 — ATR ceiling (this strategy inverts if ATR is extreme — use tighter 3.0)
        buy_signal, sell_signal = self.apply_atr_ceiling(df, buy_signal, sell_signal)

        df.loc[buy_signal,  'signal'] = 1
        df.loc[sell_signal, 'signal'] = -1

        # Layer 4 — Cooldown suppression
        df = self.apply_cooldown(df)
        return df

    def validate_params(self) -> bool:
        return (self.params.get("atr_period", 0) > 0 and
                self.params.get("atr_multiplier", 0) > 0 and
                self.params.get("tp_atr_mult", 0) > 0 and
                self.params.get("sl_atr_mult", 0) > 0)
