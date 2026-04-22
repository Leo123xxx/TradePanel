import yaml
import os
from datetime import datetime
from mt5_bridge.account import MT5Account
from data.db_client import DBClient
import MetaTrader5 as mt5
from risk.correlation_engine import CorrelationEngine

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

    def check_all(self, strategy_name, pair, lot_size, direction):
        """
        Runs the 7 pre-trade checks defined in Section 10 of the Master Plan.
        Returns (bool, str): (Passed, Reason)
        """
        # 1. Strategy is active and not paused
        if not self._check_strategy_active(strategy_name):
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

        # 8. Correlation Check (Phase 5 - WARNING ONLY)
        is_redundant, corr_val = self.correlation_engine.check_signal_redundancy(strategy_name, pair, mt5.positions_get())
        if is_redundant:
            # We don't return False here because user wanted only WARNINGS
            print(f"⚠️ [CORRELATION WARNING] Signal for {strategy_name} on {pair} detected high redundancy ({corr_val:.2f}) with existing positions.")

        return True, "All risk checks passed."

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

    def _get_strategy_id(self, strategy_name):
        res = self.db.execute_query("SELECT strategy_id FROM strategies WHERE name = %s", (strategy_name,))
        if res:
            return res[0][0]
        return None

    def _check_strategy_active(self, strategy_name):
        strategies = self.config.get('strategies', [])
        for s in strategies:
            if s['name'].lower() == strategy_name.lower():
                return s.get('enabled', False)
        return False

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
        base_regime = current_regime.split('_')[0] # 'TRENDING'
        
        return base_regime in allowed

    def _check_concurrent_positions(self):
        max_pos = self.config['risk_management']['max_concurrent_positions']
        # mt5.positions_total() returns total open positions
        current_pos = mt5.positions_total()
        if current_pos is None:
             return True # Assume okay if we can't fetch, maybe account is empty
        return current_pos < max_pos

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
        spread_points = symbol_info.spread
        point_size = symbol_info.point
        
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

