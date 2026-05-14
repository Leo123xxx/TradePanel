"""
MACD Zero-Line Scalp - 1m/5m scalping
Enters on MACD zero-line crosses for trend reversals.
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class MACDZeroScalp(BaseStrategy):
    """Scalps MACD zero-line crossovers on lower timeframes."""

    def __init__(self, params=None):
        params = params or {
            "macd_fast":    8,
            "macd_slow":    17,
            "macd_signal":  9,
            "atr_period":   14,
            "volume_filter": 1.0,
            "adx_min":       25,
            "trend_period":  200,
            "stoch_k":       14,
            "stoch_d":       3,
            "atr_avg_p":     20,
        }
        super().__init__(
            name="macd_zero_scalp",
            category="Scalping",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M1", "M5"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "XAGUSD"]
        )

    def generate_signals(self, data):
        """Generate signals on MACD zero-line crossover."""
        df = data.copy()

        # ta_compat.macd returns DataFrame with cols MACD_f_s_sig, MACDh_..., MACDs_...
        macd_result = ta.macd(df['close'],
                              fast=self.params["macd_fast"],
                              slow=self.params["macd_slow"],
                              signal=self.params["macd_signal"])
        # Extract by position -- col 0 = MACD line, col 1 = histogram, col 2 = signal
        df['macd']       = macd_result.iloc[:, 0]
        df['macd_hist']  = macd_result.iloc[:, 1]
        df['macd_signal'] = macd_result.iloc[:, 2]
        
        # ADX gate
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]
        
        # Trend filter
        df['trend_ma'] = ta.sma(df['close'], length=self.params.get("trend_period", 200))

        df['atr'] = ta.atr(df['high'], df['low'], df['close'], self.params["atr_period"])
        df['atr_avg'] = df['atr'].rolling(self.params.get("atr_avg_p", 20)).mean()
        
        # Stochastic confirmation
        stoch = ta.stoch(df['high'], df['low'], df['close'], k=self.params.get("stoch_k", 14), d=self.params.get("stoch_d", 3))
        df['stoch_k'] = stoch.iloc[:, 0]
        df['stoch_d'] = stoch.iloc[:, 1]

        # Use tick_volume if 'volume' column not present
        vol_col = 'volume' if 'volume' in df.columns else 'tick_volume'
        df['volume_avg'] = df[vol_col].rolling(10).mean()

        df['signal'] = 0

        buy_signal = (
            (df['macd'] > 0) &
            (df['macd'].shift(1) <= 0) &
            (df[vol_col] > (df['volume_avg'] * self.params["volume_filter"])) &
            (df['adx'] >= self.params.get("adx_min", 25)) &
            (df['close'] > df['trend_ma']) &
            (df['stoch_k'] > df['stoch_d']) &
            (df['atr'] > df['atr_avg'])
        )
        df.loc[buy_signal, 'signal'] = 1

        sell_signal = (
            (df['macd'] < 0) &
            (df['macd'].shift(1) >= 0) &
            (df[vol_col] > (df['volume_avg'] * self.params["volume_filter"])) &
            (df['adx'] >= self.params.get("adx_min", 25)) &
            (df['close'] < df['trend_ma']) &
            (df['stoch_k'] < df['stoch_d']) &
            (df['atr'] > df['atr_avg'])
        )
        df.loc[sell_signal, 'signal'] = -1

        # Re-derive as Series for helper calls (already assigned above, re-extract for layers)
        buy_s = df['signal'] == 1
        sell_s = df['signal'] == -1
        df['signal'] = 0

        # Layer 1 — VWAP gate
        buy_s, sell_s = self.apply_vwap_gate(df, buy_s, sell_s)
        # Layer 2 — Candle body ratio
        buy_s, sell_s = self.apply_body_ratio_filter(df, buy_s, sell_s)
        # Layer 3 — ATR ceiling (news-spike guard)
        buy_s, sell_s = self.apply_atr_ceiling(df, buy_s, sell_s)

        df.loc[buy_s,  'signal'] = 1
        df.loc[sell_s, 'signal'] = -1

        # Layer 4 — Cooldown suppression
        df = self.apply_cooldown(df)
        return df

    def validate_params(self) -> bool:
        return (self.params.get("macd_fast", 0) > 0 and
                self.params.get("macd_slow", 0) > self.params.get("macd_fast", 0) and
                self.params.get("tp_atr_mult", 0) > 0 and
                self.params.get("sl_atr_mult", 0) > 0)
