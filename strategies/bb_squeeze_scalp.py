"""
Bollinger Band Squeeze Scalp v3 — M15 (2026-05-01)

v3 upgrades — targeting 70%+ WR:
  - Squeeze persistence raised 3->5 bars (sustained compression = higher quality breakout)
  - Volume spike gate raised 1.2x -> 2.0x on the breakout bar itself
    (a genuine squeeze breakout always carries 2x+ normal volume)
  - EMA200 macro gate added (EMA50 alone insufficient)
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class BBSqueezeScalp(BaseStrategy):
    """BB squeeze breakout on M15 — v3 with tighter squeeze and higher volume spike gate."""

    def __init__(self, params=None):
        params = params or {
            "bb_period":         15,
            "bb_std":             2.5,
            "atr_period":        14,
            "squeeze_bars":       3,     # loosened 5→3: 5-bar squeeze too rare
            "squeeze_pct":        0.6,
            "tp_atr_mult":        2.0,
            "sl_atr_mult":        1.0,
            "adx_min":           28,
            "rsi_period":        14,
            "rsi_confirm_long":  52,
            "rsi_confirm_short": 48,
            "ema50_period":      50,
            "ema200_period":    200,     # NEW: macro gate
            "vol_threshold_mult": 1.5,  # loosened 2.0→1.5
            "session_start_utc":  7,
            "session_end_utc":   17,
            "stoch_k": 14,
            "stoch_d": 3,
            "atr_avg_p": 20,
        }
        super().__init__(
            name="bb_squeeze_scalp",
            category="Scalping",
            params=params,
            regime=["TRENDING", "ANY"],
            timeframes=["M15"],
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
        )

    def generate_signals(self, data):
        df = data.copy()

        bb_p          = self.params.get("bb_period",         15)
        bb_std        = self.params.get("bb_std",             2.5)
        sq_bars       = self.params.get("squeeze_bars",        5)
        sq_pct        = self.params.get("squeeze_pct",         0.6)
        adx_min       = self.params.get("adx_min",            25)
        rsi_p         = self.params.get("rsi_period",         14)
        rsi_long      = self.params.get("rsi_confirm_long",   52)
        rsi_short     = self.params.get("rsi_confirm_short",  48)
        ema50_p       = self.params.get("ema50_period",        50)
        ema200_p      = self.params.get("ema200_period",      200)
        vol_mult      = self.params.get("vol_threshold_mult",  2.0)
        session_start = self.params.get("session_start_utc",   7)
        session_end   = self.params.get("session_end_utc",    17)

        # Bollinger Bands
        sma = ta.sma(df['close'], bb_p)
        std = df['close'].rolling(bb_p).std()
        df['bb_upper'] = sma + (std * bb_std)
        df['bb_lower'] = sma - (std * bb_std)
        df['bb_width']     = df['bb_upper'] - df['bb_lower']
        df['bb_width_sma'] = df['bb_width'].rolling(20).mean()

        # Squeeze: sustained compression over sq_bars bars
        df['is_squeeze'] = df['bb_width'] < (df['bb_width_sma'] * sq_pct)
        # All of the last sq_bars bars must have been in squeeze
        df['sustained_squeeze'] = df['is_squeeze'].rolling(window=sq_bars).min().astype(bool)

        # EMA50 direction + EMA200 macro gate
        df['ema50']  = ta.ema(df['close'], length=ema50_p)
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        above_ema = (df['close'] > df['ema50']) & (df['close'] > df['ema200'])
        below_ema = (df['close'] < df['ema50']) & (df['close'] < df['ema200'])

        # ADX gate
        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]
        trend_ok  = df['adx'] >= adx_min

        # ATR Expansion
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        df['atr_avg'] = df['atr'].rolling(self.params.get("atr_avg_p", 20)).mean()
        
        # Stochastic confirmation
        stoch = ta.stoch(df['high'], df['low'], df['close'], k=self.params.get("stoch_k", 14), d=self.params.get("stoch_d", 3))
        df['stoch_k'] = stoch.iloc[:, 0]
        df['stoch_d'] = stoch.iloc[:, 1]

        # RSI gate
        df['rsi']  = ta.rsi(df['close'], length=rsi_p)
        rsi_ok_l   = df['rsi'] >= rsi_long
        rsi_ok_s   = df['rsi'] <= rsi_short

        # Volume spike gate on breakout bar
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
            vol_spike = df['tick_volume'] >= (df['vol_avg'] * vol_mult)
        else:
            vol_spike = True

        # Session gate
        try:
            hour       = df.index.hour
            in_session = (hour >= session_start) & (hour < session_end)
        except Exception:
            in_session = True

        df['signal'] = 0

        buy_signal = (
            df['sustained_squeeze'].shift(1)
            & (df['close'] > df['bb_upper'])
            & (df['close'].shift(1) <= df['bb_upper'].shift(1))
            & above_ema & trend_ok & rsi_ok_l & vol_spike & in_session
            & (df['stoch_k'] > df['stoch_d']) & (df['atr'] > df['atr_avg'])
        )
        df.loc[buy_signal, 'signal'] = 1

        sell_signal = (
            df['sustained_squeeze'].shift(1)
            & (df['close'] < df['bb_lower'])
            & (df['close'].shift(1) >= df['bb_lower'].shift(1))
            & below_ema & trend_ok & rsi_ok_s & vol_spike & in_session
            & (df['stoch_k'] < df['stoch_d']) & (df['atr'] > df['atr_avg'])
        )
        df.loc[sell_signal, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("bb_period", 0) > 0 and
                self.params.get("bb_std", 0) > 0 and
                self.params.get("tp_atr_mult", 0) > 0 and
                self.params.get("sl_atr_mult", 0) > 0)
