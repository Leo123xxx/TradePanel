import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class RSIBounceStrategy(BaseStrategy):
    """
    RSI Mean Reversion Strategy — v3 Complete Overhaul.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - ADX max tightened 30->18: only trade in strictly ranging, choppy markets.
      Divergence/mean reversion in ADX 18-30 markets has inconsistent follow-through.
    - RSI extremes tightened to 15/85 (from 20/80): only trade the deepest, most
      statistically reliable RSI extremes. 15/85 occurs far less often but has
      significantly higher reversion probability.
    - Confirmation candle filter: after the RSI crossover, the NEXT bar must be a
      bullish close (close > open for longs) or bearish close (close < open for shorts).
      This one-bar confirmation dramatically reduces false crossover entries.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period":          14,
                "oversold":            15,    # tightened 20->15: deepest extremes only
                "overbought":          85,    # tightened 80->85: deepest extremes only
                "ema_trend":          200,
                "adx_max":             18,    # tightened 30->18: strictly ranging
                "vol_threshold_mult":   1.2,
                "atr_period":          14,
                "session_start_utc":    7,
                "session_end_utc":     17,
                "tp_atr_mult":          2.0,
                "sl_atr_mult":          1.0,
                "use_partial_tp":       False,
            }
        super().__init__(
            name="RSI_Bounce",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        rsi_period       = self.params.get("rsi_period",         14)
        overbought       = self.params.get("overbought",         85)
        oversold         = self.params.get("oversold",           15)
        ema_trend_period = self.params.get("ema_trend",         200)
        adx_max          = self.params.get("adx_max",            18)
        vol_mult         = self.params.get("vol_threshold_mult",  1.2)
        atr_p            = self.params.get("atr_period",         14)
        sess_start       = self.params.get("session_start_utc",   7)
        sess_end         = self.params.get("session_end_utc",    17)

        # ── Indicators ────────────────────────────────────────────────────────
        df['rsi']       = ta.rsi(df['close'], length=rsi_period)
        df['ema_trend'] = ta.ema(df['close'], length=ema_trend_period)
        df['atr']       = ta.atr(df['high'], df['low'], df['close'], length=atr_p)
        df['atr_avg']   = df['atr'].rolling(20).mean()

        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df.iloc[:, 0]
        except Exception:
            df['adx'] = 15.0

        # ── Gates ─────────────────────────────────────────────────────────────
        in_uptrend   = df['close'] > df['ema_trend']
        in_downtrend = df['close'] < df['ema_trend']
        ranging      = df['adx'] < adx_max
        vol_ok       = df['atr'] >= df['atr_avg'] * vol_mult

        # Confirmation candle: current bar must be bullish (for longs) or bearish (shorts)
        bar_bullish = df['close'] > df['open']
        bar_bearish = df['close'] < df['open']

        # Session gate
        try:
            hour       = df.index.hour
            in_session = (hour >= sess_start) & (hour < sess_end)
        except Exception:
            in_session = True

        # ── Signals: RSI crossover + confirmation candle ───────────────────────
        # RSI crossed back above oversold on PREVIOUS bar — current bar is the confirmation
        rsi_crossed_up   = (df['rsi'].shift(1) > oversold) & (df['rsi'].shift(2) <= oversold)
        rsi_crossed_down = (df['rsi'].shift(1) < overbought) & (df['rsi'].shift(2) >= overbought)

        df['signal'] = 0

        long_cond = (
            in_uptrend &
            ranging &
            vol_ok &
            in_session &
            rsi_crossed_up &
            bar_bullish        # confirmation: current bar closes bullish
        )
        short_cond = (
            in_downtrend &
            ranging &
            vol_ok &
            in_session &
            rsi_crossed_down &
            bar_bearish        # confirmation: current bar closes bearish
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return (self.params.get("rsi_period", 0) > 0 and
                0 < self.params.get("oversold",   15) < 50 and
                50 < self.params.get("overbought", 85) < 100)
