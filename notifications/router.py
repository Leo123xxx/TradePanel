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
            "<b>📊 Account & Positions</b>\n"
            "/status — System and account status\n"
            "/balance — Balance, equity, free margin\n"
            "/active — Open positions with TP/SL targets\n"
            "/risk — Drawdown, margin level, daily P&L\n\n"
            "<b>📡 Signals & Analysis</b>\n"
            "/signals — Latest strategy signals (24h)\n"
            "/analysis — Multi-TF market regime summary\n"
            "/mode — Active strategies and trading mode\n\n"
            "<b>🔬 Backtesting</b>\n"
            "/backtest_report — Last overnight backtest summary\n"
            "/best_pairs — Top pairs by win rate\n"
            "/top_strategies — Top 5 strategies by Sharpe\n"
            "/backtest_status — When did last backtest run?\n"
            "/params — Parameter tweak suggestions\n\n"
            "<b>🛠 System</b>\n"
            "/health — System health and last heartbeat\n"
            "/dashboard — Link to web dashboard\n"
            "/help — Show this list"
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
        """
        data must contain: symbol, direction, pnl_usd, pnl_zar, exit_price, reason, duration.
        For backward compat, if pnl_usd/pnl_zar absent but legacy `pnl` present,
        derive pnl_usd from pnl and estimate pnl_zar using config USDZAR rate.
        """
        from notifications import templates
        import yaml, os
        if "pnl_usd" not in data:
            try:
                cfg_path = os.path.join(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))), "config", "config.yaml")
                with open(cfg_path) as f:
                    cfg = yaml.safe_load(f)
                usdzar = float(cfg.get("account", {}).get("backtesting_usdzar_rate", 18.50))
            except Exception:
                usdzar = 18.50
            data["pnl_usd"] = data.get("pnl", 0.0)
            data["pnl_zar"] = data["pnl_usd"] * usdzar
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

    # ── Backtest Commands ──────────────────────────────────────────────────────

    def _load_latest_backtest(self) -> dict | None:
        """Load the most recent overnight backtest JSON report."""
        import json
        from pathlib import Path
        out_dir = Path(__file__).parent.parent / "results" / "overnight"
        if not out_dir.exists():
            return None
        reports = sorted(out_dir.glob("*_backtest_report.json"))
        if not reports:
            return None
        with open(reports[-1]) as f:
            return json.load(f)

    def get_backtest_report(self) -> str:
        """Return a Telegram-formatted summary of the last overnight backtest."""
        try:
            data = self._load_latest_backtest()
            if not data:
                return ("📭 <b>No backtest report found.</b>\n"
                        "Run: <code>python scripts/run_overnight_backtest.py</code>\n"
                        "Or wait for the 02:00 UTC scheduled run.")
            results = data.get("results", [])
            generated = data.get("generated", "unknown")[:16]
            passed  = [r for r in results if r.get("status") == "PASS"]
            reviews = [r for r in results if r.get("status") == "REVIEW"]
            errors  = [r for r in results if r.get("status") in ("ERROR","SKIP","NO_TRADES")]
            top5 = sorted([r for r in results if r.get("win_rate")],
                          key=lambda x: -x.get("win_rate", 0))[:5]
            msg = (f"📊 <b>Last Overnight Backtest</b>\n"
                   f"🕒 {generated}\n"
                   f"━━━━━━━━━━━━━━━\n"
                   f"✅ Pass: <b>{len(passed)}</b>  "
                   f"⚠️ Review: <b>{len(reviews)}</b>  "
                   f"❌ Skip: <b>{len(errors)}</b>\n\n"
                   f"🏆 <b>Top Performers:</b>\n")
            for r in top5:
                msg += (f"  • <b>{r['strategy']}</b> {r['pair']} {r['timeframe']}\n"
                        f"    WR={r['win_rate']:.1f}% | Sharpe={r.get('sharpe_ratio',0):.2f}\n")
            return msg
        except Exception as e:
            return f"❌ Error loading backtest report: {e}"

    def get_best_pairs(self) -> str:
        """Top pairs ranked by average win rate across all strategies."""
        try:
            data = self._load_latest_backtest()
            if not data:
                return "📭 No backtest data. Run overnight backtest first."
            from collections import defaultdict
            results = [r for r in data.get("results", []) if r.get("win_rate")]
            pair_stats: dict = defaultdict(list)
            for r in results:
                pair_stats[r["pair"]].append(r["win_rate"])
            ranked = sorted(
                [(pair, sum(wrs)/len(wrs), len(wrs)) for pair, wrs in pair_stats.items()],
                key=lambda x: -x[1]
            )
            msg = "📈 <b>Best Pairs by Win Rate</b>\n━━━━━━━━━━━━━━━\n"
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
            for i, (pair, avg_wr, n) in enumerate(ranked):
                icon = medals[i] if i < len(medals) else "  "
                msg += f"{icon} <b>{pair}</b>  {avg_wr:.1f}% avg WR  ({n} combos)\n"
            return msg
        except Exception as e:
            return f"❌ Error: {e}"

    def get_top_strategies(self) -> str:
        """Top 5 strategies by Sharpe ratio from last backtest."""
        try:
            data = self._load_latest_backtest()
            if not data:
                return "📭 No backtest data."
            results = [r for r in data.get("results", []) if r.get("sharpe_ratio") is not None]
            top5 = sorted(results, key=lambda x: -x.get("sharpe_ratio", 0))[:5]
            msg = "🏅 <b>Top 5 Strategies by Sharpe</b>\n━━━━━━━━━━━━━━━\n"
            for i, r in enumerate(top5, 1):
                status_icon = "✅" if r.get("status") == "PASS" else "⚠️"
                msg += (f"{i}. {status_icon} <b>{r['strategy']}</b> {r['pair']} {r['timeframe']}\n"
                        f"   Sharpe={r['sharpe_ratio']:.2f} | WR={r['win_rate']:.1f}% "
                        f"| DD={r.get('max_drawdown_pct', 0):.1f}% | T{r['tier']}\n")
            return msg
        except Exception as e:
            return f"❌ Error: {e}"

    def get_backtest_status(self) -> str:
        """Report when last backtest ran and pass/fail counts."""
        try:
            from pathlib import Path
            out_dir = Path(__file__).parent.parent / "results" / "overnight"
            if not out_dir.exists() or not list(out_dir.glob("*.json")):
                return ("⏳ <b>No overnight backtest has run yet.</b>\n"
                        "Next scheduled run: <b>02:00 UTC</b> (Mon–Fri)\n"
                        "Or trigger manually: <code>python scripts/run_overnight_backtest.py</code>")
            data = self._load_latest_backtest()
            generated = data.get("generated", "unknown")
            results = data.get("results", [])
            passed = sum(1 for r in results if r.get("status") == "PASS")
            reviews = sum(1 for r in results if r.get("status") == "REVIEW")
            errors = sum(1 for r in results if r.get("status") in ("ERROR","SKIP","NO_TRADES"))
            return (f"⏱ <b>Backtest Status</b>\n"
                    f"Last run: <b>{generated[:16]}</b>\n"
                    f"Results: ✅{passed} ⚠️{reviews} ❌{errors} / {len(results)} total\n"
                    f"Next run: <b>02:00 UTC</b> (weekdays)\n"
                    f"Use /backtest_report for full details.")
        except Exception as e:
            return f"❌ Error: {e}"

    def get_strategy_params(self) -> str:
        """Show parameter tweak suggestions from last backtest."""
        try:
            data = self._load_latest_backtest()
            if not data:
                return "📭 No backtest data."
            results = data.get("results", [])
            # Only show strategies that need attention
            needs_tweaks = [
                r for r in results
                if r.get("parameter_tweaks") and r.get("status") in ("REVIEW", "PASS")
            ]
            if not needs_tweaks:
                return ("✅ <b>No parameter tweaks suggested.</b>\n"
                        "All strategies are performing within acceptable thresholds.\n"
                        "Run /backtest_report for full details.")
            msg = "🔧 <b>Parameter Tweak Suggestions</b>\n━━━━━━━━━━━━━━━\n"
            for r in needs_tweaks[:8]:   # cap at 8 to avoid Telegram message limit
                tweaks = r.get("parameter_tweaks", [])
                msg += (f"\n<b>{r['strategy']}</b> {r['pair']} {r['timeframe']} "
                        f"(WR={r.get('win_rate', 0):.1f}%)\n")
                for tweak in tweaks:
                    msg += f"  • {tweak}\n"
            return msg
        except Exception as e:
            return f"❌ Error: {e}"
