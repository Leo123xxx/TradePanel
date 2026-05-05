import pandas as pd
import MetaTrader5 as mt5
from typing import Optional
from datetime import datetime, timedelta
from strategies.base_strategy import BaseStrategy

class SignalChecker:
    """
    Bridge between live MT5 data and Strategy logic.
    Identifies signals based on recently closed bars.
    
    PHASE 0 FIX #3: Data Freshness Check
    - Validates data is < 24 hours old
    - Detects gaps in bar data (missing bars), skipping legitimate weekend gaps
    - Blocks signals on stale/gapped data

    FIX (2026-04-30):
    - _check_data_age: use UTC (not local SAST) to compare against MT5 UTC timestamps
    - _detect_data_gaps: only check last 20 bars; skip gaps that span a weekend
    - get_signal: accept lookback_bars param and scan multiple completed bars so
      signal_validity_bars config actually has an effect on live detection
    """
    
    def __init__(self):
        self.max_data_age_hours = 24
        self.gap_threshold_minutes = 60
        
    def _log_stale_data_event(self, symbol: str, timeframe: int, reason: str, details: str):
        """Log stale data or gap detection events (for audit trail)."""
        timestamp = datetime.now().isoformat()
        log_msg = (
            f"[DATA_FRESHNESS_ALERT] {timestamp} | "
            f"Symbol: {symbol} | TF: {timeframe} | "
            f"Reason: {reason} | Details: {details}"
        )
        print(log_msg)
        # TODO: Write to database table: data_freshness_log
        return log_msg

    def get_latest_data(self, symbol: str, timeframe: int, count: int = 100) -> Optional[pd.DataFrame]:
        """Fetches the last N bars from MT5 terminal."""
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None or len(rates) == 0:
            return None
        
        df = pd.DataFrame(rates)
        # The bridge returns ISO strings; native MT5 returns unix ints. Handle both.
        if df['time'].dtype == object:
            df['timestamp'] = pd.to_datetime(df['time'])
        else:
            df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('timestamp', inplace=True)
        
        # Ensure correct numeric types for technical analysis
        for col in ['open', 'high', 'low', 'close', 'tick_volume']:
            df[col] = df[col].astype(float)
            
        return df

    def _check_data_age(self, symbol: str, latest_bar_time: pd.Timestamp) -> tuple[bool, str]:
        """
        Check if latest bar is within 24 hours (PHASE 0 FIX #3).
        Returns: (is_fresh, message)

        FIX (2026-04-30): use utcnow() — MT5 copy_rates_from_pos returns UTC
        timestamps, so comparing against local SAST time made bars appear 2h
        older than they actually are.
        """
        current_time = pd.Timestamp.utcnow().tz_localize(None)
        time_diff = current_time - latest_bar_time
        age_hours = time_diff.total_seconds() / 3600
        
        if age_hours > self.max_data_age_hours:
            msg = f"Data is {age_hours:.1f} hours old (limit: {self.max_data_age_hours}h)"
            self._log_stale_data_event(symbol, None, "DATA_TOO_OLD", msg)
            return False, msg
        
        return True, f"Data age: {age_hours:.1f}h (OK)"

    def _is_weekend_gap(self, start_time: pd.Timestamp, end_time: pd.Timestamp) -> bool:
        """
        Return True if the gap between two bars spans a weekend market close.

        Forex/CFD markets close Friday ~21:00 UTC and reopen Sunday ~22:00 UTC,
        so any gap that contains a Saturday is a legitimate weekend closure and
        should NOT be treated as a connectivity problem.

        FIX (2026-04-30): added to prevent D1/H4 strategies from being permanently
        blocked by the Friday→Monday gap that appears in every historical fetch.
        """
        start_wd = start_time.weekday()  # 0=Mon … 4=Fri, 5=Sat, 6=Sun
        # If start is already Saturday, gap starts in the weekend
        if start_wd == 5:
            return True
        # Find the next Saturday after start_time
        days_to_sat = (5 - start_wd) % 7
        next_saturday = start_time + timedelta(days=days_to_sat)
        return next_saturday < end_time

    def _detect_data_gaps(self, symbol: str, timeframe: int, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Detect gaps in bar data by checking consecutive bar timestamps.
        PHASE 0 FIX #3: If gap > 1 hour (and not a weekend), block signals.
        Returns: (no_gaps, message)

        FIX (2026-04-30):
        - Only inspect the most recent 20 bars (historical bars always include
          weekend gaps and scanning all 100 caused false DATA_GAP alerts every
          Monday for D1/H4 strategies).
        - Skip gaps that span a weekend via _is_weekend_gap.
        """
        if df is None or len(df) < 2:
            return True, "Insufficient data for gap detection"
        
        # Timeframe to seconds mapping
        tf_seconds_map = {
            mt5.TIMEFRAME_M1: 60,
            mt5.TIMEFRAME_M5: 300,
            mt5.TIMEFRAME_M15: 900,
            mt5.TIMEFRAME_M30: 1800,
            mt5.TIMEFRAME_H1: 3600,
            mt5.TIMEFRAME_H4: 14400,
            mt5.TIMEFRAME_D1: 86400,
            mt5.TIMEFRAME_W1: 604800,
            mt5.TIMEFRAME_MN1: 2592000,
        }
        
        expected_interval = tf_seconds_map.get(timeframe, 3600)
        allowed_buffer_seconds = 60  # Allow 1 minute buffer for clock skew
        gap_tolerance = expected_interval + allowed_buffer_seconds

        # Only examine the most recent 20 bars to catch connectivity gaps —
        # historical bars routinely span weekends and are not meaningful here.
        recent_df = df.iloc[-20:] if len(df) >= 20 else df
        timestamps = recent_df.index.values
        gaps_detected = []
        
        for i in range(len(timestamps) - 1):
            current_bar = pd.Timestamp(timestamps[i])
            next_bar = pd.Timestamp(timestamps[i + 1])
            diff_seconds = (next_bar - current_bar).total_seconds()
            
            if diff_seconds > gap_tolerance:
                # Skip gaps that span a weekend — those are market closures, not errors
                if self._is_weekend_gap(current_bar, next_bar):
                    continue
                gap_minutes = diff_seconds / 60
                gaps_detected.append({
                    'position': i,
                    'expected': expected_interval,
                    'actual': diff_seconds,
                    'gap_minutes': gap_minutes
                })
        
        if gaps_detected:
            # If any non-weekend gap > gap_threshold_minutes, block signals
            for gap in gaps_detected:
                if gap['gap_minutes'] > self.gap_threshold_minutes:
                    msg = (
                        f"Data gap detected: {gap['gap_minutes']:.0f} minutes "
                        f"(limit: {self.gap_threshold_minutes} min)"
                    )
                    self._log_stale_data_event(symbol, timeframe, "DATA_GAP", msg)
                    return False, msg
            
            # Gaps exist but < 1 hour, warn but allow
            gap_summary = ", ".join([
                f"{g['gap_minutes']:.0f}m at bar {g['position']}" 
                for g in gaps_detected[:3]  # Show first 3 gaps
            ])
            return True, f"Minor gaps detected: {gap_summary}"
        
        return True, "No data gaps detected"

    def _is_data_stale(self, symbol: str, timeframe: int, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Comprehensive freshness check combining age + gap detection.
        PHASE 0 FIX #3: Block signals if data is stale or has gaps.
        Returns: (is_fresh, message)
        """
        if df is None or len(df) == 0:
            return False, "No data available"
        
        latest_bar_time = df.index[-1]
        
        # Check 1: Data age (< 24 hours)
        is_fresh, age_msg = self._check_data_age(symbol, latest_bar_time)
        if not is_fresh:
            return False, age_msg
        
        # Check 2: Data gaps (< 1 hour non-weekend gaps only)
        no_gaps, gaps_msg = self._detect_data_gaps(symbol, timeframe, df)
        if not no_gaps:
            return False, gaps_msg
        
        return True, f"Data fresh ({age_msg}, {gaps_msg})"

    def get_signal(
        self,
        strategy: BaseStrategy,
        symbol: str,
        timeframe: int,
        lookback_bars: int = 2,
    ) -> tuple[int, Optional[pd.Timestamp], bool]:
        """
        Executes strategy logic on the latest data.
        
        PHASE 0 FIX #3: Validates data freshness before signal generation.

        FIX (2026-04-30):
        - Added lookback_bars parameter (default 2, driven by signal_validity_bars
          in config). Scans the last `lookback_bars` completed bars and returns
          the most recent non-zero signal. Previously only iloc[-2] was checked,
          making signal_validity_bars effectively dead config for live detection.
        - Removed noisy "Data OK for {symbol}" print that fired every minute for
          every symbol/strategy combo (was ~336 lines/min at full load).
        
        Returns:
            (signal, timestamp, is_stale)
            - signal: 1 (BUY), -1 (SELL), 0 (NO SIGNAL)
            - timestamp: bar timestamp of the detected signal
            - is_stale: True if data is stale/gapped, False if fresh
        """
        df = self.get_latest_data(symbol, timeframe)
        if df is None:
            print(f"Warning: Could not fetch data for {symbol}")
            return 0, None, True
        
        # PHASE 0 FIX #3: Check data freshness before proceeding
        is_fresh, freshness_msg = self._is_data_stale(symbol, timeframe, df)
        
        if not is_fresh:
            print(f"[SignalChecker] BLOCKED: {symbol} - {freshness_msg}")
            return 0, None, True  # Block signal if data is stale
        
        # Generate signals only if data is fresh
        df_signals = strategy.generate_signals(df)
        if len(df_signals) < 2:
            return 0, None, False
        
        # Scan the last `lookback_bars` completed bars (iloc[-2] is the most
        # recent closed bar; iloc[-1] is the still-forming current bar).
        # Return the first (most recent) non-zero signal found.
        for i in range(2, 2 + lookback_bars):
            if len(df_signals) < i + 1:
                break
            bar_signal = int(df_signals['signal'].iloc[-i])
            bar_time = df_signals.index[-i]
            if bar_signal != 0:
                direction = "BUY" if bar_signal == 1 else "SELL"
                bar_label = f"bar -{i - 1}" if i > 2 else "latest bar"
                print(f"SIGNAL DETECTED: {direction} for {symbol} on {bar_time} ({bar_label})")
                return bar_signal, bar_time, False

        return 0, None, False
