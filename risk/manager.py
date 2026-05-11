import yaml
import os
from datetime import datetime
from mt5_bridge.account import MT5Account
from data.db_client import DBClient
import MetaTrader5 as mt5
import pandas as pd
import ta_compat as ta
from risk.correlation_engine import CorrelationEngine
from risk.regime_classifier import RegimeClassifier

class RiskManager:
    def __init__(self, config_path="config/config.yaml"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        # Load strategies.yaml for detailed metadata (regime, category, etc.)
        strat_path = os.path.join(os.path.dirname(config_path), "strategies.yaml")
        if os.path.exists(strat_path):
            with open(strat_path, 'r') as f:
                self.strategies_meta = yaml.safe_load(f)
        else:
            self.strategies_meta = {}
            
        self.account = MT5Account()
        self.db = DBClient() # Added for regime lookups
        self.correlation_engine = CorrelationEngine(self.db)
        self.regime_classifier = RegimeClassifier()

    def check_all(self, strategy_name, pair, lot_size, direction):
        """
        Runs the pre-trade checks.
        Returns (bool, str): (Passed, Reason)
        """
        # 0. Circuit Breaker / Manual Pause Check
        is_paused, pause_msg = self._is_bot_paused()
        if is_paused:
            return False, pause_msg

        # 0.1 Blocked Pairs Check
        if not self._check_blocked_pairs(pair):
            return False, f"RiskCheck Failed: {pair} is in the blocked_pairs list."

        # 0.2 News Blackout Check
        if self._is_news_blackout_active():
            return False, "RiskCheck Failed: News blackout active."

        # 1. Strategy is active and not paused
        if not self._check_strategy_active(strategy_name, pair):
            return False, f"RiskCheck Failed: Strategy {strategy_name} is disabled/paused."

        # 2. Market regime matches strategy category
        if not self._check_regime(strategy_name, pair):
            return False, "RiskCheck Failed: Market regime not suitable for this strategy."

        # 3. Lot size <= max_lot_size in config
        max_lot = self.config['risk_management']['max_lot_size']
        if lot_size > max_lot:
            return False, f"RiskCheck Failed: Lot size {lot_size} exceeds max limit of {max_lot}."

        # 4. Total positions < max_concurrent_positions
        if not self._check_concurrent_positions():
            return False, f"RiskCheck Failed: Max concurrent positions ({self.config['risk_management']['max_concurrent_positions']}) reached."

        # 5. Margin available in MT5 account
        if not self._check_margin(pair, lot_size, direction):
            return False, "RiskCheck Failed: Insufficient free margin available."

        # 6. Current spread <= max_spread_pips
        if not self._check_spread(pair):
            return False, f"RiskCheck Failed: Current spread exceeds max allowed ({self.config['risk_management']['max_spread_pips']} pips)."

        # 7. Within permitted trading hours
        if not self._check_trading_hours(pair):
            return False, "RiskCheck Failed: Outside of configured trading hours/days."

        # 8. High-Timeframe (D1) Trend Alignment
        if not self._check_htf_trend(strategy_name, pair, direction):
            return False, f"RiskCheck Failed: Counter-trend signal (D1 EMA 200 gate)."

        # 9. Macro Bias Alignment
        if not self._check_macro_bias(pair, direction):
            return False, f"RiskCheck Failed: Signal conflicts with Global Macro Bias."

        # 10. Correlation Check (Phase 5 - WARNING ONLY)
        is_redundant, corr_val = self.correlation_engine.check_signal_redundancy(strategy_name, pair, mt5.positions_get())
        if is_redundant:
            # We don't return False here because user wanted only WARNINGS
            print(f"⚠️ [CORRELATION WARNING] Signal for {strategy_name} on {pair} detected high redundancy ({corr_val:.2f}) with existing positions.")

        return True, "All risk checks passed."

    def calculate_lot_size(self, symbol, sl_points):
        """
        Calculates lot size for the configured risk percentage (default 1%) 
        based on SL distance in points.
        Formula: LotSize = RiskAmount / (SL_Ticks * TickValue)
        """
        try:
            if sl_points <= 0:
                return self.config['risk_management'].get('default_lot_size', 0.1)

            # 1. Get Risk Amount in ZAR
            balance = self.account.get_balance()
            risk_pct = self.config['risk_management'].get('risk_per_trade_pct', 1.0)
            risk_amount_zar = balance * (risk_pct / 100.0)

            # 2. Get MT5 Symbol Info
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return 0.1

            # Tick values in MT5 are expressed in account currency (ZAR)
            tick_value = symbol_info.trade_tick_value
            tick_size = symbol_info.trade_tick_size
            point = symbol_info.point

            if tick_value <= 0 or tick_size <= 0:
                return 0.1

            # 3. Calculate Lot Size
            sl_ticks = (sl_points * point) / tick_size
            if sl_ticks <= 0:
                return 0.1

            lot_size = risk_amount_zar / (sl_ticks * tick_value)
            
            # 4. Apply Constraints
            min_lot = symbol_info.volume_min
            max_lot_hard = self.config['risk_management'].get('max_lot_size', 1.0)
            max_lot = min(symbol_info.volume_max, max_lot_hard)

            # Round to lot_step (usually 0.01)
            lot_step = symbol_info.volume_step
            lot_size = round(lot_size / lot_step) * lot_step
            
            final_lots = max(min_lot, min(max_lot, lot_size))
            
            print(f"[RiskManager] Risk: R{risk_amount_zar:.2f} | SL: {sl_points:.1f} pts | Lots: {final_lots:.2f} (Calc: {lot_size:.4f})")
            return round(final_lots, 2)

        except Exception as e:
            print(f"[RiskManager] Error calculating lot size: {e}")
            return 0.1

    def _check_blocked_pairs(self, pair):
        """Returns False if the pair is in the blocked_pairs list."""
        blocked = self.config['risk_management'].get('blocked_pairs', [])
        return pair.upper() not in [p.upper() for p in blocked]

    def _is_news_blackout_active(self):
        """Checks if a news blackout is currently active in bot_health table."""
        try:
            # Query for the most recent NEWS_BLACKOUT event
            query = "SELECT status, message FROM bot_health WHERE event_type = 'NEWS_BLACKOUT' LIMIT 1"
            res = self.db.execute_query(query)
            if not res:
                return False
                
            status, end_time_str = res[0]
            if status != 'PAUSED':
                return False
                
            # end_time_str is expected to be ISO format timestamp
            from datetime import datetime
            try:
                end_time = datetime.fromisoformat(end_time_str)
                if datetime.now() < end_time:
                    return True
            except (ValueError, TypeError):
                # Fallback: if message isn't a timestamp, assume it's active if status is PAUSED
                return True
                
            return False
        except Exception as e:
            print(f"[RiskManager] Error checking news blackout: {e}")
            return False

    def calculate_kelly_size(self, strategy_name, symbol, base_lots=0.1):
        """
        Calculates the adaptive lot size based on the Kelly Criterion.
        K = W - (1 - W) / R
        where W is win rate and R is payoff ratio (avg win / avg loss).
        
        Using a 'Fractional Kelly' (0.25) for safety.
        """
        try:
            strategy_id = self._get_strategy_id(strategy_name)
            if not strategy_id:
                return base_lots

            # Query recent trades (last 50 CLOSED trades)
            query = """
                SELECT pnl FROM trades 
                WHERE strategy_id = %s AND pair = %s AND status = 'CLOSED' 
                ORDER BY close_time DESC LIMIT 50
            """
            rows = self.db.execute_query(query, (strategy_id, symbol))

            if len(rows) < 10:
                # Not enough data for Kelly, return base
                return base_lots

            pnls = [float(r[0]) for r in rows]
            wins = [p for p in pnls if p > 0]
            losses = [abs(p) for p in pnls if p < 0]

            if not losses:
                return base_lots * 1.5 # Scale up slightly if 100% win rate (unlikely)

            win_rate = len(wins) / len(pnls)
            avg_win = sum(wins) / len(wins) if wins else 0
            avg_loss = sum(losses) / len(losses) if losses else 1 # Avoid div by zero

            payoff_ratio = avg_win / avg_loss
            
            # Kelly Logic
            if payoff_ratio == 0:
                return base_lots
                
            kelly_fraction = win_rate - (1 - win_rate) / payoff_ratio
            
            # Apply Quarter-Kelly (0.25 safety multiplier)
            # And cap it between 0.5x and 3.0x of base_lots
            safe_kelly = max(0.1, kelly_fraction * 0.25)
            multiplier = min(3.0, max(0.5, safe_kelly * 10.0)) # Mapping 0.1 Kelly to 1x multiplier approx
            
            # Alternative: direct lot sizing if we have equity
            # But lot multiplier is safer for existing logic
            adjusted_lots = round(base_lots * multiplier, 2)
            
            print(f"[KELLY] Strategy: {strategy_name} | WR: {win_rate:.2f} | R: {payoff_ratio:.2f} | K: {kelly_fraction:.2f} | Mult: {multiplier:.2f} | Lots: {adjusted_lots}")
            
            return adjusted_lots

        except Exception as e:
            print(f"[KELLY] Error calculating size: {e}")
            return base_lots

    def _is_bot_paused(self):
        """
        Queries bot_health table for a CIRCUIT_BREAKER or MANUAL_PAUSE row
        newer than today's start or currently active.
        """
        try:
            # Check for CIRCUIT_BREAKER today
            query = """
                SELECT status, message FROM bot_health 
                WHERE event_type = 'CIRCUIT_BREAKER' 
                AND status = 'PAUSED'
                AND timestamp >= CURRENT_DATE 
                ORDER BY timestamp DESC LIMIT 1
            """
            rows = self.db.execute_query(query)
            if rows:
                return True, f"RiskCheck Failed: Circuit breaker active — {rows[0][1]}"

            # Check for MANUAL_PAUSE
            query = """
                SELECT status, message, meta_data FROM bot_health 
                WHERE event_type = 'MANUAL_PAUSE' 
                AND status = 'PAUSED'
                ORDER BY timestamp DESC LIMIT 1
            """
            rows = self.db.execute_query(query)
            if rows:
                meta = rows[0][2]
                if meta and 'resume_at' in meta:
                    resume_at = datetime.fromisoformat(meta['resume_at'])
                    if datetime.now() < resume_at:
                        return True, f"RiskCheck Failed: Manual pause active until {resume_at.strftime('%H:%M')}."
                    else:
                        # Auto-resume logic: update status to ACTIVE
                        self.db.execute_query(
                            "UPDATE bot_health SET status = 'ACTIVE' WHERE event_type = 'MANUAL_PAUSE'"
                        )
                        return False, ""
                return True, "RiskCheck Failed: Manual pause active."

            return False, ""
        except Exception as e:
            print(f"[RiskManager] Error checking pause state: {e}")
            return False, ""

    def _get_strategy_id(self, strategy_name):
        res = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strategy_name,))
        if res:
            return res[0][0]
        return None

    def _check_strategy_active(self, strategy_name, pair=None):
        strat_meta = self.strategies_meta.get(strategy_name.lower())
        if strat_meta is None:
            return False  # Unknown strategy
            
        if not strat_meta.get('enabled', False):
            return False
            
        # Check pair-level override
        if pair:
            overrides = strat_meta.get('pair_overrides', {})
            if pair in overrides:
                return overrides[pair].get('enabled', True)
                
        return True

    def _check_regime(self, strategy_name, pair):
        """
        Checks if the current market regime for the pair matches the strategy's allowed regimes.
        Allowed regimes in config are typically ['TRENDING', 'RANGING', 'ANY'].
        """
        # 1. Find strategy's allowed regimes from strategies_meta
        # Note: strategy_name from PaperEngine is lowercase (e.g. 'range_breakout')
        strat_meta = self.strategies_meta.get(strategy_name.lower())
        if not strat_meta:
            return True # If no meta, allow (fallback)
            
        allowed = [r.upper() for r in strat_meta.get('regime', [])]
        if "ANY" in allowed:
            return True

        # 2. Look up the last detected regime from the database
        query = """
            SELECT regime FROM regime_log 
            WHERE pair = %s 
            ORDER BY timestamp DESC LIMIT 1
        """
        rows = self.db.execute_query(query, (pair,))
        if not rows:
            return True # Allow if no data yet
        
        current_regime = rows[0][0].upper() # e.g. 'TRENDING_NORMAL_VOL'
        parts = current_regime.split('_')
        
        # Check if any part of the current regime (base or sub) is allowed
        # e.g. if allowed=['HIGH_VOL'] and current='NEUTRAL_HIGH_VOL', it matches.
        for part in parts:
            if part in allowed:
                return True
        
        # Also check combinations like 'HIGH_VOL'
        if "HIGH" in parts and "VOL" in parts and "HIGH_VOL" in allowed:
            return True

        return False

    def _check_concurrent_positions(self):
        max_pos = self.config['risk_management']['max_concurrent_positions']
        # Only count positions opened by the bot (magic != 0)
        all_positions = mt5.positions_get() or []
        bot_positions = [p for p in all_positions if p.magic != 0]
        return len(bot_positions) < max_pos

    def _check_margin(self, pair, lot_size, direction):
        # Calculate margin required for the proposed trade
        order_type = mt5.ORDER_TYPE_BUY if direction.upper() == "BUY" else mt5.ORDER_TYPE_SELL
        symbol_info = mt5.symbol_info(pair)
        if not symbol_info:
            return False
            
        price = symbol_info.ask if order_type == mt5.ORDER_TYPE_BUY else symbol_info.bid
        margin_required = mt5.order_calc_margin(order_type, pair, lot_size, price)
        
        if margin_required is None:
            return False
            
        free_margin = self.account.get_margin_free()
        # Requirement: Must have enough free margin to cover trade with 20% safety buffer
        return free_margin > (margin_required * 1.2)

    def _check_spread(self, pair):
        symbol_info = mt5.symbol_info(pair)
        if symbol_info is None:
            return False
            
        # spread is in points
        spread_points = getattr(symbol_info, 'spread', 0)
        point_size = getattr(symbol_info, 'point', 0.00001)
        
        # Standard pip size: 0.01 for 2-digit pairs (Gold), 0.0001 for 4/5-digit pairs
        pip_size = 0.01 if symbol_info.digits in [2, 3] else 0.0001
        
        spread_pips = (spread_points * point_size) / pip_size if pip_size != 0 else 0
        max_spread = self.config['risk_management']['max_spread_pips']
        
        return spread_pips <= max_spread

    def _check_trading_hours(self, pair):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.weekday() # 0=Mon, 6=Sun

        risk_cfg = self.config['risk_management']
        
        # Check if it's a crypto pair with special hours
        crypto_cfg = risk_cfg.get('crypto_trading_hours')
        if crypto_cfg and pair in crypto_cfg.get('pairs', []):
            start_time = crypto_cfg['start']
            end_time = crypto_cfg['end']
            allowed_days = crypto_cfg['days']
        else:
            # Standard FX/Metals hours
            start_time = risk_cfg['trading_hours']['start']
            end_time = risk_cfg['trading_hours']['end']
            allowed_days = risk_cfg['trading_hours']['days']

        if current_day not in allowed_days:
            return False
            
        return start_time <= current_time <= end_time

    def _check_htf_trend(self, strategy_name, pair, direction):
        """
        Ensures trend-following strategies align with the Daily (D1) 200 EMA.
        """
        strat_meta = self.strategies_meta.get(strategy_name.lower())
        if not strat_meta:
            return True
            
        category = strat_meta.get('category', '').upper()
        if "TREND" not in category:
            return True # Only enforce on trend strategies

        # Fetch last 250 bars of D1 data for EMA 200
        query = """
            SELECT close FROM market_data 
            WHERE pair = %s AND timeframe = 'D1' 
            ORDER BY timestamp DESC LIMIT 250
        """
        rows = self.db.execute_query(query, (pair,))
        if len(rows) < 200:
            return True # Not enough data to judge

        closes = [float(r[0]) for r in rows][::-1] # Reverse to chronological
        ema200 = ta.ema(pd.Series(closes), length=200).iloc[-1]
        last_close = closes[-1]

        if direction.upper() == "BUY":
            return last_close > ema200
        else:
            return last_close < ema200

    def _check_macro_bias(self, pair, direction):
        """
        Ensures signal aligns with Macro Regime (Risk-On/Off).
        """
        bias = self.regime_classifier.get_pair_bias(pair)
        if bias == 0:
            return True # Neutral bias, allow both
            
        if direction.upper() == "BUY":
            return bias == 1
        else:
            return bias == -1

