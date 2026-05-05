import pandas as pd
import numpy as np
import ta_compat as ta
from strategies.base_strategy import BaseStrategy


class ORBStrategy(BaseStrategy):
    """
    Opening Range Breakout (ORB) v3.

    v3 upgrades (2026-05-01) — targeting 70%+ WR on EURUSD:
    - Daily direction bias filter: only long if today's daily open > EMA20 of daily opens
      (approximated from H1 data as EMA20 of last 20 days' first bar close).
      Only buy ORB when the broader daily bias is bullish; only sell when bearish.
      Eliminates breakouts that run against the day's overall momentum.
    """

    def __init__(self, params=None):
        if params is None:
            params = {
                'ny_offset_hours':          7,
                'range_start_ny':           9.5,
                'range_duration_mins':      60,
                'vol_filter':               1.2,
                'tp_atr_mult':              2.0,
                'sl_atr_mult':              1.0,
                'adx_min':                 20,
                'post_range_window_hours':   5,
                'daily_ema_period':         20,    # NEW: daily bias EMA period
                'use_session_filter':       False,
            }
        super().__init__(
            name='Opening_Range_Breakout',
            category='Breakout',
            params=params,
            regime=['TRENDING', 'ANY'],
            timeframes=['M15'],
            pairs=['GBPUSD', 'EURUSD', 'XAUUSD'],
        )

    def generate_signals(self, data):
        df = data.copy()
        offset       = self.params.get('ny_offset_hours',          7)
        adx_min      = self.params.get('adx_min',                 20)
        post_window  = self.params.get('post_range_window_hours',  5)
        daily_ema_p  = self.params.get('daily_ema_period',        20)

        # 1. Map each bar to its NY-equivalent hour
        df['hour_ny'] = (df.index.hour - offset) + (df.index.minute / 60.0)
        df['date'] = df.index.date

        # 2. Identify Opening Range bars
        start = self.params['range_start_ny']
        end   = start + (self.params['range_duration_mins'] / 60.0)
        df['is_range'] = (df['hour_ny'] >= start) & (df['hour_ny'] < end)

        range_high = df[df['is_range']].groupby('date')['high'].max()
        range_low  = df[df['is_range']].groupby('date')['low'].min()
        df['rh'] = df['date'].map(range_high)
        df['rl'] = df['date'].map(range_low)

        # 3. Post-range window
        df['is_post_range'] = (df['hour_ny'] >= end) & (df['hour_ny'] < (end + post_window))

        # 4. ADX breakout confirmation
        try:
            adx_df    = ta.adx(df['high'], df['low'], df['close'], length=14)
            df['adx'] = adx_df.iloc[:, 0]
        except Exception:
            df['adx'] = 25.0
        adx_ok = df['adx'] > adx_min

        # 5. Daily direction bias filter
        # Compute each day's "open" price as the first bar's close on that day
        # Then EMA20 of those daily opens acts as a daily trend gauge
        daily_first_close = df.groupby('date')['close'].first()
        daily_first_close_series = pd.Series(daily_first_close.values, index=daily_first_close.index)
        # Compute EMA on daily series
        daily_ema_vals = daily_first_close_series.ewm(span=daily_ema_p, adjust=False).mean()
        daily_ema_map = daily_ema_vals.to_dict()
        daily_open_map = daily_first_close.to_dict()
        df['_daily_open'] = df['date'].map(daily_open_map)
        df['_daily_ema']  = df['date'].map(daily_ema_map)
        daily_bias_up   = df['_daily_open'] > df['_daily_ema']
        daily_bias_down = df['_daily_open'] < df['_daily_ema']
        df.drop(columns=['_daily_open', '_daily_ema'], inplace=True)

        # 6. Volume filter (range-bar normalised by hourly mean — avoids EURUSD 0-signal bug)
        tv = df['tick_volume']
        nonzero_pct = (tv > 0).mean()
        volume_data_usable = nonzero_pct >= 0.5

        if volume_data_usable:
            df['_hr'] = df.index.hour
            hmean = df.groupby('_hr')['tick_volume'].transform('mean')
            df['_vol_rel'] = tv / hmean.clip(lower=1)
            range_rel_vol = (
                df[df['is_range']]
                .groupby('date')['_vol_rel']
                .mean()
            )
            df['_day_range_vol_ok'] = df['date'].map(
                range_rel_vol >= self.params['vol_filter']
            )
            df['vol_ok'] = df['_day_range_vol_ok'].astype(bool).fillna(False)
            df.drop(columns=['_hr', '_vol_rel', '_day_range_vol_ok'], inplace=True)
        else:
            df['vol_ok'] = True

        # Diagnostics
        n_range       = int(df['is_range'].sum())
        n_post        = int(df['is_post_range'].sum())
        n_vol_ok_post = int((df['is_post_range'] & df['vol_ok']).sum())
        n_crossover   = int((df['is_post_range'] & df['rh'].notna() & (df['close'] > df['rh']) & (df['close'].shift(1) <= df['rh'])).sum())
        vol_tag = 'range-vol-filter' if volume_data_usable else 'bypassed'
        print(
            '[ORB] range_bars={}  post={}  vol_ok_post={}  crossover={}  vol={}'.format(
                n_range, n_post, n_vol_ok_post, n_crossover, vol_tag
            )
        )

        # 7. Signals
        df['signal'] = 0
        buy_cond = (
            df['is_post_range']
            & (df['close'] > df['rh'])
            & (df['close'].shift(1) <= df['rh'])
            & df['vol_ok']
            & adx_ok
            & daily_bias_up    # NEW: daily bias must be bullish
        )
        sell_cond = (
            df['is_post_range']
            & (df['close'] < df['rl'])
            & (df['close'].shift(1) >= df['rl'])
            & df['vol_ok']
            & adx_ok
            & daily_bias_down  # NEW: daily bias must be bearish
        )
        df.loc[buy_cond,  'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1

        return df

    def validate_params(self):
        return True
