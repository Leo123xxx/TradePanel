import pandas as pd
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

APPROVED_PAIRS = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD"]
APPROVED_TIMEFRAMES = ["H4", "D1"]

class RangeBreakoutStrategy(BaseStrategy):
    """
    Range Breakout — Breakout Strategy.

    v2 upgrades (2026-04-29) — targeting 70%+ WR from 56.5%:
    - Confirmation logic changed from OR → AND: both vol spike AND ADX > threshold required.
      The old OR allowed low-volume ADX-only entries that frequently failed.
    - EMA trend filter raised 20→50: EMA20 was too short to define trend on H4/D1;
      EMA50 provides a meaningful momentum baseline.
    - RSI band filter added: only enter when RSI is 40–70 (longs) or 30–60 (shorts).
      Avoids buying into overbought breakouts and selling into oversold breakdowns.
    - ADX minimum raised 20→25: reduces entries in marginal trending conditions.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "consolidation_bars": 15,    # loosened 20→15: shorter consolidation window
                "vol_threshold_mult": 1.3,
                "min_volume_mult":    1.3,   # fallback alias
                "tp_range_mult":      2.5,
                "sl_buffer_pips":    15,
                "adx_min_filter":    20,     # loosened 25→20
                "ema_period":        50,     # raised 20→50 (2026-04-29): EMA20 too noisy
                "ema_filter":        50,     # fallback alias
                "rsi_period":        14,
                "rsi_long_min":      40,     # NEW: long entry only when RSI >= 40 (not oversold bounce)
                "rsi_long_max":      70,     # NEW: long entry only when RSI <= 70 (not overbought)
                "rsi_short_min":     30,     # NEW: short entry only when RSI >= 30 (not oversold)
                "rsi_short_max":     60,     # NEW: short entry only when RSI <= 60 (bearish momentum)
            }
        super().__init__(
            name="Range_Breakout",
            category="Breakout",
            params=params,
            regime=["RANGING", "BREAKOUT", "ANY"],
            timeframes=APPROVED_TIMEFRAMES,
            pairs=APPROVED_PAIRS
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        consolidation_bars = self.params.get("consolidation_bars", 20)
        vol_threshold_mult = self.params.get("vol_threshold_mult", self.params.get("min_volume_mult", 1.3))
        adx_min    = self.params.get("adx_min_filter", 25)
        ema_period = self.params.get("ema_period", self.params.get("ema_filter", 50))
        rsi_p      = self.params.get("rsi_period",   14)
        rsi_lo_min = self.params.get("rsi_long_min",  40)
        rsi_lo_max = self.params.get("rsi_long_max",  70)
        rsi_sh_min = self.params.get("rsi_short_min", 30)
        rsi_sh_max = self.params.get("rsi_short_max", 60)

        # Resistance and Support of N bars before current bar
        df['highest_high'] = df['high'].rolling(window=consolidation_bars).max().shift(1)
        df['lowest_low']   = df['low'].rolling(window=consolidation_bars).min().shift(1)

        # EMA trend baseline (raised to EMA50 — EMA20 was too short to define trend on H4/D1)
        df['ema'] = ta.ema(df['close'], length=ema_period)

        # Volume spike
        df['avg_vol']  = df['tick_volume'].rolling(window=consolidation_bars).mean().shift(1)
        df['vol_spike'] = df['tick_volume'] >= (df['avg_vol'] * vol_threshold_mult)

        # ADX
        adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
        df['adx'] = adx_df["ADX_14"]

        # RSI — band filter to avoid overbought longs and oversold shorts
        df['rsi'] = ta.rsi(df['close'], length=rsi_p)

        # Signal
        df['signal'] = 0

        long_cond = (
            (df['close'] > df['highest_high']) &
            (df['close'] > df['ema']) &
            df['vol_spike'] &                        # AND (was OR) — both confirmations required
            (df['adx'] > adx_min) &                  # AND (was OR)
            (df['rsi'] >= rsi_lo_min) &              # RSI band: not oversold (avoid weak bounces)
            (df['rsi'] <= rsi_lo_max)                # RSI band: not overbought (avoid exhaustion entries)
        )

        short_cond = (
            (df['close'] < df['lowest_low']) &
            (df['close'] < df['ema']) &
            df['vol_spike'] &                        # AND (was OR)
            (df['adx'] > adx_min) &                  # AND (was OR)
            (df['rsi'] >= rsi_sh_min) &              # RSI band: not already oversold
            (df['rsi'] <= rsi_sh_max)                # RSI band: bearish momentum zone
        )

        df.loc[long_cond, 'signal'] = 1
        df.loc[short_cond, 'signal'] = -1

        # Crossover only
        df.loc[(df['signal'] == 1) & (df['signal'].shift(1) == 1), 'signal'] = 0
        df.loc[(df['signal'] == -1) & (df['signal'].shift(1) == -1), 'signal'] = 0

        return df

    def validate_params(self) -> bool:
        return True
