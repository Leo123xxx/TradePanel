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
    - Detects gaps in bar data (missing bars)
    - Blocks signals on stale/gapped data
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
        """
        current_time = pd.Timestamp.now(tz=None)
        time_diff = current_time - latest_bar_time
        age_hours = time_diff.total_seconds() / 3600
        
        if age_hours > self.max_data_age_hours:
            msg = f"Data is {age_hours:.1f} hours old (limit: {self.max_data_age_hours}h)"
            self._log_stale_data_event(symbol, None, "DATA_TOO_OLD", msg)
            return False, msg
        
        return True, f"Data age: {age_hours:.1f}h (OK)"

    def _detect_data_gaps(self, symbol: str, timeframe: int, df: pd.DataFrame) -> tuple[bool, str]:
        """
        Detect gaps in bar data by checking consecutive bar timestamps.
        PHASE 0 FIX #3: If gap > 1 hour, block signals.
        Returns: (no_gaps, message)
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
        
        # Check consecutive bar timestamps
        timestamps = df.index.values
        gaps_detected = []
        
        for i in range(len(timestamps) - 1):
            current_bar = pd.Timestamp(timestamps[i])
            next_bar = pd.Timestamp(timestamps[i + 1])
            diff_seconds = (next_bar - current_bar).total_seconds()
            
            if diff_seconds > gap_tolerance:
                gap_minutes = diff_seconds / 60
                gaps_detected.append({
                    'position': i,
                    'expected': expected_interval,
                    'actual': diff_seconds,
                    'gap_minutes': gap_minutes
                })
        
        if gaps_detected:
            # If any gap > gap_threshold_minutes, block signals
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
        
        # Check 2: Data gaps (< 1 hour gaps only)
        no_gaps, gaps_msg = self._detect_data_gaps(symbol, timeframe, df)
        if not no_gaps:
            return False, gaps_msg
        
        return True, f"Data fresh ({age_msg}, {gaps_msg})"

    def get_signal(self, strategy: BaseStrategy, symbol: str, timeframe: int) -> tuple[int, Optional[pd.Timestamp], bool]:
        """
        Executes strategy logic on the latest data.
        
        PHASE 0 FIX #3: Validates data freshness before signal generation.
        
        Returns:
            (signal, timestamp, is_stale)
            - signal: 1 (BUY), -1 (SELL), 0 (NO SIGNAL)
            - timestamp: timestamp of signal
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
        
        print(f"[SignalChecker] Data OK for {symbol}: {freshness_msg}")
        
        # Generate signals only if data is fresh
        df_signals = strategy.generate_signals(df)
        if len(df_signals) < 2:
            return 0, None, False
        
        latest_signal = df_signals['signal'].iloc[-2]
        signal_time = df_signals.index[-2]
        
        if latest_signal != 0:
            direction = "BUY" if latest_signal == 1 else "SELL"
            print(f"SIGNAL DETECTED: {direction} for {symbol} on {signal_time}")
        
        return int(latest_signal), signal_time, False
