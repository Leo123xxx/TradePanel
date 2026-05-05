import MetaTrader5 as mt5
from data.db_client import DBClient
from datetime import datetime, timedelta
from mt5_bridge.account import MT5Account
import os
import yaml
import html
import pytz
from pathlib import Path
from utils.pip_sizes import get_pip_size

SAST = pytz.timezone('Africa/Johannesburg')

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
            "/signal_performance — Accuracy of last 7 days\n"
            "/analysis — Multi-TF market regime summary\n"
            "/mode — Active strategies and trading mode\n\n"
            "<b>🔬 Backtesting</b>\n"
            "/backtest_report — Last overnight backtest summary\n"
            "/best_pairs — Top pairs by win rate\n"
            "/top_strategies — Top 5 strategies by Sharpe\n"
            "/backtest_status — When did last backtest run?\n"
            "/params — Parameter tweak suggestions\n\n"
            "<b>⚙️ Strategy Control</b>\n"
            "/enable &lt;name&gt; — enable a strategy\n"
            "/disable &lt;name&gt; — disable a strategy\n"
            "/pause [min] — Pause bot for N minutes\n"
            "/resume — Resume trading\n"
            "/news_blackout [min] — Block trades during news\n\n"
            "<b>🖊️ Manual Trading</b>\n"
            "/trade &lt;sym&gt; &lt;BUY/SELL&gt; &lt;lots&gt; — Log manual entry\n"
            "/close_manual &lt;ticket&gt; — Log manual exit\n\n"
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
                
                for s_name, s_def in strat_cfg.items():
                    if not isinstance(s_def, dict) or not s_def.get("enabled", False):
                        continue
                    p_list  = ", ".join(s_def.get("pairs", ["N/A"]))
                    tf_list = ", ".join(s_def.get("timeframes", ["N/A"]))
                    name    = s_def.get("name", s_name)
                    tier    = s_def.get("tier", "")
                    enabled.append(f"  • <b>{name}</b> [{tier}]\n    └ {p_list} ({tf_list})")
            
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
            
            # Check for circuit breaker or manual pause
            pause_rows = self.db.execute_query(
                "SELECT event_type, status, message, meta_data FROM bot_health "
                "WHERE event_type IN ('CIRCUIT_BREAKER', 'MANUAL_PAUSE') "
                "AND status = 'PAUSED' "
                "ORDER BY timestamp DESC"
            )
            
            pause_status = ""
            if pause_rows:
                p_type = pause_rows[0][0]
                p_msg = pause_rows[0][2]
                icon = "🔴" if p_type == 'CIRCUIT_BREAKER' else "⏸"
                pause_status = f"\n{icon} <b>BOT PAUSED:</b> {p_msg}"

            if hb_rows:
                last_hb = hb_rows[0][0]
                last_hb_sast = last_hb.replace(tzinfo=pytz.utc).astimezone(SAST)
                if datetime.now() - last_hb < timedelta(minutes=5):
                    bot_status = "🟢 Bot Status: ACTIVE" if not pause_status else "⏸ Bot Status: PAUSED"
                else:
                    bot_status = f"🔴 Bot Status: INACTIVE (Last HB: {last_hb_sast.strftime('%H:%M:%S SAST')})"
            else:
                bot_status = "🟠 Bot Status: NO DATA"
            
            if pause_status:
                bot_status += pause_status
                
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
        """Fetches the last 5 DISTINCT signals from the DB and calculates SL/TP targets."""
        try:
            # DISTINCT ON (strategy_id, pair, direction): keeps only the most recent
            # log entry per strategy+pair+direction combination, so a continuous signal
            # active across multiple 1-minute scan cycles only shows up once.
            query = """
                SELECT DISTINCT ON (s.strategy_id, s.pair, s.direction)
                    s.timestamp, s.pair, s.direction, st.name as strategy, s.validity_window, s.indicator_values
                FROM signals s
                JOIN strategies st ON s.strategy_id = st.strategy_id
                WHERE s.timestamp >= NOW() - INTERVAL '24 hours'
                ORDER BY s.strategy_id, s.pair, s.direction, s.timestamp DESC
                LIMIT 5
            """
            rows = self.db.execute_query(query)
            if not rows:
                return "📭 No recent signals found."
            
            if not mt5.initialize():
                return "❌ MT5 Connection Failed (for price data)"

            from notifications import templates
            
            # Group signals by date for cleaner display
            signals_by_date = {}
            
            for row in rows:
                pair = row[1]
                direction = row[2]
                
                # Fetch price from log or live
                iv = row[5] if row[5] else {}
                entry_price = iv.get("price")
                
                if not entry_price:
                    tick = mt5.symbol_info_tick(pair)
                    entry_price = tick.ask if direction == "BUY" else tick.bid
                
                # Calculate SL/TP Targets
                symbol_info = mt5.symbol_info(pair)
                pip_size = get_pip_size(pair)
                
                atr_val = iv.get("atr")
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

                range_dist = 5 * pip_size
                if "XAUUSD" in pair or "XAGUSD" in pair:
                    range_dist = 15 * pip_size
                
                entry_low = entry_price - range_dist
                entry_high = entry_price + range_dist

                ts_sast = row[0].replace(tzinfo=pytz.utc).astimezone(SAST)
                date_key = ts_sast.strftime("%b %d, %Y").upper()
                
                data = {
                    "timestamp": ts_sast.strftime("%H:%M SAST"),
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
                
                if date_key not in signals_by_date:
                    signals_by_date[date_key] = []
                signals_by_date[date_key].append(templates.SIGNAL_ENTRY.format(**data))

            # Build final response grouped by date
            final_response = "🛰 <b>Recent Strategy Signals</b>\n"
            for d_key in sorted(signals_by_date.keys(), reverse=True):
                final_response += f"\n📅 <b>{d_key}</b>\n"
                for entry in signals_by_date[d_key]:
                    final_response += entry
            
            mt5.shutdown()
            return final_response
        except Exception as e:
            return f"❌ Signal fetch error: {e}"

    def get_signal_performance(self):
        """Displays signal accuracy over the last 7 days."""
        try:
            query = """
                SELECT st.name,
                       COUNT(*) as total,
                       SUM(CASE WHEN so.outcome IN ('TP1', 'TP2', 'TP3') THEN 1 ELSE 0 END) as wins,
                       AVG(so.pnl_pips) as avg_pips
                FROM signal_outcomes so
                JOIN signals s ON so.signal_id = s.signal_id
                JOIN strategies st ON s.strategy_id = st.strategy_id
                WHERE so.checked_at >= NOW() - INTERVAL '7 days'
                GROUP BY st.name
                ORDER BY wins DESC
            """
            rows = self.db.execute_query(query)
            if not rows:
                return "📭 No signal performance data available yet."
                
            response = "📊 <b>Signal Performance (7d)</b>\n━━━━━━━━━━━━━━━\n"
            for name, total, wins, avg_pips in rows:
                wr = (wins / total * 100) if total > 0 else 0
                icon = "🟢" if wr >= 60 else ("🟡" if wr >= 40 else "🔴")
                response += (f"{icon} <b>{name}</b>\n"
                             f"   WR: {wr:.1f}% ({wins}/{total}) | Avg: {avg_pips:+.1f} pips\n")
            
            response += "\n<i>Targets: TP1 (1:1), TP2 (1:2), TP3 (1:3)</i>"
            return response
        except Exception as e:
            return f"❌ Performance fetch error: {e}"

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
                    "open_time": datetime.fromtimestamp(pos.time, tz=pytz.utc).astimezone(SAST).strftime("%H:%M SAST")
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
                strat_name = html.escape(r['strategy'])
                pair = html.escape(r['pair'])
                tf = html.escape(r['timeframe'])
                wr = r.get('win_rate', 0)
                
                msg += f"\n<b>{strat_name}</b> {pair} {tf} (WR={wr:.1f}%)\n"
                for tweak in tweaks:
                    msg += f"  • {html.escape(tweak)}\n"
            return msg
        except Exception as e:
            return f"❌ Error: {e}"

    # ── New Commands ────────────────────────────────────────────────────────

    def get_wfo_summary(self) -> str:
        """Return the latest WFO master summary table."""
        try:
            from pathlib import Path
            wfo_path = Path(__file__).parent.parent / "results" / "wfo_master_summary.md"
            if not wfo_path.exists():
                return ("📭 <b>No WFO results yet.</b>\n"
                        "Run <code>RUN_WFO_AND_UPDATE.bat</code> to generate.")
            content = wfo_path.read_text(encoding="utf-8")
            # Extract generated date
            import re
            m = re.search(r"\*\*Generated:\*\* (.+?)  ", content)
            gen = m.group(1).strip() if m else "unknown"
            # Count pass/fail/error
            passes = content.count("| PASS |")
            fails  = content.count("| FAIL |")
            errors = content.count("| ERROR |")
            # Extract failing strategies for quick view
            fail_lines = []
            for line in content.splitlines():
                if "| FAIL |" in line or "| ERROR |" in line:
                    parts = [p.strip() for p in line.strip("|").split("|")]
                    if len(parts) >= 6:
                        s_name = html.escape(parts[0])
                        p_name = html.escape(parts[1])
                        tf_name = html.escape(parts[2])
                        pr_val = html.escape(parts[3])
                        fail_lines.append(f"  ❌ {s_name} {p_name} {tf_name} ({pr_val})")
            msg = (f"📊 <b>WFO Master Summary</b>\n"
                   f"🕒 {gen}\n"
                   f"━━━━━━━━━━━━━━━\n"
                   f"✅ Pass: <b>{passes}</b>  ❌ Fail: <b>{fails}</b>  ⚠️ Error: <b>{errors}</b>\n")
            if fail_lines:
                msg += "\n<b>Failing combos:</b>\n" + "\n".join(fail_lines[:10])
            msg += "\n\n<i>Run /backtest_report for real-data results.</i>"
            return msg
        except Exception as e:
            return f"❌ WFO summary error: {e}"

    def get_demotion(self) -> str:
        """Return current demotion tracker status."""
        try:
            import json
            from pathlib import Path
            path = Path(__file__).parent.parent / "results" / "demotion_tracker.json"
            if not path.exists():
                return "✅ <b>Demotion Tracker</b>\nNo demotion events recorded."

            raw = path.read_text(encoding="utf-8")
            try:
                tracker = json.loads(raw)
            except json.JSONDecodeError:
                # Auto-repair truncated JSON (e.g. interrupted write)
                last_brace = raw.rfind('},')
                if last_brace > 0:
                    repaired = raw[:last_brace + 1] + '\n}'
                    tracker = json.loads(repaired)
                    # Save the repaired file
                    path.write_text(json.dumps(tracker, indent=2), encoding="utf-8")
                else:
                    return "❌ <b>Demotion Tracker</b>\nFile is corrupted and could not be auto-repaired."

            if not tracker:
                return "✅ <b>Demotion Tracker</b>\nAll strategies performing normally."

            # Split into at-risk (fails >= 1) and healthy (fails == 0)
            at_risk = {k: v for k, v in tracker.items() if v.get("consecutive_fails", 0) >= 1}
            healthy_count = len(tracker) - len(at_risk)

            if not at_risk:
                return (f"✅ <b>Demotion Tracker</b>\n"
                        f"All {len(tracker)} strategies performing normally.\n"
                        f"<i>Auto-demotion triggers at 5 consecutive fails.</i>")

            msg = "⚠️ <b>Demotion Tracker</b>\n━━━━━━━━━━━━━━━\n"
            for strat, info in sorted(at_risk.items(), key=lambda x: -x[1].get("consecutive_fails", 0)):
                consec = info.get("consecutive_fails", 0)
                last_wr = info.get("last_wr")
                wr_str  = f"{last_wr:.1f}%" if isinstance(last_wr, (int, float)) else "N/A"
                icon = "🔴" if consec >= 5 else ("🟡" if consec >= 3 else "🟢")
                msg += f"{icon} <b>{strat}</b>: {consec} fails | WR {wr_str}\n"
            msg += f"\n✅ {healthy_count} strategies healthy (0 fails)"
            msg += "\n<i>Auto-demotion triggers at 5 consecutive fails.</i>"
            return msg
        except Exception as e:
            return f"❌ Demotion tracker error: {e}"

    def get_data_coverage(self) -> str:
        """Show latest bar date per pair for key timeframes."""
        try:
            rows = self.db.execute_query(
                "SELECT pair, timeframe, MAX(timestamp), COUNT(*) "
                "FROM market_data "
                "WHERE timeframe IN ('M1','H1','H4','D1') "
                "GROUP BY pair, timeframe ORDER BY pair, timeframe"
            )
            if not rows:
                return "📭 No market data in DB."
            from collections import defaultdict
            from datetime import datetime, timedelta
            by_pair = defaultdict(dict)
            for pair, tf, latest, count in rows:
                by_pair[pair][tf] = latest
            now    = datetime.now()
            cutoff = now - timedelta(hours=4)
            msg = "📡 <b>Data Coverage</b>\n━━━━━━━━━━━━━━━\n"
            for pair in ["XAUUSD","EURUSD","GBPUSD","USDJPY","XAGUSD","BTCUSD","ETHUSD"]:
                tfs = by_pair.get(pair, {})
                if not tfs:
                    continue
                m1 = tfs.get("M1")
                d1 = tfs.get("D1")
                stale = m1 and m1 < cutoff
                icon  = "🔴" if stale else "🟢"
                m1_sast = m1.replace(tzinfo=pytz.utc).astimezone(SAST) if m1 else None
                m1_str = m1_sast.strftime("%m-%d %H:%M") if m1_sast else "-"
                d1_sast = d1.replace(tzinfo=pytz.utc).astimezone(SAST) if d1 else None
                d1_str = d1_sast.strftime("%Y-%m-%d") if d1_sast else "-"
                msg += f"{icon} <b>{pair}</b>  M1: {m1_str}  D1: {d1_str}\n"
            msg += "\n<i>🔴 = M1 data not updated in last 4 hours.</i>"
            return msg
        except Exception as e:
            return f"❌ Data coverage error: {e}"

    def toggle_strategy(self, strategy_name: str, enable: bool) -> str:
        """Enable or disable a strategy in config/strategies.yaml."""
        try:
            import yaml, re
            from pathlib import Path
            cfg_path = Path(__file__).parent.parent / "config" / "strategies.yaml"
            content  = cfg_path.read_text(encoding="utf-8")

            # Check strategy exists
            if f"\n{strategy_name}:" not in content:
                return (f"❌ Strategy <code>{strategy_name}</code> not found in strategies.yaml.\n"
                        "Use /mode to see valid strategy names.")

            action = "true" if enable else "false"
            old_val = "false" if enable else "true"

            # Replace enabled: <old> → enabled: <new> within the strategy block
            # Find block start
            block_start = content.index(f"\n{strategy_name}:")
            block_end   = len(content)
            # Find next top-level key
            next_key = re.search(r"\n[a-zA-Z_][a-zA-Z0-9_]*:", content[block_start+1:])
            if next_key:
                block_end = block_start + 1 + next_key.start()

            block = content[block_start:block_end]
            if f"enabled: {old_val}" not in block:
                current = "enabled" if enable else "disabled"
                return f"ℹ️ <b>{strategy_name}</b> is already {current}."

            new_block = block.replace(f"enabled: {old_val}", f"enabled: {action}", 1)
            new_content = content[:block_start] + new_block + content[block_end:]
            cfg_path.write_text(new_content, encoding="utf-8")
            verb = "✅ Enabled" if enable else "⛔ Disabled"
            return f"{verb} <b>{strategy_name}</b>\nChange takes effect on next strategy cycle."
        except Exception as e:
            return f"❌ Toggle error: {e}"

    def pause_bot(self, minutes: int = None) -> str:
        """Pauses new trade entry."""
        import json
        try:
            message = "Manual pause via Telegram"
            meta = {}
            if minutes:
                resume_at = datetime.now() + timedelta(minutes=minutes)
                meta['resume_at'] = resume_at.isoformat()
                message += f" for {minutes} min"
            
            self.db.execute_query(
                "INSERT INTO bot_health (event_type, status, message, meta_data, timestamp) "
                "VALUES ('MANUAL_PAUSE', 'PAUSED', %s, %s, %s) "
                "ON CONFLICT (event_type) DO UPDATE SET status='PAUSED', message=EXCLUDED.message, "
                "meta_data=EXCLUDED.meta_data, timestamp=EXCLUDED.timestamp",
                (message, json.dumps(meta), datetime.now())
            )
            
            resp = "⏸ <b>Bot paused.</b> New entries blocked."
            if minutes:
                resp += f"\nAuto-resumes at {resume_at.strftime('%H:%M')} SAST."
            else:
                resp += "\nRun /resume to re-enable."
            return resp
        except Exception as e:
            return f"❌ Pause error: {e}"

    def resume_bot(self) -> str:
        """Clears pause and circuit breaker."""
        try:
            self.db.execute_query(
                "UPDATE bot_health SET status='ACTIVE' WHERE event_type IN ('MANUAL_PAUSE', 'CIRCUIT_BREAKER')"
            )
            return "▶️ <b>Bot resumed.</b> Trading re-enabled."
        except Exception as e:
            return f"❌ Resume error: {e}"

    def get_morning_brief(self) -> str:
        """08:00 morning push — account status + last backtest summary."""
        try:
            import MetaTrader5 as mt5
            lines = ["🌅 <b>Morning Brief</b>\n━━━━━━━━━━━━━━━"]
            # Account
            if mt5.initialize():
                info = mt5.account_info()
                if info:
                    lines.append(f"💰 Balance: {info.balance:.2f} {info.currency}")
                    lines.append(f"📈 Equity:  {info.equity:.2f} {info.currency}")
                    dd = round((info.balance - info.equity) / info.balance * 100, 2) if info.balance else 0
                    lines.append(f"📉 DrawDown: {dd:.1f}%")
                positions = mt5.positions_get() or []
                lines.append(f"📊 Open positions: {len(positions)}")
                mt5.shutdown()
            # Last backtest
            lines.append("\n" + self.get_backtest_status())
            return "\n".join(lines)
        except Exception as e:
            return f"❌ Morning brief error: {e}"

    def set_news_blackout(self, minutes):
        """Sets a news blackout period in the bot_health table."""
        try:
            resume_at = datetime.now() + timedelta(minutes=minutes)
            resume_at_str = resume_at.isoformat()
            
            # Upsert into bot_health
            query = """
                INSERT INTO bot_health (event_type, status, timestamp, message)
                VALUES ('NEWS_BLACKOUT', 'PAUSED', %s, %s)
                ON CONFLICT (event_type) 
                DO UPDATE SET status = 'PAUSED', timestamp = %s, message = %s
            """
            self.db.execute_query(query, (datetime.now(), resume_at_str, datetime.now(), resume_at_str))
            
            return True, f"News blackout active until {resume_at.strftime('%H:%M')} SAST."
        except Exception as e:
            return False, f"Database error: {e}"

    def log_manual_trade(self, symbol, direction, lots, entry=None):
        """Logs a manual trade entry into the database."""
        try:
            import uuid
            trade_id = str(uuid.uuid4())
            
            # 1. Validate symbol and get current price if entry is None
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return False, f"Symbol {symbol} not found in MT5."
            
            if entry is None:
                entry = symbol_info.ask if direction == "BUY" else symbol_info.bid
                
            # 2. Log to DB
            query = """
                INSERT INTO trades 
                (trade_id, mode, account_id, pair, direction, lot_size, entry_price, open_time, status, magic) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Using account_id=1 (Demo) and magic=0 for manual
            self.db.execute_query(query, (
                trade_id, 'MANUAL', 1, symbol, direction, lots, entry, datetime.now(), 'OPENED', 0
            ))
            
            return True, f"Manual trade logged: {symbol} {direction} {lots} lots @ {entry:.5f}"
        except Exception as e:
            return False, f"Error logging manual trade: {e}"

    def close_manual_trade(self, ticket, exit_price=None):
        """Logs a manual trade exit/closure."""
        try:
            # 1. Find the trade in DB
            rows = self.db.execute_query(
                "SELECT trade_id, pair, direction, entry_price, open_time FROM trades WHERE mt5_ticket = %s OR (pair IS NOT NULL AND status='OPENED' AND mode='MANUAL' AND trade_id::text LIKE %s)",
                (ticket, f"%{ticket}%") # Allow partial ticket/id matching for convenience
            )
            
            if not rows:
                return False, f"Manual trade with ticket/ID matching '{ticket}' not found or already closed."
            
            trade_id, symbol, direction, entry_price, open_time = rows[0]
            
            # 2. Get exit price if None
            if exit_price is None:
                symbol_info = mt5.symbol_info(symbol)
                if symbol_info:
                    exit_price = symbol_info.bid if direction == "BUY" else symbol_info.ask
                else:
                    return False, "Symbol not found in MT5, please provide exit_price."

            # 3. Calculate P&L (approximate)
            pnl = (exit_price - entry_price) if direction == "BUY" else (entry_price - exit_price)
            
            # 4. Update DB
            query = """
                UPDATE trades 
                SET exit_price = %s, close_time = %s, status = %s, close_reason = %s
                WHERE trade_id = %s
            """
            self.db.execute_query(query, (
                exit_price, datetime.now(), 'CLOSED', 'MANUAL', trade_id
            ))
            
            return True, f"Manual trade closed: {symbol} @ {exit_price:.5f}. (Entry: {entry_price:.5f})"
        except Exception as e:
            return False, f"Error closing manual trade: {e}"
