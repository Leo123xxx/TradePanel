import time
import zlib
import traceback
from datetime import datetime
try:
    import MetaTrader5 as mt5
except ImportError:
    from mt5_bridge.docker_mock import setup_mock
    setup_mock()
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
        
        # Phase 1: Reconcile open positions on startup
        self.magic_to_strategy = {
            zlib.adler32(name.encode()) % 1000000: name
            for name in STRATEGY_REGISTRY
        }
        self._reconcile_open_positions()

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
                wait_secs = min(2 ** count, 300)  # Exponential backoff
                if time.time() - last_time < wait_secs:
                    if int(time.time()) % 60 == 0:
                        print(f"[BACKOFF] {strat_name} on {symbol}: Waiting {wait_secs:.0f}s before retry.")
                    return

            # 1. Fetch current bot positions
            positions = self._get_bot_positions(symbol)
            
            # 2. Get latest market data and calculate ATR (needed for both BE and Entry)
            df = self.signal_checker.get_latest_data(symbol, mt5_tf, count=50)
            latest_atr = None
            if df is not None and not df.empty:
                df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
                latest_atr = df['atr'].iloc[-1]

            # 3. IF positions exist, manage them (Breakeven & Reversal)
            if positions:
                # 3.1 Breakeven Management (Phase 3)
                self._manage_breakeven(symbol, strategy, positions, latest_atr)
                
                # 3.2 Check for reversal signal
                signal, signal_time, is_stale = self.signal_checker.get_signal(
                    strategy, symbol, mt5_tf, lookback_bars=self.signal_validity_bars
                )
                if signal != 0 and signal_time is not None:
                    for pos in positions:
                        if (pos.type == mt5.POSITION_TYPE_BUY and signal == -1) or \
                           (pos.type == mt5.POSITION_TYPE_SELL and signal == 1):
                            print(f"REVERSAL DETECTED: Closing position {pos.ticket}")
                            res, msg = self.order_manager.close_position(pos.ticket, "SIGNAL_REVERSAL")
                            if res is not None and res.retcode == mt5.TRADE_RETCODE_DONE:
                                 self._log_trade_close(pos.ticket, res)
                            else:
                                 print(f"FAILED to close on reversal: {msg}")
                                 self.failed_attempts[key] = (self.failed_attempts.get(key, (0, 0))[0] + 1, time.time())
                return # If we have positions, we don't look for new entries on this symbol/tf

            # 4. IF NO positions, check for entry signal
            signal, signal_time, is_stale = self.signal_checker.get_signal(
                strategy, symbol, mt5_tf, lookback_bars=self.signal_validity_bars
            )

            if is_stale:
                print(f"[PaperEngine] [SYNC] Stale data detected for {symbol}. Triggering forced reconnect...")
                self.connector.connect(force=True)
                signal, signal_time, is_stale = self.signal_checker.get_signal(
                    strategy, symbol, mt5_tf, lookback_bars=self.signal_validity_bars
                )
            
            # 5. Signal Deduplication
            signal_key = self._create_signal_key(strat_name, symbol, mt5_tf, signal)
            if signal != 0 and signal_time is not None:
                if self._check_signal_duplicate(signal_key, signal_time):
                    return
            
            if signal != 0:
                self._log_signal(strat_name, symbol, signal, mt5_tf, signal_time=signal_time)
                self._track_processed_signal(signal_key, signal_time)

            if mode == 'detect' or signal == 0:
                return

            # --- PATH B: MULTI-TF CONFIRMATION ---
            confirm_tf = strategy.confirm_tf
            if self.use_confirm_tf and confirm_tf:
                trend = self._get_confirmation_trend(symbol, confirm_tf)
                if (signal == 1 and trend == -1) or (signal == -1 and trend == 1):
                    print(f"[CONFIRM] Skipping {signal} on {symbol} — {confirm_tf} trend conflicts")
                    return

            # 6. Regime Filter
            direction = "BUY" if signal == 1 else "SELL"
            if (self.use_regime_filter or strategy.use_regime_filter) and "XAU" in symbol:
                bias = self.regime_classifier.get_pair_bias(symbol)
                if (bias == 1 and direction == "SELL") or (bias == -1 and direction == "BUY") or (bias == 0):
                    print(f"[REGIME] Skipping {direction} on {symbol} due to macro bias {bias}")
                    return

            # 7. Calculate SL/TP Targets
            sl_points = 0
            tp_points = 0
            if latest_atr is not None:
                symbol_info = mt5.symbol_info(symbol)
                sl_mult = strategy.params.get('sl_atr_mult', 1.0)
                tp_mult = strategy.params.get('tp_atr_mult', 1.5)
                sl_points = (latest_atr * sl_mult) / symbol_info.point
                tp_points = (latest_atr * tp_mult) / symbol_info.point
                print(f"[PaperEngine] Calculated Targets ({strat_name}): SL={sl_points:.1f} pts, TP={tp_points:.1f} pts")

            # 8. Dynamic Lot Sizing (1% Risk Rule)
            lot_size = self.risk_manager.calculate_lot_size(symbol, sl_points)
            
            # 9. RISK CHECK
            passed, reason = self.risk_manager.check_all(strat_name, symbol, lot_size, direction)
            if not passed:
                print(f"RISK BLOCKED: {reason}")
                return

            magic_number = zlib.adler32(strat_name.encode()) % 1000000
            print(f"EXECUTING: {direction} {lot_size} lots on {symbol} (Magic: {magic_number})")
            res, msg = self.order_manager.open_position(
                symbol, direction, lot_size, 
                sl_points=sl_points, tp_points=tp_points, 
                comment=f"PAPER_{strat_name}",
                magic=magic_number
            )
            
            self._track_processed_signal(signal_key, signal_time)

            if res is not None and res.retcode == mt5.TRADE_RETCODE_DONE:
                self._log_trade_open(strat_name, symbol, direction, lot_size, res, sl_points, tp_points)
                if key in self.failed_attempts: del self.failed_attempts[key]
            else:
                print(f"FAILED to open trade: {msg}")
                self.failed_attempts[key] = (self.failed_attempts.get(key, (0, 0))[0] + 1, time.time())

        except Exception as e:
            print(f"[PaperEngine] [FAIL] Error in _process_symbol ({strat_name}/{symbol}): {e}")
            traceback.print_exc()

    def _manage_breakeven(self, symbol, strategy, positions, latest_atr):
        """Moves SL to breakeven if price has moved sufficiently in profit (Phase 3)."""
        try:
            use_be = strategy.params.get('use_breakeven', False)
            if not use_be or latest_atr is None:
                return

            trigger_mult = strategy.params.get('breakeven_trigger_mult', 1.5)
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info: return

            for pos in positions:
                # Skip if SL is already at or beyond entry
                entry = pos.price_open
                current_sl = pos.sl
                is_buy = pos.type == mt5.POSITION_TYPE_BUY
                
                # Check if SL is already at breakeven
                if is_buy:
                    if current_sl >= entry: continue
                else:
                    if current_sl <= entry and current_sl != 0: continue

                # Calculate current profit in points
                current_price = symbol_info.bid if is_buy else symbol_info.ask
                profit_points = (current_price - entry) if is_buy else (entry - current_price)
                profit_points /= symbol_info.point
                
                trigger_points = (latest_atr * trigger_mult) / symbol_info.point
                
                if profit_points >= trigger_points:
                    # Move to breakeven + 10 points buffer
                    buffer_points = 10 * symbol_info.point
                    new_sl = entry + buffer_points if is_buy else entry - buffer_points
                    
                    print(f"[BREAKEVEN] Triggered for {symbol} ticket {pos.ticket}. Moving SL to {new_sl}")
                    res, msg = self.order_manager.modify_position(pos.ticket, sl=new_sl, tp=pos.tp)
                    if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
                        print(f"[BREAKEVEN] Failed to modify {pos.ticket}: {msg}")
        except Exception as e:
            print(f"[PaperEngine] Error in _manage_breakeven: {e}")

    def _reconcile_open_positions(self):
        """
        Scans MT5 for open positions with bot magic numbers.
        Adds them to attempted_signals so the bot knows they exist.
        """
        try:
            positions = mt5.positions_get() or []
            bot_positions = [p for p in positions if p.magic != 0]
            
            reconciled_count = 0
            for p in bot_positions:
                strat_name = self.magic_to_strategy.get(p.magic)
                if not strat_name:
                    continue
                
                # Mock a signal key to prevent re-entry
                # We don't know the exact timeframe it was opened on, so we mark it
                # for the current tf being scanned if possible, but the best is to
                # mark it for all timeframes the strategy uses.
                strat_cfg = next((s for s in self.strategies_cfg if s['name'] == strat_name), None)
                if strat_cfg:
                    for tf_str in strat_cfg.get('timeframes', []):
                        mt5_tf = getattr(mt5, f"TIMEFRAME_{tf_str}", mt5.TIMEFRAME_H1)
                        # We don't know the signal direction from the position easily without logic
                        # but we can mark both BUY and SELL for that bar to be safe
                        # Or better, just mark the one that matches position type
                        direction = 1 if p.type == mt5.POSITION_TYPE_BUY else -1
                        signal_key = self._create_signal_key(strat_name, p.symbol, mt5_tf, direction)
                        
                        # Use position open time as signal time
                        # mt5 position time is in seconds
                        sig_time = p.time
                        self._track_processed_signal(signal_key, sig_time)
                
                # Verify trade exists in DB trades table
                rows = self.db.execute_query(
                    "SELECT 1 FROM trades WHERE mt5_ticket = %s", (p.ticket,)
                )
                if not rows:
                    print(f"[PaperEngine] Orphaned position detected (ticket={p.ticket}). Recovering...")
                    self._recover_orphaned_position(p, strat_name)
                
                reconciled_count += 1
            
            if reconciled_count > 0:
                print(f"[PaperEngine] Reconciled {reconciled_count} open positions on startup.")
                
        except Exception as e:
            print(f"[PaperEngine] Error in _reconcile_open_positions: {e}")

    def _recover_orphaned_position(self, pos, strat_name):
        """Inserts a missing trade record for an existing MT5 position."""
        import uuid
        trade_id = str(uuid.uuid4())
        
        strat_info = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strat_name,))
        strategy_id = strat_info[0][0] if strat_info else None
        
        direction = "BUY" if pos.type == mt5.POSITION_TYPE_BUY else "SELL"
        open_time = datetime.fromtimestamp(pos.time)
        
        query = (
            "INSERT INTO trades "
            "(trade_id, strategy_id, mode, account_id, pair, direction, lot_size, entry_price, open_time, status, mt5_ticket) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        self.db.execute_query(query, (
            trade_id, strategy_id, 'PAPER', 1, pos.symbol, direction, pos.volume,
            pos.price_open, open_time, 'OPENED', pos.ticket
        ))
        print(f"[PaperEngine] Recovered trade {trade_id} for ticket {pos.ticket}")

    def _get_bot_positions(self, symbol):
        """Returns only positions opened by this bot (non-zero magic)."""
        all_positions = mt5.positions_get(symbol=symbol) or []
        
        # Calculate active strategy magics
        bot_magics = {zlib.adler32(name.encode()) % 1000000 
                      for name in self.active_strategies}
        
        bot_positions = [p for p in all_positions if p.magic in bot_magics]
        
        # Log skipping of manual positions
        for p in all_positions:
            if p.magic == 0:
                print(f"[PaperEngine] Skipping manual position ticket={p.ticket} magic=0")
        
        return bot_positions

    def _log_trade_open(self, strat_name, symbol, direction, lot, result,
                        sl_points=0, tp_points=0):
        """Logs the trade to DB and pushes a Telegram notification with full strategy context."""
        import uuid
        trade_id = str(uuid.uuid4())

        # Strategy ID fetch — names stored lowercase in DB, match exactly
        strat_info = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strat_name,))
        if not strat_info:
            strat_info = self.db.execute_query(
                "INSERT INTO strategies (name, category) VALUES (%s, %s) RETURNING strategy_id",
                (strat_name, "paper")
            )
        strategy_id = strat_info[0][0] if strat_info else None

        query = (
            "INSERT INTO trades "
            "(trade_id, strategy_id, mode, account_id, pair, direction, lot_size, entry_price, open_time, status, mt5_ticket) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        # account_id=1 is the Demo account profile (MT5 .env credentials are Demo)
        self.db.execute_query(query, (
            trade_id, strategy_id, 'PAPER', 1, symbol, direction, lot,
            result.price, datetime.now(), 'OPENED', result.order
        ))

        # Build actual SL/TP price levels from points (sl_points/tp_points are MT5 points)
        symbol_info = mt5.symbol_info(symbol)
        digits = symbol_info.digits if symbol_info else 5
        point = symbol_info.point if symbol_info else 0.00001

        sl_price = 0
        tp_price = 0
        if sl_points > 0:
            sl_dist = sl_points * point
            sl_price = round(result.price - sl_dist if direction == "BUY" else result.price + sl_dist, digits)
        if tp_points > 0:
            tp_dist = tp_points * point
            tp_price = round(result.price + tp_dist if direction == "BUY" else result.price - tp_dist, digits)

        # Pull strategy-specific ATR multipliers for the notification
        strategy_obj = self.active_strategies.get(strat_name)
        sl_mult = strategy_obj.params.get('sl_atr_mult', 1.0) if strategy_obj and hasattr(strategy_obj, 'params') else 1.0
        tp_mult = strategy_obj.params.get('tp_atr_mult', 1.5) if strategy_obj and hasattr(strategy_obj, 'params') else 1.5

        dir_icon = "🟢 BUY" if direction == "BUY" else "🔴 SELL"
        notif_data = {
            "symbol": symbol,
            "direction": dir_icon,
            "strategy": strat_name,
            "lot_size": lot,
            "entry_price": round(result.price, digits),
            "sl": sl_price if sl_price else "—",
            "tp": tp_price if tp_price else "—",
            "sl_mult": sl_mult,
            "tp_mult": tp_mult,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S SAST"),
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

    def _log_signal(self, strat_name, symbol, direction_val, mt5_tf, signal_time=None):
        """Logs the detected signal to the database and pushes a Telegram alert
        if the signal bar is within the 15-minute freshness window."""
        try:
            import pandas as pd
            import pytz

            # 1. Resolve strategy_id
            strat_info = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strat_name,))
            if not strat_info:
                strat_info = self.db.execute_query(
                    "INSERT INTO strategies (name, category) VALUES (%s, %s) RETURNING strategy_id",
                    (strat_name, "paper")
                )
            strategy_id = strat_info[0][0] if strat_info else None

            # 2. Calculate validity window
            tf_minutes = {
                mt5.TIMEFRAME_M1: 1,
                mt5.TIMEFRAME_M5: 5,
                mt5.TIMEFRAME_M15: 15,
                mt5.TIMEFRAME_M30: 30,
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

            # 3. Fetch current price
            symbol_info = mt5.symbol_info(symbol)
            price = symbol_info.ask if direction == "BUY" else symbol_info.bid
            indicator_values = {"price": price}

            tf_str = {
                mt5.TIMEFRAME_M1: "M1",
                mt5.TIMEFRAME_M5: "M5",
                mt5.TIMEFRAME_M15: "M15",
                mt5.TIMEFRAME_M30: "M30",
                mt5.TIMEFRAME_H1: "H1",
                mt5.TIMEFRAME_H4: "H4",
                mt5.TIMEFRAME_D1: "D1"
            }.get(mt5_tf, "H1")

            # 4. Insert into DB
            query = """
                INSERT INTO signals (strategy_id, timestamp, pair, direction, validity_window, indicator_values, timeframe)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (
                strategy_id, datetime.now(), symbol, direction,
                validity_str, json.dumps(indicator_values), tf_str
            ))

            # 5. Push Telegram alert if signal bar is within 15-minute freshness window.
            #    signal_time is the bar open timestamp (UTC from MT5). We compare against
            #    UTC now. For M1/M5/M15 strategies this fires immediately. For H1+ it only
            #    fires on the first bar after a new signal bar opens (age <= 15 min).
            if signal_time is not None:
                try:
                    sig_ts = pd.Timestamp(signal_time)
                    if sig_ts.tzinfo is not None:
                        sig_ts = sig_ts.tz_convert(None)  # strip tz, treat as UTC
                    now_utc = pd.Timestamp.utcnow().tz_localize(None)
                    age_minutes = (now_utc - sig_ts).total_seconds() / 60

                    if age_minutes <= 15:
                        self._push_signal_alert(
                            strat_name, symbol, direction, price,
                            tf_str, sig_ts, symbol_info
                        )
                except Exception as push_err:
                    print(f"[PaperEngine] Signal push error ({symbol}): {push_err}")

        except Exception as e:
            print(f"[PaperEngine] Error logging signal: {e}")

    def _push_signal_alert(self, strat_name, symbol, direction, price, tf_str, sig_ts, symbol_info):
        """Formats and sends an immediate Telegram signal alert with strategy-specific SL/TP."""
        try:
            import pytz
            from notifications import templates

            SAST = pytz.timezone('Africa/Johannesburg')

            # Retrieve strategy params for SL/TP multipliers
            strategy_obj = self.active_strategies.get(strat_name)
            sl_mult = 1.0
            tp_mult = 1.5
            if strategy_obj and hasattr(strategy_obj, 'params'):
                sl_mult = strategy_obj.params.get('sl_atr_mult', sl_mult)
                tp_mult = strategy_obj.params.get('tp_atr_mult', tp_mult)

            # Compute ATR-based SL/TP prices for the alert
            mt5_tf = getattr(mt5, f"TIMEFRAME_{tf_str}", mt5.TIMEFRAME_H1)
            df = self.signal_checker.get_latest_data(symbol, mt5_tf, count=50)
            sl_price = "N/A"
            tp_price = "N/A"
            if df is not None and not df.empty:
                import ta_compat as ta
                df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
                atr = df['atr'].iloc[-1]
                sl_dist = atr * sl_mult
                tp_dist = atr * tp_mult
                digits = symbol_info.digits
                if direction == "BUY":
                    sl_price = round(price - sl_dist, digits)
                    tp_price = round(price + tp_dist, digits)
                else:
                    sl_price = round(price + sl_dist, digits)
                    tp_price = round(price - tp_dist, digits)

            # Convert bar time to SAST for display
            bar_time_sast = sig_ts.tz_localize('UTC').astimezone(SAST).strftime("%H:%M")

            dir_icon = "🟢 BUY" if direction == "BUY" else "🔴 SELL"
            msg = templates.SIGNAL_ALERT.format(
                symbol=symbol,
                direction=dir_icon,
                strategy=strat_name,
                timeframe=tf_str,
                bar_time=bar_time_sast,
                entry_price=round(price, symbol_info.digits),
                sl=sl_price,
                tp=tp_price,
                sl_mult=sl_mult,
                tp_mult=tp_mult,
            )
            self.notif_bot.send_sync_message(msg)
            print(f"[PaperEngine] Signal alert pushed: {strat_name} {symbol} {direction} [{tf_str}]")

        except Exception as e:
            print(f"[PaperEngine] _push_signal_alert error: {e}")

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

        FIX (2026-04-30): The cache now stores (signal_time, tracked_at) tuples.
        Expiry is based on tracked_at (wall clock) so D1/H4 bar timestamps —
        which are many hours in the past — no longer cause immediate expiry.
        Window extended to 25h to safely cover a full D1 bar + buffer.
        """
        from datetime import datetime, timedelta

        current_time = datetime.now()
        # 25 hours covers D1 bars (24h) plus a buffer so signals aren't re-logged
        # on the next scheduler cycle after a long-lived bar expires.
        dedup_window = timedelta(hours=25)

        # Remove entries where the wall-clock tracking time is older than the window
        expired_keys = [
            key for key, (_, tracked_at) in self.attempted_signals.items()
            if (current_time - tracked_at).total_seconds() > dedup_window.total_seconds()
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

        FIX (2026-04-30): Cache values are now (signal_time, tracked_at) tuples.
        Duplicate detection still uses signal_time equality (same bar = same signal),
        but expiry is driven by tracked_at (wall clock) in _clean_dedup_cache.
        """
        if signal_key in self.attempted_signals:
            stored_signal_time, _ = self.attempted_signals[signal_key]
            if stored_signal_time == signal_time:
                return True  # Duplicate: same bar, already processed

        return False  # New signal

    def _track_processed_signal(self, signal_key: tuple, signal_time):
        """
        PHASE 0 FIX #1: Mark this signal as processed.

        FIX (2026-04-30): Store (signal_time, datetime.now()) so the cache
        expiry in _clean_dedup_cache is anchored to wall clock, not the bar's
        open timestamp. D1 bar timestamps are 24h in the past the moment they
        close, which caused the old single-value cache to expire immediately and
        re-log the same signal every hour.
        """
        self.attempted_signals[signal_key] = (signal_time, datetime.now())

        # Periodically clean cache
        if len(self.attempted_signals) % 100 == 0:
            self._clean_dedup_cache()