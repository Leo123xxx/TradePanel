import os
import time
import logging
import MetaTrader5 as mt5
from dotenv import load_dotenv
from typing import List, Dict

class MT5Connector:
    def __init__(self):
        load_dotenv()
        self.login = int(os.getenv("MT5_LOGIN"))
        self.password = os.getenv("MT5_PASSWORD")
        self.server = os.getenv("MT5_SERVER")
        self.connected = False
        self.required_symbols = ["XAUUSD", "EURUSD", "GBPUSD", "USDJPY", "XAGUSD", "BTCUSD", "ETHUSD"]
        self.timeframes = ["M5", "H1", "H4", "D1"]

    def connect(self, required_symbols=None, force=False):
        """
        Attempts to connect to MT5 terminal.
        If force=True, it will shutdown any existing connection first.
        """
        if force and self.connected:
            print("INFO: Forcing MT5 reconnection...")
            mt5.shutdown()
            self.connected = False

        if self.connected:
            # Already connected, just ensure symbols are selected
            self._select_required_symbols(required_symbols)
            return True

        print(f"Attempting to connect to MT5 Server: {self.server} (Login: {self.login})...")
        
        if not mt5.initialize():
            print(f"MT5 initialize() failed, error code: {mt5.last_error()}")
            return False

        authorized = mt5.login(self.login, password=self.password, server=self.server)
        
        if authorized:
            print(f"SUCCESS: Connected and authorized on {self.server}.")
            self.connected = True
            self._select_required_symbols(required_symbols)
            
            acc_info = mt5.account_info()
            if acc_info:
                print(f"Account: {acc_info.login} | Balance: {acc_info.balance} {acc_info.currency}")
        else:
            print(f"FAILED: Authorization failed, error code: {mt5.last_error()}")
            mt5.shutdown()
            self.connected = False

        return self.connected

    def connect_with_retry(self, max_attempts: int = 3,
                           delays: list = None,
                           notify_fn=None) -> bool:
        """
        Attempts MT5 connection with exponential backoff.

        Args:
            max_attempts: Number of connection attempts before giving up (default 3).
            delays:       Seconds to wait between attempts (default [5, 15, 30]).
            notify_fn:    Optional callable(str) — called with error message on final failure
                          (pass TelegramBot.send_sync_message to alert via Telegram).

        Returns:
            True if connected, False if all attempts failed.
        """
        if delays is None:
            delays = [5, 15, 30]

        for attempt in range(1, max_attempts + 1):
            print(f"[MT5] Connection attempt {attempt}/{max_attempts}...")
            try:
                if self.connect(force=(attempt > 1)):
                    if attempt > 1:
                        msg = f"✅ MT5 reconnected after {attempt} attempts."
                        print(f"[MT5] {msg}")
                        if notify_fn:
                            try:
                                notify_fn(msg)
                            except Exception:
                                pass
                    return True
            except Exception as e:
                print(f"[MT5] Attempt {attempt} raised exception: {e}")

            if attempt < max_attempts:
                wait = delays[min(attempt - 1, len(delays) - 1)]
                print(f"[MT5] Waiting {wait}s before retry...")
                time.sleep(wait)

        # All attempts failed
        error_code = mt5.last_error()
        msg = (
            f"🔴 <b>MT5 CONNECTION FAILED</b>\n"
            f"All {max_attempts} attempts exhausted.\n"
            f"Error: {error_code}\n"
            f"Action: Check MT5 terminal is running and logged in."
        )
        print(f"[MT5] CRITICAL: {msg}")
        if notify_fn:
            try:
                notify_fn(msg)
            except Exception:
                pass
        return False

    def _select_required_symbols(self, required_symbols):
        """
        Helper to ensure symbols are in Market Watch.
        PHASE 0 FIX #4: Enhanced verification.
        """
        if required_symbols is None:
            required_symbols = self.required_symbols
        
        print("\n[Market Watch Setup]")
        print("=" * 70)
        
        success_count = 0
        warning_count = 0
        critical_count = 0
        
        for symbol in required_symbols:
            # Try to select symbol
            if not mt5.symbol_select(symbol, True):
                print(f"  [FAIL] CRITICAL: Could not add {symbol} to market watch")
                critical_count += 1
                continue
            
            # Verify symbol info
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print(f"  [FAIL] CRITICAL: {symbol} selected but no data returned. Check trading permissions.")
                critical_count += 1
                continue
            
            # Check if visible
            if not symbol_info.visible:
                print(f"  [WARN] WARNING: {symbol} is not visible in market watch (may be hidden)")
                warning_count += 1
            
            # Verify data streams for all required timeframes
            data_streams_ok = True
            for tf_str in self.timeframes:
                tf = getattr(mt5, f"TIMEFRAME_{tf_str}", None)
                if tf is None:
                    continue
                
                rates = mt5.copy_rates_from_pos(symbol, tf, 0, 5)
                if rates is None or len(rates) < 3:
                    print(f"  [WARN] WARNING: {symbol} {tf_str} has insufficient data (< 3 bars)")
                    data_streams_ok = False
                    warning_count += 1
            
            if data_streams_ok:
                print(f"  [OK] {symbol:10} - OK (visible, data streams active)")
                success_count += 1
            else:
                print(f"  [WARN] {symbol:10} - Warnings (see above)")
        
        print("=" * 70)
        print(f"Summary: {success_count} OK, {warning_count} warnings, {critical_count} critical")
        print()
        
        return critical_count == 0

    def verify_symbol_availability(self, symbol: str) -> Dict:
        """
        PHASE 0 FIX #4: Detailed symbol verification.
        Returns: {symbol: str, available: bool, visible: bool, tradeable: bool, details: str}
        """
        info = mt5.symbol_info(symbol)
        if info is None:
            return {
                'symbol': symbol,
                'available': False,
                'visible': False,
                'tradeable': False,
                'details': 'Symbol not found in MT5'
            }
        
        tradeable = info.trade_mode != mt5.SYMBOL_TRADE_MODE_DISABLED
        
        return {
            'symbol': symbol,
            'available': True,
            'visible': info.visible,
            'tradeable': tradeable,
            'details': f"digits={info.digits}, volume_min={info.volume_min}, volume_max={info.volume_max}"
        }

    def validate_data_streams(self) -> Dict[str, Dict]:
        """
        PHASE 0 FIX #4: Validate all symbols × timeframes have active data streams.
        Returns: {symbol: {timeframe: bool}}
        """
        results = {}
        
        for symbol in self.required_symbols:
            results[symbol] = {}
            for tf_str in self.timeframes:
                tf = getattr(mt5, f"TIMEFRAME_{tf_str}", None)
                if tf is None:
                    results[symbol][tf_str] = False
                    continue
                
                rates = mt5.copy_rates_from_pos(symbol, tf, 0, 5)
                results[symbol][tf_str] = (rates is not None and len(rates) >= 3)
        
        return results

    def disconnect(self, shutdown=False):
        """
        Marks as disconnected. 
        Only calls mt5.shutdown() if shutdown=True is passed.
        """
        if self.connected:
            if shutdown:
                mt5.shutdown()
                print("INFO: Fully shut down MT5 connection.")
            self.connected = False
            print("INFO: Connector marked as disconnected.")

if __name__ == "__main__":
    connector = MT5Connector()
    if connector.connect():
        # Verify all symbols
        print("\nDetailed Symbol Verification:")
        for sym in connector.required_symbols:
            result = connector.verify_symbol_availability(sym)
            print(f"  {sym}: {result['details']}")
        
        # Validate data streams
        print("\nData Stream Validation:")
        streams = connector.validate_data_streams()
        for symbol, tfs in streams.items():
            status = "[OK]" if all(tfs.values()) else "[WARN]"
            print(f"  {status} {symbol}: {tfs}")
        
        connector.disconnect()
