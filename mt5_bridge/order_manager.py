import MetaTrader5 as mt5
import yaml
from typing import Dict, Optional
from datetime import datetime

class OrderManager:
    def __init__(self, config_path="config/config.yaml", magic=123456):
        self.magic = magic
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Extract risk management settings
        self.risk_cfg = self.config.get('risk_management', {})
        self.margin_safety_buffer = 1.5  # 150% of required margin
        self.max_portfolio_leverage_fx = self.risk_cfg.get('max_portfolio_leverage_fx', 20)
        self.max_portfolio_leverage_crypto = self.risk_cfg.get('max_portfolio_leverage_crypto', 2)
        self.min_equity_threshold = self.risk_cfg.get('min_equity_threshold', 1000)
        self.trading_hours_fx = self.risk_cfg.get('trading_hours', {})
        self.trading_hours_crypto = self.risk_cfg.get('crypto_trading_hours', {})
        
        # Per-symbol position limits (from config pairs)
        self.per_symbol_limits = {}
        for pair, cfg in self.config.get('pairs', {}).items():
            self.per_symbol_limits[pair] = {
                'max_lot': cfg.get('max_lot', 1.0),
                'min_lot': cfg.get('min_lot', 0.01)
            }

    def _is_trading_hours(self, symbol: str) -> bool:
        """Check if current time falls within allowed trading hours for symbol."""
        from datetime import datetime, time
        import pytz
        
        current_time = datetime.now(pytz.UTC)
        current_hour = current_time.hour
        current_day = current_time.weekday()  # 0=Monday, 6=Sunday
        
        # Crypto pairs: always open
        if symbol in ['BTCUSD', 'ETHUSD']:
            return True
        
        # FX/metals: check configured hours
        trading_hours = self.trading_hours_fx
        start_hour = int(trading_hours.get('start', '00:30').split(':')[0])
        end_hour = int(trading_hours.get('end', '23:59').split(':')[0])
        allowed_days = trading_hours.get('days', [0, 1, 2, 3, 4])
        
        # Check day
        if current_day not in allowed_days:
            return False
        
        # Check hour (simplified: 00:30 = hour 0, 23:59 = hour 23)
        if start_hour <= end_hour:
            return start_hour <= current_hour <= end_hour
        else:
            return current_hour >= start_hour or current_hour <= end_hour

    def _get_account_info(self) -> Dict:
        """Get current account balance, margin, and equity."""
        account_info = mt5.account_info()
        if account_info is None:
            return None
        
        return {
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'margin_level': account_info.margin_level,
        }

    def _calculate_required_margin(self, symbol: str, lot: float) -> Optional[float]:
        """Calculate required margin for a position."""
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return None
        
        # Required margin = lot * point value * required margin % / leverage
        # Simplified: use MT5's built-in calculation
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None
            
        # Required margin = lot * price * contract_size * (margin_required % / leverage)
        # We'll use a conservative 2% margin (50:1) for FX if not specified
        contract_size = getattr(symbol_info, 'trade_contract_size', 100000)
        margin_initial = getattr(symbol_info, 'margin_initial', 0)
        margin_pct = (margin_initial / 100) if margin_initial > 0 else 0.02
        
        margin_required = lot * tick.ask * contract_size * margin_pct
        return margin_required

    def _check_margin(self, symbol: str, lot: float) -> tuple[bool, str]:
        """Validate that account has sufficient free margin."""
        account = self._get_account_info()
        if account is None:
            return False, "Could not retrieve account info"
        
        required_margin = self._calculate_required_margin(symbol, lot)
        if required_margin is None:
            return False, f"Could not calculate required margin for {symbol}"
        
        # Apply safety buffer: require 150% of margin
        required_with_buffer = required_margin * self.margin_safety_buffer
        
        if account['free_margin'] < required_with_buffer:
            return False, (
                f"Insufficient margin: free={account['free_margin']:.2f}, "
                f"required={required_with_buffer:.2f}"
            )
        
        return True, "MARGIN_OK"

    def _check_position_limits(self, symbol: str, lot: float) -> tuple[bool, str]:
        """Check that position size respects per-symbol limits."""
        if symbol not in self.per_symbol_limits:
            return True, "NO_LIMITS_CONFIGURED"
        
        limits = self.per_symbol_limits[symbol]
        max_lot = limits['max_lot']
        
        # Get current position size
        positions = mt5.positions_get(symbol=symbol)
        current_size = sum(p.volume for p in positions) if positions else 0.0
        
        # Check if adding this lot would exceed limit
        new_total = current_size + lot
        if new_total > max_lot:
            return False, (
                f"Position limit exceeded for {symbol}: "
                f"current={current_size:.2f}, "
                f"new_order={lot:.2f}, "
                f"max={max_lot:.2f}"
            )
        
        return True, "POSITION_OK"

    def _check_portfolio_leverage(self, symbol: str, lot: float) -> tuple[bool, str]:
        """Check portfolio-wide leverage against FSCA compliance limits."""
        account = self._get_account_info()
        if account is None:
            return False, "Could not retrieve account info"
        
        # Determine symbol type
        is_crypto = symbol in ['BTCUSD', 'ETHUSD']
        max_leverage = self.max_portfolio_leverage_crypto if is_crypto else self.max_portfolio_leverage_fx
        
        # Current portfolio leverage = total exposure / equity
        # Get all open positions
        total_exposure = 0
        positions = mt5.positions_get()
        if positions:
            total_exposure = sum(p.volume * mt5.symbol_info(p.symbol).bid for p in positions)
            current_leverage = total_exposure / account['equity'] if account['equity'] > 0 else 0
        else:
            current_leverage = 0
        
        # Estimate leverage with new position
        symbol_info = mt5.symbol_info(symbol)
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return False, f"Could not get tick for {symbol}"
        
        new_exposure = lot * tick.ask
        estimated_leverage = (total_exposure + new_exposure) / account['equity'] if account['equity'] > 0 else 0
        
        if estimated_leverage > max_leverage:
            return False, (
                f"Portfolio leverage exceeds limit: "
                f"current={current_leverage:.1f}, "
                f"estimated={estimated_leverage:.1f}, "
                f"max={max_leverage:.1f}"
            )
        
        return True, f"LEVERAGE_OK ({estimated_leverage:.1f}/{max_leverage:.1f})"

    def _check_equity_threshold(self) -> tuple[bool, str]:
        """Verify account equity meets minimum threshold."""
        account = self._get_account_info()
        if account is None:
            return False, "Could not retrieve account info"
        
        if account['equity'] < self.min_equity_threshold:
            return False, (
                f"Account equity below minimum: "
                f"current={account['equity']:.2f}, "
                f"minimum={self.min_equity_threshold:.2f}"
            )
        
        return True, "EQUITY_OK"

    def _validate_order(self, symbol: str, lot: float) -> tuple[bool, str]:
        """Validate order parameters before sending to MT5."""
        # 1. Symbol existence
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return False, f"Symbol {symbol} not found in MT5"
        
        # 2. Ensure symbol is selected
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                return False, f"Symbol {symbol} exists but could not be added to market watch"
            symbol_info = mt5.symbol_info(symbol)

        # 3. Check lot is valid (MT5 limits)
        if lot < symbol_info.volume_min:
            return False, f"Lot {lot} below minimum {symbol_info.volume_min} for {symbol}"
        if lot > symbol_info.volume_max:
            return False, f"Lot {lot} above maximum {symbol_info.volume_max} for {symbol}"
        
        # 4. Check trading hours
        if not self._is_trading_hours(symbol):
            return False, f"Outside trading hours for {symbol}"
        
        # ═══════════════════════════════════════════════════════════
        # PHASE 0 FIX #2: CRITICAL RISK CHECKS
        # ═══════════════════════════════════════════════════════════
        
        # 5. Check equity threshold
        valid, msg = self._check_equity_threshold()
        if not valid:
            return False, msg
        
        # 6. Check margin
        valid, msg = self._check_margin(symbol, lot)
        if not valid:
            return False, msg
        
        # 7. Check position limits
        valid, msg = self._check_position_limits(symbol, lot)
        if not valid:
            return False, msg
        
        # 8. Check portfolio leverage
        valid, msg = self._check_portfolio_leverage(symbol, lot)
        if not valid:
            return False, msg

        return True, "ALL_CHECKS_PASSED"

    def open_position(self, symbol: str, direction: str, lot: float, sl_points: float = 0, tp_points: float = 0, comment: str = "", magic: Optional[int] = None):
        """
        Sends a market order to MT5.
        direction: 'BUY' or 'SELL'
        """
        # 1. Validation
        valid, msg = self._validate_order(symbol, lot)
        if not valid:
            print(f"[OrderManager] Validation FAILED for {symbol}: {msg}")
            return None, msg

        symbol_info = mt5.symbol_info(symbol)
        tick = mt5.symbol_info_tick(symbol)
        digits = symbol_info.digits
        
        if direction.upper() == "BUY":
            type_val = mt5.ORDER_TYPE_BUY
            price = round(tick.ask, digits)
            sl = round(price - (sl_points * symbol_info.point), digits) if sl_points > 0 else 0.0
            tp = round(price + (tp_points * symbol_info.point), digits) if tp_points > 0 else 0.0
        else:
            type_val = mt5.ORDER_TYPE_SELL
            price = round(tick.bid, digits)
            sl = round(price + (sl_points * symbol_info.point), digits) if sl_points > 0 else 0.0
            tp = round(price - (tp_points * symbol_info.point), digits) if tp_points > 0 else 0.0

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": round(lot, 2),
            "type": type_val,
            "price": price,
            "sl": float(sl),
            "tp": float(tp),
            "deviation": 20,
            "magic": magic if magic is not None else self.magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None:
            err = mt5.last_error()
            return None, f"mt5.order_send returned None. MT5 Error: {err}"
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return result, f"Order failed: {result.comment} (code: {result.retcode})"
            
        return result, "SUCCESS"

    def close_position(self, ticket: int, volume: Optional[float] = None, comment: str = ""):
        """Closes an open position (full or partial) by ticket number."""
        positions = mt5.positions_get(ticket=ticket)
        if not positions:
             return None, f"Position {ticket} not found or already closed."
        
        pos = positions[0]
        symbol = pos.symbol
        # Use provided volume or full position volume
        close_volume = round(volume, 2) if volume is not None else pos.volume
        
        order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        tick = mt5.symbol_info_tick(symbol)
        symbol_info = mt5.symbol_info(symbol)
        digits = symbol_info.digits
        price = round(tick.bid if order_type == mt5.ORDER_TYPE_SELL else tick.ask, digits)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(close_volume),
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": self.magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result is None:
            err = mt5.last_error()
            return None, f"mt5.order_send (close) returned None. MT5 Error: {err}"
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return result, f"Close failed: {result.comment} (code: {result.retcode})"
            
        return result, "SUCCESS"

    def close_all_for_symbol(self, symbol: str):
        """Closes all open positions for a specific symbol."""
        positions = mt5.positions_get(symbol=symbol)
        if not positions:
            return True, "No positions to close"
            
        all_success = True
        for p in positions:
            res, msg = self.close_position(p.ticket, "CLOSE_ALL_SYMBOL")
            if not res or res.retcode != mt5.TRADE_RETCODE_DONE:
                all_success = False
        return all_success, "SUCCESS" if all_success else "Partial failure"

    def modify_position(self, ticket: int, sl: float, tp: float):
        """Modifies SL and TP for an existing position."""
        positions = mt5.positions_get(ticket=ticket)
        if not positions:
            return None, f"Position {ticket} not found."
            
        pos = positions[0]
        symbol_info = mt5.symbol_info(pos.symbol)
        digits = symbol_info.digits

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": round(float(sl), digits),
            "tp": round(float(tp), digits),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None:
            err = mt5.last_error()
            return None, f"mt5.order_send (modify) returned None. MT5 Error: {err}"
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return result, f"Modify failed: {result.comment} (code: {result.retcode})"
            
        return result, "SUCCESS"