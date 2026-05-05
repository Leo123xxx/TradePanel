"""
scheduler/signal_outcome_checker.py — Validates signal outcomes using OHLCV data.
"""

import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from data.db_client import DBClient
from utils.pip_sizes import get_pip_size

class SignalOutcomeChecker:
    def __init__(self):
        self.db = DBClient()

    def run(self, last_n_hours=24):
        """Checks outcomes for signals generated in the last N hours."""
        print(f"[{datetime.now()}] Starting signal outcome check (last {last_n_hours}h)...")
        
        # Fetch signals that haven't been checked yet
        query = """
            SELECT s.signal_id, s.strategy_id, s.timestamp, s.pair, s.direction, 
                   s.validity_window, s.indicator_values, s.timeframe, st.name
            FROM signals s
            JOIN strategies st ON s.strategy_id = st.strategy_id
            LEFT JOIN signal_outcomes so ON s.signal_id = so.signal_id
            WHERE s.timestamp >= NOW() - INTERVAL %s
              AND so.signal_id IS NULL
              AND s.timeframe IS NOT NULL
            ORDER BY s.timestamp ASC
        """
        signals = self.db.execute_query(query, (f"{last_n_hours} hours",))
        
        if not signals:
            print("No new signals to check.")
            return
            
        print(f"Found {len(signals)} signals to validate.")
        
        for sig in signals:
            self._check_single_signal(sig)

    def _check_single_signal(self, sig):
        sig_id, strat_id, ts, pair, direction, validity_str, iv, tf, strat_name = sig
        
        # 1. Parse validity window to number of bars
        # Validity string format: "2 hours", "30 min"
        try:
            if "hour" in validity_str:
                val_hours = int(validity_str.split()[0])
                # We need to know how many bars this represents for the signal's TF
                tf_to_hours = {"M1": 1/60, "M5": 5/60, "M15": 0.25, "H1": 1, "H4": 4, "D1": 24}
                bars_to_check = int(val_hours / tf_to_hours.get(tf, 1))
            else:
                val_min = int(validity_str.split()[0])
                tf_to_min = {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440}
                bars_to_check = int(val_min / tf_to_min.get(tf, 60))
        except Exception:
            bars_to_check = 10 # Fallback
            
        # Ensure we check at least a few bars
        bars_to_check = max(bars_to_check, 5)
        
        # 2. Get entry price and targets
        iv_dict = iv if isinstance(iv, dict) else json.loads(iv)
        entry_price = iv_dict.get("price")
        if not entry_price:
            return

        pip_size = get_pip_size(pair)
        
        # Re-calculate targets using same logic as router.py
        atr_val = iv_dict.get("atr")
        if atr_val and isinstance(atr_val, (int, float)) and atr_val > 0:
            sl_dist = atr_val * pip_size
        else:
            if "XAUUSD" in pair: default_sl_pips = 300
            elif "JPY" in pair: default_sl_pips = 50
            else: default_sl_pips = 30
            sl_dist = default_sl_pips * pip_size
            
        if direction == "BUY":
            sl = entry_price - sl_dist
            tp1 = entry_price + sl_dist
            tp2 = entry_price + (sl_dist * 2)
            tp3 = entry_price + (sl_dist * 3)
        else:
            sl = entry_price + sl_dist
            tp1 = entry_price - sl_dist
            tp2 = entry_price - (sl_dist * 2)
            tp3 = entry_price - (sl_dist * 3)

        # 3. Fetch future market data
        # Fetch bars starting from signal timestamp
        data_query = """
            SELECT high, low, close, timestamp
            FROM market_data
            WHERE pair = %s AND timeframe = %s AND timestamp > %s
            ORDER BY timestamp ASC
            LIMIT %s
        """
        future_bars = self.db.execute_query(data_query, (pair, tf, ts, bars_to_check))
        
        if not future_bars:
            # Maybe data sync hasn't run yet
            return
            
        outcome = "EXPIRED"
        bars_to_close = len(future_bars)
        pnl_pips = 0.0
        
        # 4. Check bars sequentially
        for i, (high, low, close, bar_ts) in enumerate(future_bars):
            high = float(high)
            low = float(low)
            
            if direction == "BUY":
                # Check SL first (conservative)
                if low <= sl:
                    outcome = "SL"
                    bars_to_close = i + 1
                    pnl_pips = (sl - entry_price) / pip_size
                    break
                elif high >= tp3:
                    outcome = "TP3"
                    bars_to_close = i + 1
                    pnl_pips = (tp3 - entry_price) / pip_size
                    break
                elif high >= tp2:
                    outcome = "TP2"
                    # Keep looking for TP3 unless we hit SL
                    outcome = "TP2"
                    pnl_pips = (tp2 - entry_price) / pip_size
                elif high >= tp1:
                    if outcome not in ["TP2", "TP3"]:
                        outcome = "TP1"
                        pnl_pips = (tp1 - entry_price) / pip_size
            else: # SELL
                if high >= sl:
                    outcome = "SL"
                    bars_to_close = i + 1
                    pnl_pips = (entry_price - sl) / pip_size
                    break
                elif low <= tp3:
                    outcome = "TP3"
                    bars_to_close = i + 1
                    pnl_pips = (entry_price - tp3) / pip_size
                    break
                elif low <= tp2:
                    outcome = "TP2"
                    pnl_pips = (entry_price - tp2) / pip_size
                elif low <= tp1:
                    if outcome not in ["TP2", "TP3"]:
                        outcome = "TP1"
                        pnl_pips = (entry_price - tp1) / pip_size

        # If expired, calculate P&L at the last bar's close
        if outcome == "EXPIRED":
            last_close = float(future_bars[-1][2])
            pnl_pips = (last_close - entry_price) / pip_size if direction == "BUY" else (entry_price - last_close) / pip_size

        # 5. Write results
        insert_query = """
            INSERT INTO signal_outcomes (signal_id, outcome, bars_to_close, pnl_pips, checked_at)
            VALUES (%s, %s, %s, %s, NOW())
        """
        self.db.execute_query(insert_query, (sig_id, outcome, bars_to_close, pnl_pips))
        print(f"  Signal {sig_id} ({strat_name} {pair} {tf}): {outcome} in {bars_to_close} bars (PnL: {pnl_pips:.1f} pips)")

if __name__ == "__main__":
    checker = SignalOutcomeChecker()
    checker.run()
