import time
import MetaTrader5 as mt5
import ta_compat as ta

import yaml
import os
import json
from mt5_bridge.connector import MT5Connector
from mt5_bridge.order_manager import OrderManager
from risk.manager import RiskManager
from forward_test.signal_checker import SignalChecker
from data.db_client import DBClient
from risk.regime_classifier import RegimeClassifier
from strategies.bb_mean_reversion import BBMeanReversionStrategy
from strategies.cot_sentiment import COTSentimentStrategy
from strategies.crypto_rsi_extremes import CryptoRSIExtremesStrategy
from strategies.dual_ema_fractal import DualEMAFractal
from strategies.dual_ema_momentum import DualEMAMomentum
from strategies.ema_ribbon_trend import EMARibbonTrendStrategy
from strategies.ensemble import EnsembleStrategy
from strategies.gold_momentum_breakout import GoldMomentumBreakoutStrategy
from strategies.hikkake_trap import HikkakeTrap
from strategies.ict_judas_swing import ICTJudasSwing
from strategies.institutional_silver_bullet import InstitutionalSilverBullet
from strategies.ma_crossover import MACrossoverStrategy
from strategies.macd_trend import MACDTrendStrategy
from strategies.naked_price_action import NakedPriceAction
from strategies.orb import ORBStrategy
from strategies.range_breakout import RangeBreakoutStrategy
from strategies.rsi_2 import RSITwoStrategy
from strategies.rsi_bounce import RSIBounceStrategy
from strategies.rsi_pullback import RSIPullbackStrategy
from strategies.rvgi_cci_confluence import RVGICCIConfluence
from strategies.session_momentum import SessionMomentumStrategy
from strategies.stat_arb_gold_silver import StatArbGoldSilver
from strategies.stoch_divergence import StochDivergenceStrategy
from strategies.swing_pullback import SwingPullbackStrategy
from strategies.triple_macd_scalping import TripleMACDScalping
from strategies.turtle_soup import TurtleSoup
from strategies.volatility_contraction import VolatilityContraction
from strategies.volatility_squeeze_breakout import VolatilitySqueezeBreakoutStrategy
from strategies.vwap_momentum import VWAPMomentum
# NEW: 1m/5m Scalping Strategies (April 24, 2026)
from strategies.fast_ma_scalper import FastMAScalper
from strategies.bb_squeeze_scalp import BBSqueezeScalp
from strategies.rsi_extremes_scalp import RSIExtremesScalp
from strategies.macd_zero_scalp import MACDZeroScalp
from strategies.volatility_breakout_scalp import VolatilityBreakoutScalp
from strategies.ema_ribbon_scalp import EMARibbonScalp

STRATEGY_REGISTRY = {
    "bb_mean_reversion": BBMeanReversionStrategy,
    "cot_sentiment": COTSentimentStrategy,
    "crypto_rsi_extremes": CryptoRSIExtremesStrategy,
    "dual_ema_fractal": DualEMAFractal,
    "dual_ema_momentum": DualEMAMomentum,
    "ema_ribbon_trend": EMARibbonTrendStrategy,
    "ensemble": EnsembleStrategy,
    "gold_momentum_breakout": GoldMomentumBreakoutStrategy,
    "hikkake_trap": HikkakeTrap,
    "ict_judas_swing": ICTJudasSwing,
    "institutional_silver_bullet": InstitutionalSilverBullet,
    "ma_crossover": MACrossoverStrategy,
    "macd_trend": MACDTrendStrategy,
    "naked_price_action": NakedPriceAction,
    "orb": ORBStrategy,
    "range_breakout": RangeBreakoutStrategy,
    "rsi_2": RSITwoStrategy,
    "rsi_bounce": RSIBounceStrategy,
    "rsi_pullback": RSIPullbackStrategy,
    "rvgi_cci_confluence": RVGICCIConfluence,
    "session_momentum": SessionMomentumStrategy,
    "stat_arb_gold_silver": StatArbGoldSilver,
    "stoch_divergence": StochDivergenceStrategy,
    "swing_pullback": SwingPullbackStrategy,
    "triple_macd_scalping": TripleMACDScalping,
    "turtle_soup": TurtleSoup,
    "volatility_contraction": VolatilityContraction,
    "volatility_squeeze_breakout": VolatilitySqueezeBreakoutStrategy,
    "vwap_momentum": VWAPMomentum,
    # NEW: 1m/5m Scalping Strategies
    "fast_ma_scalper": FastMAScalper,
    "bb_squeeze_scalp": BBSqueezeScalp,
    "rsi_extremes_scalp": RSIExtremesScalp,
    "macd_zero_scalp": MACDZeroScalp,
    "volatility_breakout_scalp": VolatilityBreakoutScalp,
    "ema_ribbon_scalp": EMARibbonScalp,
}
from datetime import datetime
from notifications.telegram_bot import TelegramBot
from notifications.router import CommandRouter

class PaperEngine:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.connector = MT5Connector()
        self.order_manager = OrderManager()
        self.risk_manager = RiskManager(config_path)
        self.signal_checker = SignalChecker()
        self.db = DBClient()
        self.notif_bot = TelegramBot()
        self.notif_router = CommandRouter()
        
        # Path B: Macro Regime Filter
        self.regime_classifier = RegimeClassifier()
        self.use_regime_filter = self.config.get('risk_management', {}).get('use_macro_regime_filter', False)
        self.use_confirm_tf = self.config.get('risk_management', {}).get('use_multi_tf_confirmation', False)
        self.signal_validity_bars = max(2, self.config.get('risk_management', {}).get('signal_validity_bars', 2))
        
        # State tracking
        self.attempted_signals = {}  # {(strat_name, symbol, tf): last_attempted_timestamp}
        self.failed_attempts = {}    # {(strat_name, symbol): (count, last_failure_time)}
        
        # Load active strategies
        self.strategies_cfg = []
        self.active_strategies = {}
        self.load_strategies()

    def load_strategies(self, strategies_path="config/strategies.yaml"):
        """Loads and initializes all enabled strategies from the config file."""
        if not os.path.exists(strategies_path):
            print(f"[PaperEngine] [ERROR] Strategies config not found at {strategies_path}")
            return

        with open(strategies_path, 'r') as f:
            full_strat_cfg = yaml.safe_load(f)

        self.strategies_cfg = []
        self.active_strategies = {}

        for strat_name, strat_data in full_strat_cfg.items():
            if not isinstance(strat_data, dict) or not strat_data.get('enabled', False):
                continue
            
            if strat_name not in STRATEGY_REGISTRY:
                print(f"[PaperEngine] Unknown strategy '{strat_name}' — skipping.")
                continue

            # Check if it should be monitor only (Staging)
            is_monitor = strat_data.get('mode') == 'monitor_only'
            tier = strat_data.get('tier', 'UNKNOWN')

            strategy_class = STRATEGY_REGISTRY[strat_name]
            custom_params = strat_data.get('parameters', None)
            
            self.active_strategies[strat_name] = strategy_class(custom_params)
            self.active_strategies[strat_name].tier = tier
            self.active_strategies[strat_name].monitor_only = is_monitor
            
            # Store config for loop access
            self.strategies_cfg.append({
                'name': strat_name,
                'enabled': True,
                'pairs': strat_data.get('pairs', []),
                'timeframes': strat_data.get('timeframes', ['H1']),
                'tier': tier,
                'mode': strat_data.get('mode', 'trade')
            })
            
            print(f"[PaperEngine] Loaded {tier} strategy: {strat_name} ({'MONITOR' if is_monitor else 'TRADE'} mode)")
        
        print(f"[PaperEngine] Successfully loaded {len(self.active_strategies)} strategies.")

    def run_detect(self):
        """High-frequency signal detection (1m interval)."""
        self._run_loop(mode='detect')

    def run_execute(self):
        """Moderate-frequency trade execution (5m interval)."""
        self._run_loop(mode='execute')

    def _run_loop(self, mode='full'):
        """Generic loop over symbols."""
        try:
            all_symbols = set()
            for strat_cfg in self.strategies_cfg:
                all_symbols.update(strat_cfg.get('pairs', []))
            
            if not self.connector.connect(required_symbols=list(all_symbols)):
                print("Failed to connect to MT5. Skipping iteration.")
                return

            for strat_name, strategy in self.active_strategies.items():
                strat_cfg = next((s for s in self.strategies_cfg if s['name'] == strat_name), None)
                if not strat_cfg:
                    continue
                    
                for symbol in strat_cfg.get('pairs', []):
                    for tf_str in strat_cfg.get('timeframes', []):
                        mt5_tf = getattr(mt5, f"TIMEFRAME_{tf_str}", mt5.TIMEFRAME_H1)
                        self._process_symbol(strat_name, strategy, symbol, mt5_tf, mode=mode)

        except Exception as e:
            print(f"[PaperEngine] [FAIL] Error in _run_loop ({mode}): {e}")
        finally:
            self.connector.disconnect()

    def _process_symbol(self, strat_name, strategy, symbol, mt5_tf, mode='full'):
        """Processes signals and positions for a symbol."""
        try:
            # 0. Backoff Check for failed attempts
            key = (strat_name, symbol)
            if key in self.failed_attempts:
                count, last_time = self.failed_attempts[key]
                wait_secs = min(2 ** count, 300)  # Exponential backoff: 1, 2, 4, 8, ... max 300s
                if time.time() - last_time < wait_secs:
                    # Log once per minute to avoid noise
                    if int(time.time()) % 60 == 0:
                        print(f"[BACKOFF] {strat_name} on {symbol}: Waiting {wait_secs:.0f}s before retry.")
                    return

            # 1. Manage existing positions
            positions = mt5.positions_get(symbol=symbol)
            
            # 2. Get current signal
            signal, signal_time, is_stale = self.signal_checker.get_signal(strategy, symbol, mt5_tf)

            if is_stale:
                print(f"[PaperEngine] [SYNC] Stale data detected for {symbol}. Triggering forced reconnect...")
                self.connector.connect(force=True)
                # Retry signal fetch after reconnect
                signal, signal_time, is_stale = self.signal_checker.get_signal(strategy, symbol, mt5_tf)
            
            # 3. Signal Deduplication (PHASE 0 FIX #1 INTEGRATION)
            signal_key = self._create_signal_key(strat_name, symbol, mt5_tf, signal)
            if signal != 0 and signal_time is not None:
                if self._check_signal_duplicate(signal_key, signal_time):
                    # print(f"[PaperEngine] Skipping duplicate signal for {symbol}")
                    return # Already processed this bar/signal
            
            # Log detected signal to DB
            if signal != 0:
                self._log_signal(strat_name, symbol, signal, mt5_tf)

            if mode == 'detect':
                return # In detection mode, we only log signals

            # --- PATH B: MULTI-TF CONFIRMATION ---
            confirm_tf = strategy.confirm_tf
            if self.use_confirm_tf and confirm_tf and signal != 0:
                trend = self._get_confirmation_trend(symbol, confirm_tf)
                if signal == 1 and trend == -1:
                    print(f"[CONFIRM] Skipping BUY on {symbol} — {confirm_tf} trend is BEARISH")
                    signal = 0
                elif signal == -1 and trend == 1:
                    print(f"[CONFIRM] Skipping SELL on {symbol} — {confirm_tf} trend is BULLISH")
                    signal = 0

            # 4. IF position exists, check for close signal (Reversal)
            if positions:
                for pos in positions:
                    # Check for reversal: If Buy and Signal is Sell, or Vice Versa
                    if (pos.type == mt5.POSITION_TYPE_BUY and signal == -1) or \
                       (pos.type == mt5.POSITION_TYPE_SELL and signal == 1):
                        print(f"REVERSAL DETECTED: Closing position {pos.ticket}")
                        res, msg = self.order_manager.close_position(pos.ticket, "SIGNAL_REVERSAL")
                        if res is not None and res.retcode == mt5.TRADE_RETCODE_DONE:
                             self._log_trade_close(pos.ticket, res)
                             # Mark as attempted only if successful or if we want to stop retrying
                             self._track_processed_signal(signal_key, signal_time)
                        else:
                             print(f"FAILED to close on reversal: {msg}")
                             self.failed_attempts[key] = (self.failed_attempts.get(key, (0, 0))[0] + 1, time.time())
                             
            # 5. IF NO position, check for entry signal
            if not positions and signal != 0:
                direction = "BUY" if signal == 1 else "SELL"
                
                # --- PATH B: REGIME FILTER ---
                if (self.use_regime_filter or strategy.use_regime_filter) and "XAU" in symbol:
                    bias = self.regime_classifier.get_pair_bias(symbol)
                    if bias == 1 and direction == "SELL":
                        print(f"[REGIME] Skipping SELL on {symbol} due to LONG_BIAS")
                        return
                    if bias == -1 and direction == "BUY":
                        print(f"[REGIME] Skipping BUY on {symbol} due to SHORT_BIAS")
                        return
                    if bias == 0:
                        print(f"[REGIME] Skipping {direction} on {symbol} due to NEUTRAL macro state")
                        return
                
                # 5. Kelly Criterion / Dynamic Lot Sizing (Phase 4)
                base_lots = self.config.get('risk_management', {}).get('default_lot_size', 0.1)
                lot_size = self.risk_manager.calculate_kelly_size(strat_name, symbol, base_lots=base_lots)
                
                # 6. RISK CHECK
                passed, reason = self.risk_manager.check_all(strat_name, symbol, lot_size, direction)
                if not passed:
                    print(f"RISK BLOCKED: {reason}")
                    return

                # --- SL/TP CALCULATION FIX ---
                # Retrieve ATR and multipliers
                df = self.signal_checker.get_latest_data(symbol, mt5_tf, count=50)
                sl_points = 0
                tp_points = 0
                
                if df is not None and not df.empty:
                    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
                    latest_atr = df['atr'].iloc[-1]
                    
                    sl_mult = strategy.params.get('sl_atr_mult', 1.0)
                    tp_mult = strategy.params.get('tp_atr_mult', 1.5)
                    
                    # Convert ATR value to points (MT5 point size)
                    symbol_info = mt5.symbol_info(symbol)
                    pips_multiplier = 10 if symbol_info.digits in [3, 5] else 1
                    
                    sl_points = (latest_atr * sl_mult) / symbol_info.point
                    tp_points = (latest_atr * tp_mult) / symbol_info.point
                    
                    print(f"[PaperEngine] Calculated Targets ({strat_name}): SL={sl_points:.1f} pts, TP={tp_points:.1f} pts (ATR: {latest_atr:.5f})")

                # Generate a pseudo-magic number from strategy name (hashes to 6 digits)
                import zlib
                magic_number = zlib.adler32(strat_name.encode()) % 1000000

                print(f"EXECUTING: {direction} {lot_size} lots on {symbol} (Magic: {magic_number})")
                res, msg = self.order_manager.open_position(
                    symbol, direction, lot_size, 
                    sl_points=sl_points, tp_points=tp_points, 
                    comment=f"PAPER_{strat_name}",
                    magic=magic_number
                )
                
                # Mark as attempted (we don't want to spam if it fails validation or MT5 error)
                self._track_processed_signal(signal_key, signal_time)

                if res is not None and res.retcode == mt5.TRADE_RETCODE_DONE:
                    self._log_trade_open(strat_name, symbol, direction, lot_size, res)
                    # Reset failures on success
                    if key in self.failed_attempts:
                        del self.failed_attempts[key]
                else:
                    print(f"FAILED to open trade: {msg}")
                    self.failed_attempts[key] = (self.failed_attempts.get(key, (0, 0))[0] + 1, time.time())
        except Exception as e:
            print(f"[PaperEngine] [FAIL] Error in _process_symbol ({strat_name}/{symbol}): {e}")
            import traceback
            traceback.print_exc()

    def _log_trade_open(self, strat_name, symbol, direction, lot, result):
        import uuid
        trade_id = str(uuid.uuid4())

        # Strategy ID fetch — names stored lowercase in DB, match exactly
        strat_info = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strat_name,))
        if not strat_info:
            # Auto-insert if not yet present (first run for this strategy)
            strat_info = self.db.execute_query(
                "INSERT INTO strategies (name, category) VALUES (%s, %s) RETURNING strategy_id",
                (strat_name, "paper")
            )
        strategy_id = strat_info[0][0] if strat_info else None
        
        query = """
            INSERT INTO trades (trade_id, strategy_id, mode, pair, direction, lot_size, entry_price, open_time, status, mt5_ticket)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (
            trade_id, strategy_id, 'PAPER', symbol, direction, lot, 
            result.price, datetime.now(), 'OPENED', result.order
        ))
        
        # 6. Notify
        notif_data = {
            "symbol": symbol,
            "direction": direction,
            "lot_size": lot,
            "entry_price": result.price,
            "tp": round(tp_points * mt5.symbol_info(symbol).point, mt5.symbol_info(symbol).digits) if 'tp_points' in locals() else 0,
            "sl": round(sl_points * mt5.symbol_info(symbol).point, mt5.symbol_info(symbol).digits) if 'sl_points' in locals() else 0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        msg = self.notif_router.format_trade_open(notif_data)
        self.notif_bot.send_sync_message(msg)
        
    def _log_trade_close(self, ticket, result):
        # 1. Fetch the trade record from DB before updating it to get symbol/direction
        trade_info = self.db.execute_query(
            "SELECT pair, direction, entry_price, open_time FROM trades WHERE mt5_ticket = %s",
            (ticket,)
        )
        
        symbol = "N/A"
        direction = "N/A"
        pnl = 0.0
        duration = "N/A"
        
        if trade_info:
            symbol, direction, entry_price, open_time = trade_info[0]
            # Simple P&L calculation (points * lot_size * pip_value)
            # In a real scenario, we'd fetch actual P&L from MT5 history
            # But for paper trading, this is a good approximation if result.deal is not available
            exit_price = result.price
            pnl_points = (exit_price - entry_price) if direction == "BUY" else (entry_price - exit_price)
            # Fetch lot_size and pip_value from config for better accuracy
            pnl = pnl_points * 10.0 # Approximation or fetch from MT5 deal if possible
            
            delta = datetime.now() - open_time
            duration = str(delta).split('.')[0] # HH:MM:SS

        # 2. Update existing trade record
        query = """
            UPDATE trades 
            SET exit_price = %s, close_time = %s, status = %s, close_reason = %s
            WHERE mt5_ticket = %s
        """
        self.db.execute_query(query, (
            result.price, datetime.now(), 'CLOSED', 'SIGNAL_REVERSAL', ticket
        ))

        # 3. Notify
        close_data = {
            "symbol": symbol,
            "direction": direction,
            "pnl": round(pnl, 2),
            "exit_price": result.price,
            "reason": "SIGNAL_REVERSAL",
            "duration": duration,
            "currency": self.config.get('currency', 'USD'),
        }
        msg = self.notif_router.format_trade_close(close_data)
        self.notif_bot.send_sync_message(msg)

    def _log_signal(self, strat_name, symbol, direction_val, mt5_tf):
        """Logs the detected signal to the database."""
        try:
            # 1. Resolve strategy_id
            strat_info = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strat_name,))
            if not strat_info:
                strat_info = self.db.execute_query(
                    "INSERT INTO strategies (name, category) VALUES (%s, %s) RETURNING strategy_id",
                    (strat_name, "paper")
                )
            strategy_id = strat_info[0][0] if strat_info else None
            
            # 2. Calculate validity window
            # Default to 2 bars if not specified, min 2 bars
            # Map minutes to human readable duration
            tf_minutes = {
                mt5.TIMEFRAME_M15: 15,
                mt5.TIMEFRAME_H1: 60,
                mt5.TIMEFRAME_H4: 240,
                mt5.TIMEFRAME_D1: 1440
            }.get(mt5_tf, 60)
            
            validity_min = tf_minutes * self.signal_validity_bars
            if validity_min < 60:
                validity_str = f"{validity_min} min"
            else:
                validity_str = f"{validity_min // 60} hours"

            direction = "BUY" if direction_val == 1 else "SELL"
            
            # Fetch current price for SL/TP calculation in bot
            symbol_info = mt5.symbol_info(symbol)
            price = symbol_info.ask if direction == "BUY" else symbol_info.bid
            indicator_values = {"price": price}

            query = """
                INSERT INTO signals (strategy_id, timestamp, pair, direction, validity_window, indicator_values)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (strategy_id, datetime.now(), symbol, direction, validity_str, json.dumps(indicator_values)))
            
        except Exception as e:
            print(f"[PaperEngine] Error logging signal: {e}")

    def _get_confirmation_trend(self, symbol, confirm_tf_str):
        """Checks EMA 20 vs EMA 50 on the specified higher timeframe."""
        # Convert TF string to MT5 constant
        confirm_tf = getattr(mt5, f"TIMEFRAME_{confirm_tf_str}", None)
        if not confirm_tf:
            return 0
            
        # Fetch 100 bars of higher TF
        rates = mt5.copy_rates_from_pos(symbol, confirm_tf, 0, 100)
        if rates is None or len(rates) < 50:
            return 0
            
        import pandas as pd
        df = pd.DataFrame(rates)
        ema20 = df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
        ema50 = df['close'].ewm(span=50, adjust=False).mean().iloc[-1]
        
        if ema20 > ema50:
            return 1  # Bullish trend
        elif ema20 < ema50:
            return -1 # Bearish trend
        else:
            return 0  # Neutral / Choppy


    # ════════════════════════════════════════════════════════════════════════════
    # PHASE 0 FIX #1: SIGNAL DEDUPLICATION (IMPROVEMENTS)
    # ════════════════════════════════════════════════════════════════════════════
    
    def _clean_dedup_cache(self):
        """
        PHASE 0 FIX #1: Clean up old signal hashes to prevent memory leaks.
        Removes entries older than dedup_window (prevents unbounded cache growth).
        """
        from datetime import datetime, timedelta
        
        current_time = datetime.now()
        dedup_window_minutes = 5
        dedup_window = timedelta(minutes=dedup_window_minutes)
        
        # Remove entries older than dedup window
        expired_keys = [
            key for key, timestamp in self.attempted_signals.items()
            if (current_time - timestamp).total_seconds() > dedup_window.total_seconds()
        ]
        
        for key in expired_keys:
            del self.attempted_signals[key]
        
        if expired_keys:
            print(f"[PaperEngine] Cleaned {len(expired_keys)} expired dedup entries")
        
        return len(self.attempted_signals)

    def _create_signal_key(self, strat_name: str, symbol: str, timeframe: int, direction: int) -> tuple:
        """
        PHASE 0 FIX #1: Create a consistent signal key for deduplication.
        Key format: (strategy_name, symbol, timeframe, direction)
        """
        return (strat_name, symbol, timeframe, direction)

    def _check_signal_duplicate(self, signal_key: tuple, signal_time) -> bool:
        """
        PHASE 0 FIX #1: Check if this signal has been processed recently.
        Returns: True if duplicate (should skip), False if new (should process)
        """
        if signal_key in self.attempted_signals:
            # Check if it's the exact same signal (same timestamp)
            if self.attempted_signals[signal_key] == signal_time:
                return True  # Duplicate detected
        
        return False  # New signal

    def _track_processed_signal(self, signal_key: tuple, signal_time):
        """
        PHASE 0 FIX #1: Mark this signal as processed.
        Matches the signal_time (bar timestamp) to prevent duplicate execution on same bar.
        """
        self.attempted_signals[signal_key] = signal_time
        
        # Periodically clean cache
        if len(self.attempted_signals) % 100 == 0:
            self._clean_dedup_cache()