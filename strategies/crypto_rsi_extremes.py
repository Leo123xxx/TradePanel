"""
strategies/crypto_rsi_extremes.py
===================================
Crypto RSI Extremes — Mean Reversion at RSI Extremes with BB Confirmation.

Designed for BTC/ETH corrections within bull markets and recovery from oversold
conditions. Bitcoin and Ethereum regularly drop 20–40% during bull markets before
recovering; this strategy aims to catch those entries.

Signal logic:
  Buy  (1):  RSI < oversold_threshold (default 25) AND close <= lower Bollinger Band
             AND ADX < adx_max (not in vertical sell-off — ranges and corrections only)
             AND tick_volume spike (confirms genuine selling climax, not noise)
  Sell (-1): RSI > overbought_threshold (default 75) AND close >= upper Bollinger Band
             AND ADX < adx_max (ranging/correction, not breakout)
             AND tick_volume spike

Why RSI + BB confirmation?
  RSI alone fires too often in trending crypto markets (RSI stays oversold for weeks).
  Adding BB lower/upper band touch requires price to have actually extended
  significantly before entry — higher hit rate on mean reversion.

ADX guard:
  When ADX > 35, crypto is in a strong trend and mean reversion is dangerous.
  The guard ensures we only take reversion trades in corrections, not waterfall declines.

Volume filter:
  Capitulation lows and blow-off tops typically coincide with a volume spike.
  tick_volume > vol_spike_mult × 20-bar average is the filter.
  NOTE: tick_volume on MT5 CFDs is tick count, not real dollar volume.
"""

import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["BTCUSD", "ETHUSD", "XAUUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]


class CryptoRSIExtremesStrategy(BaseStrategy):
    """
    RSI Extremes + Bollinger Band + Volume spike mean reversion.
    Primary application: BTCUSD, ETHUSD corrections.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "rsi_period":           14,
                "rsi_oversold":         25,    # Tighter than standard 30 — reduces false signals
                "rsi_overbought":       75,    # Tighter than standard 70
                "bb_period":            20,
                "bb_deviation":          2.0,
                "adx_max":             35,    # Only trade when market is NOT in a strong trend
                "vol_spike_mult":       1.5,   # Require vol > 1.5x 20-bar average
                "atr_period":          14,
                "tp_atr_mult":          2.5,   # Generous TP for crypto bounces
                "sl_atr_mult":          1.0,
            }
        super().__init__(
            name="Crypto_RSI_Extremes",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "CHOPPY", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS,
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        RSI extremes + BB band touch + volume spike + ADX guard.
        """
        df = data.copy()

        rsi_p       = self.params.get("rsi_period",    14)
        rsi_os      = self.params.get("rsi_oversold",  25)
        rsi_ob      = self.params.get("rsi_overbought", 75)
        bb_p        = self.params.get("bb_period",     20)
        bb_std      = self.params.get("bb_deviation",   2.0)
        adx_max     = self.params.get("adx_max",       35)
        vol_mult    = self.params.get("vol_spike_mult", 1.5)

        # ── RSI ───────────────────────────────────────────────────────────────
        df['rsi'] = ta.rsi(df['close'], length=rsi_p)

        # ── Bollinger Bands ───────────────────────────────────────────────────
        bb_df = ta.bbands(df['close'], length=bb_p, std=bb_std)
        df['bb_lower'] = bb_df[f"BBL_{bb_p}_{bb_std}"]
        df['bb_upper'] = bb_df[f"BBU_{bb_p}_{bb_std}"]

        # ── ADX ───────────────────────────────────────────────────────────────
        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # ── Volume spike filter ───────────────────────────────────────────────
        df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
        vol_spike     = df['tick_volume'] > (df['vol_avg'] * vol_mult)

        # ── Market regime guard ───────────────────────────────────────────────
        not_trending = df['adx'] < adx_max

        # ── Signals ───────────────────────────────────────────────────────────
        df['signal'] = 0

        long_cond = (
            (df['rsi']   <= rsi_os) &
            (df['close'] <= df['bb_lower']) &
            not_trending &
            vol_spike
        )

        short_cond = (
            (df['rsi']   >= rsi_ob) &
            (df['close'] >= df['bb_upper']) &
            not_trending &
            vol_spike
        )

        df.loc[long_cond,  'signal'] =  1
        df.loc[short_cond, 'signal'] = -1

        # Suppress consecutive duplicates
        df.loc[(df['signal'] ==  1) & (df['signal'].shift(1) ==  1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return (
            self.params.get("rsi_oversold", 0) < self.params.get("rsi_overbought", 100) and
            self.params.get("bb_deviation", 0) > 0 and
            self.params.get("adx_max", 0) > 0
        )
