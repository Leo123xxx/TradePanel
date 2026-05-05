import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
APPROVED_TIMEFRAMES = ["H1", "H4"]

class BBMeanReversionStrategy(BaseStrategy):
    """
    Bollinger Band Mean Reversion — v3 Complete Overhaul.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - ADX max tightened 25->15: only trade in dead-flat ranging markets.
      BB mean reversion in ADX 15-25 markets fails regularly — the band touch is
      often the start of a new leg, not a reversion.
    - BB at 3.0 sigma (from 2.5): only the rarest, most extreme band touches.
      A 3-sigma touch occurs once every 370 bars on average — much higher quality.
    - Volume exhaustion filter: volume must be DECLINING for 2 bars before the
      touch (momentum into the band is fading). A band touch on rising volume
      is a breakout, not a reversion setup.
    - RSI zones tightened: oversold 35->28 max, overbought 65->72 min.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "bb_period":           20,
                "bb_deviation":         3.0,  # raised 2.5->3.0: 3-sigma extremes only
                "rsi_period":          14,
                "rsi_os_low":          10,
                "rsi_os_high":         28,    # tightened 35->28
                "rsi_ob_low":          72,    # tightened 65->72
                "rsi_ob_high":         90,
                "adx_max":             15,    # tightened 25->15: dead-flat ranging only
                "atr_period":          14,
                "tp_atr_mult":          2.0,
                "sl_atr_mult":          1.0,
                "vol_threshold_mult":   1.2,
                "vol_exhaustion_bars":  2,    # NEW: volume must be declining N bars pre-touch
                "ema200_period":       200,
                "session_start_utc":    7,
                "session_end_utc":     17,
            }
        super().__init__(
            name="BB_Mean_Reversion",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        bb_period      = self.params.get("bb_period",            20)
        bb_deviation   = self.params.get("bb_deviation",          3.0)
        rsi_period     = self.params.get("rsi_period",           14)
        rsi_os_low     = self.params.get("rsi_os_low",           10)
        rsi_os_high    = self.params.get("rsi_os_high",          28)
        rsi_ob_low     = self.params.get("rsi_ob_low",           72)
        rsi_ob_high    = self.params.get("rsi_ob_high",          90)
        adx_max        = self.params.get("adx_max",              15)
        atr_period     = self.params.get("atr_period",           14)
        vol_mult       = self.params.get("vol_threshold_mult",    1.2)
        vol_exhaust_n  = self.params.get("vol_exhaustion_bars",   2)
        ema200_p       = self.params.get("ema200_period",        200)
        sess_start     = self.params.get("session_start_utc",     7)
        sess_end       = self.params.get("session_end_utc",      17)

        # Bollinger Bands at 3-sigma
        sma = ta.sma(df['close'], length=bb_period)
        std = df['close'].rolling(bb_period).std()
        df['bb_upper'] = sma + std * bb_deviation
        df['bb_lower'] = sma - std * bb_deviation
        df['bb_mid']   = sma

        df['atr']     = ta.atr(df['high'], df['low'], df['close'], length=atr_period)
        df['atr_sma'] = df['atr'].rolling(20).mean()
        df['rsi']     = ta.rsi(df['close'], length=rsi_period)

        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df.iloc[:, 0]

        # EMA200 macro alignment
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']
        macro_down = df['close'] < df['ema200']

        # ATR confirmation on reversal bar
        vol_ok  = df['atr'] >= df['atr_sma'] * vol_mult

        # Dead-flat ranging gate
        ranging = df['adx'] < adx_max

        # Volume exhaustion: volume must be decreasing in the N bars BEFORE the touch
        # vol_exhaust_n=2: tick_volume[i-1] < tick_volume[i-2] < tick_volume[i-3]
        if vol_exhaust_n >= 1 and 'tick_volume' in df.columns:
            vol_declining = df['tick_volume'].shift(1) < df['tick_volume'].shift(2)
            for k in range(2, vol_exhaust_n + 1):
                vol_declining = vol_declining & (df['tick_volume'].shift(k) < df['tick_volume'].shift(k + 1))
        else:
            vol_declining = True

        # Session gate
        try:
            hour       = df.index.hour
            in_session = (hour >= sess_start) & (hour < sess_end)
        except Exception:
            in_session = True

        df['signal'] = 0

        long_cond = (
            (df['low'] <= df['bb_lower']) &
            vol_ok &
            vol_declining &
            ranging &
            macro_up &
            in_session &
            df['rsi'].between(rsi_os_low, rsi_os_high)
        )
        short_cond = (
            (df['high'] >= df['bb_upper']) &
            vol_ok &
            vol_declining &
            ranging &
            macro_down &
            in_session &
            df['rsi'].between(rsi_ob_low, rsi_ob_high)
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Dedup consecutive signals
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return (self.params.get("bb_period", 0) > 0 and
                self.params.get("bb_deviation", 0) > 0 and
                self.params.get("tp_atr_mult", 0) > 0)
