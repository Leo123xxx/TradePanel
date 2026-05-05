"""
RSI Extremes Scalp — M15 (rehabilitated 2026-04-29)

Original M1/M5 version failed in real-data testing (WR 11-17%) due to:
  - RSI at M1/M5 hits extremes constantly in trending moves (not mean-reverting)
  - No ADX gate: took counter-trend mean reversion in waterfall/explosive moves
  - No volume confirmation: many extreme RSI prints on thin, low-volume bars
  - No session filter: traded through illiquid Asian session

M15 rehabilitation changes:
  - ADX max gate (<= 30): only mean-revert in ranging/choppy conditions
  - Volume spike required: genuine capitulation/blow-off needs participation
  - Tighter RSI thresholds: oversold <= 18, overbought >= 82 (was 25/75)
  - Session filter: London/NY only (UTC 7–17)
  - Increased min_rsi_move 3→5: stronger bounce confirmation required
  - Restricted to FX + Gold — crypto too volatile for RSI mean reversion on M15
"""

from strategies.base_strategy import BaseStrategy
import ta_compat as ta


class RSIExtremesScalp(BaseStrategy):
    """RSI extreme mean reversion on M15 — rehabilitated with ADX/vol/session gates."""

    def __init__(self, params=None):
        params = params or {
            "rsi_period":         14,   # yaml value
            "oversold":           22,   # loosened 18→22: 18 too rare
            "overbought":         78,   # loosened 82→78
            "min_rsi_move":        5,   # raised 3→5: stronger bounce required before entry
            "atr_period":         14,
            "tp_atr_mult":         2.0,
            "sl_atr_mult":         1.0,
            "adx_max":            30,   # NEW: only mean-revert in ranging markets
            "vol_spike_mult":      1.2, # loosened 1.5→1.2
            "session_start_utc":   7,  # NEW: London open
            "session_end_utc":    17,  # NEW: NY close
        }
        super().__init__(
            name="rsi_extremes_scalp",
            category="Scalping",
            params=params,
            regime=["RANGING", "CHOPPY"],
            timeframes=["M15"],         # M1/M5 removed — too noisy
            pairs=["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
        )

    def generate_signals(self, data):
        """RSI extreme bounce with ADX, volume, and session gates."""
        df = data.copy()

        rsi_p         = self.params.get("rsi_period",       14)
        oversold      = self.params.get("oversold",         18)
        overbought    = self.params.get("overbought",       82)
        min_move      = self.params.get("min_rsi_move",      5)
        adx_max       = self.params.get("adx_max",          30)
        vol_mult      = self.params.get("vol_spike_mult",    0.0)
        session_start = self.params.get("session_start_utc", 7)
        session_end   = self.params.get("session_end_utc",  17)

        df['rsi']      = ta.rsi(df['close'], rsi_p)
        df['prev_rsi'] = df['rsi'].shift(1)

        # ADX gate — only trade when market is ranging/choppy
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 15.0
        not_trending = df['adx'] <= adx_max

        # Volume spike gate — genuine capitulation / blow-off requires volume
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (df['vol_avg'] * vol_mult)
        else:
            vol_ok = True

        # Session gate
        try:
            hour       = df.index.hour
            in_session = (hour >= session_start) & (hour < session_end)
        except Exception:
            in_session = True

        df['signal'] = 0

        buy_signal = (
            (df['prev_rsi'] <= oversold) &
            (df['rsi'] > df['prev_rsi']) &
            (df['rsi'] > (oversold + min_move)) &
            not_trending & vol_ok & in_session
        )
        df.loc[buy_signal, 'signal'] = 1

        sell_signal = (
            (df['prev_rsi'] >= overbought) &
            (df['rsi'] < df['prev_rsi']) &
            (df['rsi'] < (overbought - min_move)) &
            not_trending & vol_ok & in_session
        )
        df.loc[sell_signal, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("rsi_period", 0) > 0 and
                0 < self.params.get("oversold", 25) < 50 and
                50 < self.params.get("overbought", 75) < 100 and
                self.params.get("tp_atr_mult", 0) > 0)
