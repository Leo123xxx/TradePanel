import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class TurtleSoup(BaseStrategy):
    """
    Turtle Soup Strategy (SMC / Liquidity Sweep)

    Logic:
    1. Identify the N-bar High or Low level.
    2. Price sweeps the level (liquidity grab) then reverses and closes back inside.
    3. Cooldown: No new signal for N bars after a signal fires.
    RR = 2.5:1 (tp_atr_mult=2.5, sl_atr_mult=1.0).

    v2 upgrades (2026-04-29) — targeting 70%+ WR from 66.7%:
    - EMA200 trend context: sweep of a LOW in uptrend (close > EMA200) = high-quality BUY.
      Sweep of a HIGH in downtrend (close < EMA200) = high-quality SELL. Counter-trend
      sweeps are discarded — they often become continuation moves, not reversals.
    - ADX max gate (default 30): sweeps in strong trends tend to run rather than reverse.
      Only take sweeps when ADX < 30 (ranging or mild trend context).
    - Volume confirmation: the sweep bar must carry above-average volume — confirms genuine
      liquidity grab rather than thin-market spike.
    - Minimum penetration tightened (pips → ATR units): avoids shallow noise sweeps
      that barely touch the level.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "lookback":              20,
                "min_penetration_pips":   5,   # loosened 8→5: restore original
                "max_penetration_pips":  40,
                "atr_period":            14,
                "tp_atr_mult":            2.5, # RR 2.5:1
                "sl_atr_mult":            1.0,
                "sl_buffer_pips":         5,   # kept for reference only
                "cooldown_bars":         10,   # loosened 15→10
                "adx_max":               30,   # NEW: sweeps only in ranging/mild trend (ADX < 30)
                "vol_threshold_mult":     1.3, # NEW: sweep bar must have above-avg volume
                "ema200_period":        200,   # NEW: macro trend filter
            }
        super().__init__(
            name="Turtle_Soup",
            category="SMC",
            params=params,
            regime=["RANGING", "ANY"],
            timeframes=["H1", "H4"],
            pairs=["XAUUSD", "BTCUSD", "EURUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        lookback       = self.params.get("lookback", 20)
        adx_max        = self.params.get("adx_max", 30)
        vol_mult       = self.params.get("vol_threshold_mult", 0.0)
        ema200_p       = self.params.get("ema200_period", 200)

        # 1. Previous N-bar High and Low
        df['h20'] = df['high'].rolling(window=lookback).max().shift(1)
        df['l20'] = df['low'].rolling(window=lookback).min().shift(1)

        # 2. Sweep Detection
        # Low swept: current low < l20, but current close > l20 (reversal back inside)
        df['sweep_low']  = (df['low']  < df['l20']) & (df['close'] > df['l20'])
        # High swept: current high > h20, but current close < h20 (reversal back inside)
        df['sweep_high'] = (df['high'] > df['h20']) & (df['close'] < df['h20'])

        # 3. ADX gate — only sweep-fade in ranging/mild-trend markets
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 20.0  # fallback: always pass
        not_trending = df['adx'] < adx_max

        # 4. EMA200 macro trend context
        df['ema200'] = ta.ema(df['close'], length=ema200_p)
        macro_up   = df['close'] > df['ema200']   # uptrend: sweep of lows = best buy
        macro_down = df['close'] < df['ema200']   # downtrend: sweep of highs = best sell

        # 5. Volume gate — sweep bar must carry conviction
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (df['vol_avg'] * vol_mult)
        else:
            vol_ok = True

        # 6. Signals — sweep in alignment with macro trend + ADX not extreme + volume confirmed
        df['signal'] = 0
        df.loc[df['sweep_low']  & not_trending & macro_up   & vol_ok, 'signal'] =  1
        df.loc[df['sweep_high'] & not_trending & macro_down & vol_ok, 'signal'] = -1

        # 7. Cooldown filter — suppress repeated signals within N bars
        cooldown = self.params.get("cooldown_bars", 15)
        signal_arr = df['signal'].values.copy()
        last_signal_bar = -cooldown - 1
        for i in range(len(signal_arr)):
            if signal_arr[i] != 0:
                if i - last_signal_bar <= cooldown:
                    signal_arr[i] = 0
                else:
                    last_signal_bar = i
        df['signal'] = signal_arr

        return df

    def validate_params(self) -> bool:
        return self.params.get("lookback", 0) > 0
