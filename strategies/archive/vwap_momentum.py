import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy

class VWAPMomentum(BaseStrategy):
    """
    VWAP Momentum Shift (Mean Reversion) v3.

    v3 upgrades (2026-05-01) — targeting 70%+ WR:
    - ADX max tightened 30->22: only trade in clearly ranging markets
    - RSI zones tightened: rsi_buy_max 45->35 (deep oversold), rsi_sell_min 55->65 (deep overbought)
    - VWAP deviation filter: price must be >= 0.8x ATR beyond VWAP band (not just touching it)
    - Volume direction filter: volume must be DECREASING over last 3 bars (exhaustion signal)
      before the reversal bar. A spike into the band on rising volume is momentum, not exhaustion.
    """

    def __init__(self, params: dict = None):
        if params is None:
            params = {
                "std_dev_mult":           2.0,
                "atr_period":            14,
                "tp_atr_mult":            2.0,
                "sl_atr_mult":            1.0,
                "min_std_periods":        5,
                "use_partial_tp":        False,
                "adx_max":               22,    # tightened 30->22
                "rsi_period":            14,
                "rsi_buy_max":           35,    # tightened 45->35 (deep oversold only)
                "rsi_sell_min":          65,    # tightened 55->65 (deep overbought only)
                "vol_threshold_mult":     1.2,  # reversal bar volume gate
                "vwap_atr_min_excess":    0.8,  # NEW: min excess beyond band in ATR units
                "vol_exhaustion_bars":    3,    # NEW: volume must be declining this many bars
                "session_start_utc":      7,
                "session_end_utc":       17,
            }
        super().__init__(
            name="VWAP_Momentum",
            category="Mean Reversion",
            params=params,
            regime=["RANGING", "HIGH_VOL"],
            timeframes=["M15", "M30", "H1"],
            pairs=["GBPUSD", "EURUSD", "XAUUSD"]
        )

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        std_mult        = self.params.get("std_dev_mult",          2.0)
        adx_max         = self.params.get("adx_max",               22)
        rsi_p           = self.params.get("rsi_period",            14)
        rsi_buy_max     = self.params.get("rsi_buy_max",           35)
        rsi_sell_min    = self.params.get("rsi_sell_min",          65)
        vol_mult        = self.params.get("vol_threshold_mult",     1.2)
        vwap_excess_atr = self.params.get("vwap_atr_min_excess",    0.8)
        vol_exhaust_n   = self.params.get("vol_exhaustion_bars",    3)
        session_start   = self.params.get("session_start_utc",     7)
        session_end     = self.params.get("session_end_utc",       17)

        # 1. Daily VWAP
        df['date'] = df.index.date
        df['pv']   = df['close'] * df['tick_volume']
        df['cum_pv'] = df.groupby('date')['pv'].cumsum()
        df['cum_v']  = df.groupby('date')['tick_volume'].cumsum()
        df['vwap']   = df['cum_pv'] / df['cum_v']

        # 2. VWAP std deviation
        df['vwap_std'] = df.groupby('date')['close'].transform(lambda x: x.expanding().std())
        valid_std = df['vwap_std'].notna() & (df['vwap_std'] > 0)

        # 3. ATR
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)

        # 4. VWAP bands
        df['vwap_upper'] = df['vwap'] + std_mult * df['vwap_std']
        df['vwap_lower'] = df['vwap'] - std_mult * df['vwap_std']

        # 5. Overextended with minimum excess beyond band (in ATR units)
        df['excess_up']   = df['close'] - df['vwap_upper']   # positive = above upper band
        df['excess_down'] = df['vwap_lower'] - df['close']   # positive = below lower band
        df['is_overbought'] = df['excess_up']   >= vwap_excess_atr * df['atr']
        df['is_oversold']   = df['excess_down'] >= vwap_excess_atr * df['atr']

        # 6. ADX gate
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df["ADX_14"]
        except Exception:
            df['adx'] = 15.0
        not_trending = df['adx'] < adx_max

        # 7. RSI gate (deeper extreme zones)
        df['rsi']    = ta.rsi(df['close'], length=rsi_p)
        rsi_buy_ok   = df['rsi'] <= rsi_buy_max
        rsi_sell_ok  = df['rsi'] >= rsi_sell_min

        # 8. Volume exhaustion: volume must be declining over last N bars before reversal
        #    vol_exhaust_n=3: vol[i-1] < vol[i-2] < vol[i-3] => declining momentum into band
        if vol_exhaust_n >= 2 and 'tick_volume' in df.columns:
            # Check that each successive bar has lower volume than the one before
            vol_declining = df['tick_volume'].shift(1) < df['tick_volume'].shift(2)
            for k in range(2, vol_exhaust_n):
                vol_declining = vol_declining & (df['tick_volume'].shift(k) < df['tick_volume'].shift(k + 1))
        else:
            vol_declining = True

        # 9. Reversal bar volume confirmation
        if vol_mult > 0 and 'tick_volume' in df.columns:
            df['vol_avg'] = df['tick_volume'].rolling(window=20).mean()
            vol_ok = df['tick_volume'] >= (df['vol_avg'] * vol_mult)
        else:
            vol_ok = True

        # 10. Session gate
        try:
            hour = df.index.hour
            in_session = (hour >= session_start) & (hour < session_end)
        except Exception:
            in_session = True

        # 11. Signals
        df['signal'] = 0

        buy_gate  = valid_std & not_trending & rsi_buy_ok  & vol_ok & vol_declining & in_session
        sell_gate = valid_std & not_trending & rsi_sell_ok & vol_ok & vol_declining & in_session

        df.loc[buy_gate  & df['is_oversold'].shift(1)   & (df['close'] > df['high'].shift(1)), 'signal'] =  1
        df.loc[sell_gate & df['is_overbought'].shift(1) & (df['close'] < df['low'].shift(1)),  'signal'] = -1

        return df

    def validate_params(self) -> bool:
        return True
