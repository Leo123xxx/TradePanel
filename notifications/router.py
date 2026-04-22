import MetaTrader5 as mt5
from data.db_client import DBClient
from datetime import datetime, timedelta
from mt5_bridge.account import MT5Account
import os
import yaml
from pathlib import Path

class CommandRouter:
    def __init__(self):
        self.db = DBClient()
        self.account = MT5Account()

    def get_help(self):
        return (
            "🤖 <b>TradePanel Help</b>\n\n"
            "/status - System and account status\n"
            "/balance - Balance and equity\n"
            "/active - List open positions\n"
            "/signals - Recent strategy signals\n"
            "/analysis - Multi-TF market summary\n"
            "/risk - Account drawdown and risk\n"
            "/mode - Operating mode and strategies\n"
            "/help - Show this list"
        )

    def get_health(self):
        from datetime import datetime, timedelta
        try:
            # Last heartbeat
            rows = self.db.execute_query(
                "SELECT timestamp, status FROM bot_health WHERE event_type = 'HEARTBEAT' ORDER BY timestamp DESC LIMIT 1"
            )
            if rows:
                last_hb = rows[0][0].strftime("%Y-%m-%d %H:%M:%S")
                hb_status = rows[0][1]
            else:
                last_hb = "No heartbeat recorded"
                hb_status = "UNKNOWN"

            # Count warnings/criticals in last 24h
            cutoff = datetime.now() - timedelta(hours=24)
            warn_rows = self.db.execute_query(
                "SELECT COUNT(*) FROM bot_health WHERE status IN ('WARNING','CRITICAL') AND timestamp >= %s",
                (cutoff,)
            )
            warn_count = int(warn_rows[0][0]) if warn_rows else 0

            icon = "🟢" if hb_status == "SUCCESS" else "🔴"
            return (
                f"🏥 <b>System Health</b>\n"
                f"{icon} Last heartbeat: {last_hb}\n"
                f"⚠️ Alerts (24h): {warn_count}"
            )
        except Exception as e:
            return f"❌ Health check error: {e}"

    def get_mode(self):
        try:
            # Mode from .env
            mode = os.getenv("TRADING_MODE", "unknown").upper()

            # Strategies from strategies.yaml
            project_root = Path(__file__).parent.parent
            strat_path = project_root / "config" / "strategies.yaml"
            enabled = []
            if strat_path.exists():
                with open(strat_path) as f:
                    strat_cfg = yaml.safe_load(f)
                
                active_list = strat_cfg.get("active", [])
                for s_name in active_list:
                    # Try to find strategy definition for details
                    s_def = strat_cfg.get(s_name, {})
                    p_list = ", ".join(s_def.get("pairs", ["N/A"]))
                    tf_list = ", ".join(s_def.get("timeframes", ["N/A"]))
                    name = s_def.get("name", s_name)
                    enabled.append(f"  • <b>{name}</b>\n    └ {p_list} ({tf_list})")
            
            strat_list = "\n".join(enabled) if enabled else "  None enabled"

            return (
                f"🛠 <b>Operating Mode: {mode}</b>\n\n"
                f"📋 <b>Active Strategies:</b>\n{strat_list}"
            )
        except Exception as e:
            return f"❌ Mode check error: {e}"

    def get_status(self):
        import yaml
        from collections import defaultdict
        if not mt5.initialize():
            return "❌ Error: Could not connect to MT5."

        info = self.account.get_info()

        # Open positions — query MT5 directly (ground truth, not the DB)
        positions = mt5.positions_get() or []
        open_positions = len(positions)

        # Build a per-symbol breakdown
        pos_lines = ""
        if positions:
            by_symbol = defaultdict(list)
            for p in positions:
                by_symbol[p.symbol].append(p)
            currency = info.get("currency", "USD") if info else "USD"
            for sym, pos_list in by_symbol.items():
                total_profit = sum(p.profit for p in pos_list)
                lots = sum(p.volume for p in pos_list)
                sign = "▲" if total_profit >= 0 else "▼"
                pos_lines += f"\n  {sign} {sym}  {lots:.2f} lot  {total_profit:+.2f} {currency}"

        mt5.shutdown()

        if not info:
            return "❌ Error: Could not fetch account info."

        try:
            mode = os.getenv("TRADING_MODE", "unknown").upper()
            project_root = Path(__file__).parent.parent
            strat_path = project_root / "config" / "strategies.yaml"
            strat_count = 0
            if strat_path.exists():
                with open(strat_path) as f:
                    strat_cfg = yaml.safe_load(f)
                strat_count = len(strat_cfg.get("active", []))
        except Exception:
            mode = "UNKNOWN"
            strat_count = 0

        # Determine Bot Status from DB
        try:
            hb_rows = self.db.execute_query(
                "SELECT timestamp FROM bot_health WHERE event_type = 'HEARTBEAT' ORDER BY timestamp DESC LIMIT 1"
            )
            if hb_rows:
                last_hb = hb_rows[0][0]
                if datetime.now() - last_hb < timedelta(minutes=5):
                    bot_status = "🟢 Bot Status: ACTIVE"
                else:
                    bot_status = f"🔴 Bot Status: INACTIVE (Last HB: {last_hb.strftime('%H:%M:%S')})"
            else:
                bot_status = "🟠 Bot Status: NO DATA"
        except Exception:
            bot_status = "🔴 Bot Status: ERROR"

        status = (
            f"💹 <b>System Status</b>\n"
            f"👤 Account: {info['login']}\n"
            f"💰 Equity: {info['equity']} {info['currency']}\n"
            f"{bot_status}\n"
            f"🛠 Mode: {mode}\n"
            f"📊 Open Positions: {open_positions}"
        )
        if pos_lines:
            status += pos_lines
        status += f"\n📋 Active Strategies: {strat_count}"
        return status

    def get_balance(self):
        if not mt5.initialize():
            return "❌ Error: Could not connect to MT5."
        
        info = self.account.get_info()
        mt5.shutdown()
        
        if not info:
            return "❌ Error: Could not fetch account info."
            
        return (
            "💰 <b>Balance Info</b>\n"
            f"Balance: {info['balance']} {info['currency']}\n"
            f"Equity: {info['equity']} {info['currency']}\n"
            f"Free Margin: {info['margin_free']} {info['currency']}"
        )

    def format_drawdown_warning(self, data: dict):
        from notifications import templates
        return templates.DRAWDOWN_WARNING.format(**data)

    def format_trade_open(self, data: dict):
        from notifications import templates
        return templates.TRADE_OPEN.format(**data)

    def format_trade_close(self, data: dict):
        from notifications import templates
        return templates.TRADE_CLOSE.format(**data)

    def format_daily_summary(self, stats: dict):
        """Format the daily P&L summary Telegram message."""
        from notifications import templates
        return templates.DAILY_SUMMARY.format(**stats)

    def format_weekly_report(self, stats: dict):
        from notifications import templates
        wins   = stats.get("winning_trades", 0)
        losses = stats.get("losing_trades", 0)
        total  = wins + losses
        stats["win_rate"]      = (wins / total * 100) if total > 0 else 0.0
        stats["total_trades"]  = total
        return templates.WEEKLY_REPORT.format(**stats)

    def get_signals(self):
        """Fetches the last 5 signals from the DB and calculates SL/TP targets."""
        try:
            query = """
                SELECT s.timestamp, s.pair, s.direction, st.name as strategy, s.validity_window, s.indicator_values 
                FROM signals s
                JOIN strategies st ON s.strategy_id = st.strategy_id
                WHERE s.timestamp >= NOW() - INTERVAL '24 hours'
                ORDER BY s.timestamp DESC LIMIT 5
            """
            rows = self.db.execute_query(query)
            if not rows:
                return "📭 No recent signals found."
            
            if not mt5.initialize():
                return "❌ MT5 Connection Failed (for price data)"

            from notifications import templates
            response = "🛰 <b>Recent Strategy Signals</b>\n"
            for row in rows:
                pair = row[1]
                direction = row[2]
                
                # Fetch price from log or live
                iv = row[5] if row[5] else {}
                entry_price = iv.get("price")
                
                if not entry_price:
                    tick = mt5.symbol_info_tick(pair)
                    entry_price = tick.ask if direction == "BUY" else tick.bid
                
                # Calculate SL/TP Targets (Standard RR 1:1, 1:2, 1:3)
                # Estimate SL at 30 pips if not specified by strategy
                symbol_info = mt5.symbol_info(pair)
                pip_size = 0.01 if symbol_info.digits in [2, 3] else 0.0001
                sl_dist = 30 * pip_size # 30 pips default
                
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

                # Calculate Entry Range (Price +/- 5 pips)
                range_dist = 5 * pip_size
                if "XAUUSD" in pair or "XAGUSD" in pair:
                    range_dist = 15 * pip_size # Wider range for metals
                
                entry_low = entry_price - range_dist
                entry_high = entry_price + range_dist

                data = {
                    "timestamp": row[0].strftime("%H:%M"),
                    "symbol": pair,
                    "direction": "🟢 BUY" if direction == "BUY" else "🔴 SELL",
                    "strategy": row[3],
                    "validity": row[4],
                    "entry_range": f"{round(entry_low, symbol_info.digits)} - {round(entry_high, symbol_info.digits)}",
                    "sl": round(sl, symbol_info.digits),
                    "tp1": round(tp1, symbol_info.digits),
                    "tp2": round(tp2, symbol_info.digits),
                    "tp3": round(tp3, symbol_info.digits),
                    "exit": "RR 3.0 / Reversal"
                }
                response += templates.SIGNAL_ENTRY.format(**data)
            
            mt5.shutdown()
            return response
        except Exception as e:
            return f"❌ Signal fetch error: {e}"

    def get_analysis(self):
        """Fetches market analysis from the Analyzer."""
        try:
            from notifications.analyzer import MarketAnalyzer
            analyzer = MarketAnalyzer()
            return analyzer.get_analysis_summary()
        except Exception as e:
            return f"❌ Analysis error: {e}"

    def get_risk(self):
        """Fetches detailed risk metrics."""
        if not mt5.initialize():
            return "❌ MT5 Connection Failed"
        
        try:
            from datetime import datetime
            info = mt5.account_info()
            equity = info.equity
            balance = info.balance
            margin_level = info.margin_level
            drawdown = round(((balance - equity) / balance * 100), 2) if balance > 0 else 0
            
            # Fetch Daily/Weekly P&L from DB
            today = datetime.now().date()
            pnl_rows = self.db.execute_query("SELECT total_pnl FROM daily_summary WHERE date = %s", (today,))
            daily_pnl = round(float(pnl_rows[0][0]), 2) if pnl_rows else 0.0
            
            from notifications import templates
            data = {
                "equity": equity,
                "currency": info.currency,
                "margin_level": round(margin_level, 1),
                "drawdown": drawdown,
                "daily_pnl": daily_pnl,
                "weekly_pnl": "TBD", # TODO: Implement weekly rollup query
            }
            return templates.RISK_STATUS.format(**data)
        except Exception as e:
            return f"❌ Risk check error: {e}"
        finally:
            mt5.shutdown()

    def get_active(self):
        """Lists all currently open positions."""
        if not mt5.initialize():
            return "❌ MT5 Connection Failed"
            
        try:
            info = self.account.get_info()
            currency = info.get("currency", "USD") if info else "USD"
            
            positions = mt5.positions_get()
            if not positions:
                return "📴 No open positions."
                
            from notifications import templates
            response = "📊 <b>Active Positions</b>\n"
            for pos in positions:
                symbol_info = mt5.symbol_info(pos.symbol)
                
                # Calculate projected targets if SL exists
                tp2 = "N/A"
                tp3 = "N/A"
                if pos.sl > 0:
                    risk = abs(pos.price_open - pos.sl)
                    if pos.type == mt5.POSITION_TYPE_BUY:
                        tp2 = round(pos.price_open + (risk * 2), symbol_info.digits)
                        tp3 = round(pos.price_open + (risk * 3), symbol_info.digits)
                    else:
                        tp2 = round(pos.price_open - (risk * 2), symbol_info.digits)
                        tp3 = round(pos.price_open - (risk * 3), symbol_info.digits)

                data = {
                    "symbol": pos.symbol,
                    "direction": "🔵 BUY" if pos.type == mt5.POSITION_TYPE_BUY else "🔴 SELL",
                    "profit": round(pos.profit, 2),
                    "currency": currency,
                    "volume": pos.volume,
                    "sl": pos.sl if pos.sl > 0 else "None",
                    "tp": pos.tp if pos.tp > 0 else "None",
                    "tp2": tp2,
                    "tp3": tp3,
                    "open_time": datetime.fromtimestamp(pos.time).strftime("%H:%M")
                }
                response += templates.ACTIVE_TRADE_ENTRY.format(**data)
            return response
        except Exception as e:
            return f"❌ Active list error: {e}"
        finally:
            mt5.shutdown()
