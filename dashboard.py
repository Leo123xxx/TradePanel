#!/usr/bin/env python3
"""
dashboard.py — TradePanel Web Dashboard and Monitoring

Real-time web dashboard for monitoring trading performance, system health, and portfolio metrics.
Provides both web UI and REST API endpoints for integration.

USAGE:
    python dashboard.py --port 5000              # Start web UI (default)
    python dashboard.py --port 5000 --host 0.0.0.0  # Listen on all interfaces
    python dashboard.py --mode metrics           # API only (no web UI)
    python dashboard.py --mode live              # Console monitoring

For help:
    python dashboard.py --help
"""

import os
import sys
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError:
    print("❌ FastAPI not installed. Install with: pip install fastapi uvicorn")
    sys.exit(1)

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv()

# Configure logging
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(LOGS_DIR / "dashboard.log", maxBytes=10*1024*1024, backupCount=5)
    ]
)
logger = logging.getLogger(__name__)


class DashboardMetrics:
    """Collect and aggregate dashboard metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.project_root = PROJECT_ROOT
        self.results_dir = self.project_root / "results"
        self.logs_dir = self.project_root / "logs"

    def get_portfolio_metrics(self) -> Dict[str, Any]:
        """Get portfolio performance metrics."""
        try:
            from data.db_client import DBClient
            db = DBClient()

            # Get latest dashboard data
            dashboard_file = self._get_latest_dashboard_file()
            if dashboard_file and dashboard_file.exists():
                with open(dashboard_file, 'r') as f:
                    data = json.load(f)
                    val_summary = data.get("validation_summary", {})
                    pass_rate_str = val_summary.get("pass_rate", "0%").replace("%", "")
                    try:
                        pass_rate = float(pass_rate_str) / 100.0
                    except:
                        pass_rate = 0.0

                    return {
                        "status": "active",
                        "strategy_count": val_summary.get("total_strategies", 0),
                        "test_pass_rate": pass_rate,
                        "overall_status": "OK" if pass_rate > 0.5 else "WARNING",
                        "total_p_l": 0, # Not in current JSON
                        "timestamp": data.get("last_update", datetime.now().isoformat()),
                        "logs": self.get_log_summary()
                    }
            return {"status": "no_data", "strategy_count": 0, "test_pass_rate": 0, "logs": self.get_log_summary()}
        except Exception as e:
            logger.warning(f"Could not get portfolio metrics: {e}")
            return {"status": "error", "error": str(e)}

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        health = {
            "database": "OK",
            "mt5": "OK",
            "telegram": "OK",
            "alerts_24h": 0,
            "last_check": datetime.now().isoformat()
        }

        try:
            from data.db_client import DBClient
            db = DBClient()
            db.execute_query("SELECT 1")
        except Exception as e:
            health["database"] = "ERROR"
            logger.warning(f"Database health check failed: {e}")

        try:
            from mt5_bridge.connector import MT5Connector
            connector = MT5Connector()
            health["mt5"] = "CONNECTED" if connector.connected else "DISCONNECTED"
        except Exception as e:
            health["mt5"] = "ERROR"
            logger.warning(f"MT5 health check failed: {e}")

        return health

    def get_trading_summary(self) -> Dict[str, Any]:
        """Get trading summary metrics."""
        try:
            dashboard_file = self._get_latest_dashboard_file()
            if dashboard_file and dashboard_file.exists():
                with open(dashboard_file, 'r') as f:
                    data = json.load(f)
                    val_summary = data.get("validation_summary", {})
                    perf_matrix = data.get("charts", {}).get("performance_matrix", [])
                    
                    pass_rate_str = val_summary.get("pass_rate", "0%").replace("%", "")
                    try:
                        win_rate = float(pass_rate_str) / 100.0
                    except:
                        win_rate = 0.0

                    return {
                        "today_trades": val_summary.get("total_tests", 0),
                        "win_rate": win_rate,
                        "pnl_today": 0,
                        "drawdown": 0,
                        "active_strategies": val_summary.get("total_strategies", 0)
                    }
            return {"today_trades": 0, "win_rate": 0, "pnl_today": 0, "drawdown": 0, "active_strategies": 0}
        except Exception as e:
            logger.warning(f"Could not get trading summary: {e}")
            return {"error": str(e)}

    def get_strategies(self) -> Dict[str, Any]:
        """Get top performing strategies."""
        try:
            dashboard_file = self._get_latest_dashboard_file()
            if dashboard_file and dashboard_file.exists():
                with open(dashboard_file, 'r') as f:
                    data = json.load(f)
                    strategies = data.get("charts", {}).get("performance_matrix", [])
                    # Sort by win rate
                    strategies = sorted(strategies, key=lambda x: x.get("win_rate", 0), reverse=True)
                    # Filter for unique strategy names (take best pair)
                    unique_strats = {}
                    for s in strategies:
                        name = s.get("strategy")
                        if name not in unique_strats:
                            unique_strats[name] = {
                                "name": name,
                                "pair": s.get("pair"),
                                "win_rate": s.get("win_rate", 0) / 100.0,
                                "trades": s.get("trades", 0), # Not in current JSON, will be 0
                                "avg_pnl": 0 # Not in current JSON
                            }
                    return {"strategies": list(unique_strats.values())[:10]}  # Top 10
            return {"strategies": []}
        except Exception as e:
            logger.warning(f"Could not get strategies: {e}")
            return {"error": str(e)}

    def get_live_trades(self) -> list[Dict[str, Any]]:
        """Fetch active trades from DB."""
        try:
            from data.db_client import DBClient
            db = DBClient()
            rows = db.execute_query(
                "SELECT pair, direction, lot_size, entry_price, open_time, mode, mt5_ticket FROM trades WHERE status = 'OPENED' ORDER BY open_time DESC"
            )
            trades = []
            for r in rows:
                trades.append({
                    "pair": r[0],
                    "direction": r[1],
                    "lots": float(r[2]),
                    "entry": float(r[3]),
                    "time": r[4].strftime("%H:%M:%S") if r[4] else "N/A",
                    "mode": r[5],
                    "ticket": r[6]
                })
            return trades
        except Exception as e:
            logger.warning(f"Could not get live trades: {e}")
            return []

    def get_manual_history(self) -> list[Dict[str, Any]]:
        """Fetch manual trade history."""
        try:
            from data.db_client import DBClient
            db = DBClient()
            rows = db.execute_query(
                "SELECT pair, direction, lot_size, entry_price, exit_price, close_time, status FROM trades WHERE mode = 'MANUAL' ORDER BY close_time DESC LIMIT 20"
            )
            history = []
            for r in rows:
                pnl = 0
                if r[4] and r[3]:
                    pnl = (r[4] - r[3]) if r[1] == 'BUY' else (r[3] - r[4])
                history.append({
                    "pair": r[0],
                    "direction": r[1],
                    "lots": float(r[2]),
                    "entry": float(r[3]),
                    "exit": float(r[4]) if r[4] else 0,
                    "time": r[5].strftime("%m-%d %H:%M") if r[5] else "OPEN",
                    "status": r[6],
                    "pnl": pnl
                })
            return history
        except Exception as e:
            logger.warning(f"Could not get manual history: {e}")
            return []

    def get_live_account(self) -> Dict[str, Any]:
        """Live account: daily P&L, open positions (bot vs manual), circuit breaker status."""
        try:
            from data.db_client import DBClient
            db = DBClient()

            # Today's closed trade P&L
            pnl_rows = db.execute_query(
                "SELECT COALESCE(SUM(net_pnl), 0) FROM trades "
                "WHERE status = 'CLOSED' AND DATE(close_time) = CURRENT_DATE"
            )
            daily_pnl = float(pnl_rows[0][0]) if pnl_rows else 0.0

            # Open positions grouped by mode
            pos_rows = db.execute_query(
                "SELECT mode, COUNT(*), COALESCE(SUM(lot_size), 0) "
                "FROM trades WHERE status = 'OPENED' GROUP BY mode"
            )
            bot_count, manual_count = 0, 0
            bot_lots, manual_lots = 0.0, 0.0
            for mode, count, lots in (pos_rows or []):
                if mode in ('PAPER', 'LIVE'):
                    bot_count += count
                    bot_lots += float(lots)
                elif mode == 'MANUAL':
                    manual_count += count
                    manual_lots += float(lots)

            # Circuit breaker / pause status
            cb_rows = db.execute_query(
                "SELECT event_type, message FROM bot_health "
                "WHERE event_type IN ('CIRCUIT_BREAKER','MANUAL_PAUSE') "
                "ORDER BY timestamp DESC LIMIT 1"
            )
            circuit_breaker_active = bool(cb_rows)
            cb_message = f"{cb_rows[0][0]}: {cb_rows[0][1]}" if cb_rows else ""

            # Max drawdown last 30 days
            dd_rows = db.execute_query(
                "SELECT COALESCE(MAX(max_drawdown), 0) FROM daily_summary "
                "WHERE date >= CURRENT_DATE - INTERVAL '30 days'"
            )
            max_dd = float(dd_rows[0][0]) if dd_rows else 0.0

            return {
                "daily_pnl": round(daily_pnl, 2),
                "bot_positions": {"count": bot_count, "lots": round(bot_lots, 2)},
                "manual_positions": {"count": manual_count, "lots": round(manual_lots, 2)},
                "circuit_breaker_active": circuit_breaker_active,
                "cb_message": cb_message,
                "max_drawdown_30d": round(max_dd, 2),
                "account_currency": "ZAR",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"Could not get live account: {e}")
            return {
                "daily_pnl": 0, "bot_positions": {"count": 0, "lots": 0},
                "manual_positions": {"count": 0, "lots": 0},
                "circuit_breaker_active": False, "cb_message": "",
                "max_drawdown_30d": 0, "account_currency": "ZAR",
                "error": str(e)
            }

    def get_signal_performance(self) -> Dict[str, Any]:
        """Signal hit rate by strategy, signals per day BUY/SELL, conversion rate."""
        try:
            from data.db_client import DBClient
            db = DBClient()

            # Hit rate by strategy (last 7 days)
            hit_rows = db.execute_query(
                "SELECT COALESCE(st.name,'Unknown'), COUNT(sig.signal_id), "
                "COUNT(sig.triggered_trade_id) "
                "FROM signals sig LEFT JOIN strategies st ON st.strategy_id=sig.strategy_id "
                "WHERE sig.timestamp >= NOW() - INTERVAL '7 days' "
                "GROUP BY st.name ORDER BY 2 DESC LIMIT 15"
            )
            hit_rate = []
            for name, total, converted in (hit_rows or []):
                rate = round(float(converted) / float(total) * 100, 1) if total > 0 else 0.0
                hit_rate.append({"strategy": name, "total": int(total),
                                 "converted": int(converted), "rate": rate})

            # Signals per day BUY/SELL (last 7 days)
            pd_rows = db.execute_query(
                "SELECT DATE(timestamp), direction, COUNT(*) FROM signals "
                "WHERE timestamp >= NOW() - INTERVAL '7 days' "
                "GROUP BY DATE(timestamp), direction ORDER BY 1 ASC"
            )
            per_day = {}
            for day, direction, count in (pd_rows or []):
                ds = str(day)
                per_day.setdefault(ds, {"BUY": 0, "SELL": 0})
                per_day[ds][direction] = int(count)
            signals_per_day = [{"date": k, "buy": v.get("BUY", 0), "sell": v.get("SELL", 0)}
                                for k, v in sorted(per_day.items())]

            # Overall conversion rate
            conv_rows = db.execute_query(
                "SELECT COUNT(*), COUNT(triggered_trade_id) FROM signals "
                "WHERE timestamp >= NOW() - INTERVAL '7 days'"
            )
            total_sigs = int(conv_rows[0][0]) if conv_rows else 0
            total_conv = int(conv_rows[0][1]) if conv_rows else 0

            return {
                "hit_rate_by_strategy": hit_rate,
                "signals_per_day": signals_per_day,
                "conversion_rate": {"converted": total_conv, "not_converted": total_sigs - total_conv}
            }
        except Exception as e:
            logger.warning(f"Could not get signal performance: {e}")
            return {"hit_rate_by_strategy": [], "signals_per_day": [],
                    "conversion_rate": {"converted": 0, "not_converted": 0}}

    def get_risk_metrics(self) -> Dict[str, Any]:
        """Daily drawdown, Kelly fraction per strategy, circuit breaker events."""
        try:
            from data.db_client import DBClient
            db = DBClient()

            # Daily drawdown last 14 days
            dd_rows = db.execute_query(
                "SELECT date, COALESCE(max_drawdown, 0) FROM daily_summary "
                "WHERE date >= CURRENT_DATE - INTERVAL '14 days' ORDER BY date ASC"
            )
            daily_drawdown = [{"date": str(r[0]), "drawdown": round(float(r[1]), 2)}
                               for r in (dd_rows or [])]

            # Kelly fraction per strategy (closed trades, min 5 samples)
            kelly_rows = db.execute_query(
                "SELECT COALESCE(st.name,'Unknown'), COUNT(*), "
                "SUM(CASE WHEN net_pnl>0 THEN 1 ELSE 0 END)::float/NULLIF(COUNT(*),0), "
                "ABS(AVG(CASE WHEN net_pnl>0 THEN net_pnl END))/"
                "NULLIF(ABS(AVG(CASE WHEN net_pnl<0 THEN net_pnl END)),0) "
                "FROM trades t LEFT JOIN strategies st ON st.strategy_id=t.strategy_id "
                "WHERE t.status='CLOSED' GROUP BY st.name HAVING COUNT(*)>=5 "
                "ORDER BY 2 DESC LIMIT 10"
            )
            kelly_list = []
            for strat, trades, wr, payoff in (kelly_rows or []):
                wr = float(wr) if wr else 0.5
                payoff = float(payoff) if payoff else 1.0
                kelly = max(0.0, wr - (1 - wr) / payoff) * 0.25
                kelly_list.append({"strategy": strat, "kelly_pct": round(kelly * 100, 2),
                                    "win_rate": round(wr * 100, 1), "trades": int(trades)})

            # Recent circuit breaker / pause / resume events
            cb_rows = db.execute_query(
                "SELECT event_type, message, timestamp FROM bot_health "
                "WHERE event_type IN ('CIRCUIT_BREAKER','MANUAL_PAUSE','RESUME') "
                "ORDER BY timestamp DESC LIMIT 20"
            )
            cb_events = [{"type": r[0], "message": r[1] or "",
                           "time": r[2].strftime("%m-%d %H:%M") if r[2] else ""}
                          for r in (cb_rows or [])]

            return {"daily_drawdown": daily_drawdown,
                    "kelly_per_strategy": kelly_list,
                    "circuit_breaker_events": cb_events}
        except Exception as e:
            logger.warning(f"Could not get risk metrics: {e}")
            return {"daily_drawdown": [], "kelly_per_strategy": [], "circuit_breaker_events": []}

    def get_trade_journal(self, date_from=None, date_to=None,
                          strategy=None, pair=None, status=None, mode=None) -> Dict[str, Any]:
        """Filterable trade journal from trades table (last 200 matching rows)."""
        try:
            from data.db_client import DBClient
            db = DBClient()

            clauses, params = [], []
            if date_from:
                clauses.append("t.open_time >= %s"); params.append(date_from)
            if date_to:
                clauses.append("t.open_time <= %s"); params.append(date_to + " 23:59:59")
            if strategy:
                clauses.append("st.name ILIKE %s"); params.append(f"%{strategy}%")
            if pair:
                clauses.append("t.pair ILIKE %s"); params.append(f"%{pair}%")
            if status:
                clauses.append("t.status = %s"); params.append(status.upper())
            if mode:
                clauses.append("t.mode = %s"); params.append(mode.upper())
            where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

            rows = db.execute_query(
                f"SELECT t.trade_id, COALESCE(st.name,'Unknown'), t.pair, t.direction, "
                f"t.lot_size, t.entry_price, t.exit_price, t.net_pnl, "
                f"t.open_time, t.close_time, t.status, t.mode, t.close_reason, "
                f"t.sl_price, t.tp_price "
                f"FROM trades t LEFT JOIN strategies st ON st.strategy_id=t.strategy_id "
                f"{where} ORDER BY t.open_time DESC LIMIT 200",
                tuple(params) if params else None
            )
            trades = []
            for r in (rows or []):
                trades.append({
                    "id": str(r[0]), "strategy": r[1], "pair": r[2],
                    "direction": r[3], "lots": float(r[4]) if r[4] else 0.0,
                    "entry": float(r[5]) if r[5] else 0.0,
                    "exit": float(r[6]) if r[6] else 0.0,
                    "net_pnl": round(float(r[7]), 2) if r[7] is not None else 0.0,
                    "open_time": r[8].strftime("%Y-%m-%d %H:%M") if r[8] else "",
                    "close_time": r[9].strftime("%Y-%m-%d %H:%M") if r[9] else "OPEN",
                    "status": r[10], "mode": r[11],
                    "close_reason": r[12] or "",
                    "sl": float(r[13]) if r[13] else 0.0,
                    "tp": float(r[14]) if r[14] else 0.0
                })
            closed = [t for t in trades if t["status"] == "CLOSED"]
            winners = [t for t in closed if t["net_pnl"] > 0]
            return {
                "trades": trades,
                "summary": {
                    "total": len(trades), "closed": len(closed),
                    "open": len(trades) - len(closed),
                    "win_rate": round(len(winners) / len(closed) * 100, 1) if closed else 0.0,
                    "total_pnl": round(sum(t["net_pnl"] for t in closed), 2)
                }
            }
        except Exception as e:
            logger.warning(f"Could not get trade journal: {e}")
            return {"trades": [], "summary": {"total": 0, "closed": 0, "open": 0,
                                               "win_rate": 0, "total_pnl": 0}}

    def _get_latest_dashboard_file(self) -> Path:
        """Get the latest dashboard JSON file."""
        try:
            dashboard_dir = self.results_dir / "daily_validation"
            if dashboard_dir.exists():
                json_files = sorted(dashboard_dir.glob("dashboard_*.json"), reverse=True)
                return json_files[0] if json_files else None
        except Exception as e:
            logger.warning(f"Could not find dashboard file: {e}")
        return None

    def get_log_summary(self, lines: int = 20) -> list[str]:
        """Get the latest log entries."""
        try:
            log_file = Path("logs/main.log")
            if not log_file.exists():
                return ["No log file found."]
            
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                # Efficiently read last N lines
                all_lines = f.readlines()
                last_lines = all_lines[-lines:]
                # Clean up formatting for HTML display
                return [l.strip() for l in last_lines if l.strip()]
        except Exception as e:
            logger.warning(f"Could not read logs: {e}")
            return [f"Error reading logs: {e}"]


class Dashboard:
    """FastAPI dashboard application."""

    def __init__(self):
        """Initialize dashboard."""
        self.app = FastAPI(title="TradePanel Dashboard")
        self.metrics = DashboardMetrics()
        self._setup_routes()

    def _setup_routes(self):
        """Setup API routes."""

        @self.app.get("/", response_class=HTMLResponse)
        async def get_dashboard():
            """Get HTML dashboard."""
            return self._get_html_dashboard()

        @self.app.get("/api/metrics")
        async def get_all_metrics():
            """Get all metrics."""
            return {
                "portfolio": self.metrics.get_portfolio_metrics(),
                "health": self.metrics.get_system_health(),
                "trading": self.metrics.get_trading_summary(),
                "strategies": self.metrics.get_strategies()
            }

        @self.app.get("/api/portfolio")
        async def get_portfolio():
            """Get portfolio metrics."""
            return self.metrics.get_portfolio_metrics()

        @self.app.get("/api/health")
        async def get_health():
            """Get system health."""
            return self.metrics.get_system_health()

        @self.app.get("/api/trading")
        async def get_trading():
            """Get trading summary."""
            return self.metrics.get_trading_summary()

        @self.app.get("/api/strategies")
        async def get_strategies():
            """Get strategies."""
            return self.metrics.get_strategies()

        @self.app.get("/api/live_account")
        async def get_live_account():
            """Live account: daily P&L, positions, circuit breaker status."""
            return self.metrics.get_live_account()

        @self.app.get("/api/signal_performance")
        async def get_signal_performance():
            """Signal hit rate by strategy, signals per day, conversion rate (7-day window)."""
            return self.metrics.get_signal_performance()

        @self.app.get("/api/risk_metrics")
        async def get_risk_metrics():
            """Daily drawdown, Kelly fraction per strategy, circuit breaker events."""
            return self.metrics.get_risk_metrics()

        from fastapi import Query as FQuery

        @self.app.get("/api/trade_journal")
        async def get_trade_journal(
            date_from: str = FQuery(None),
            date_to: str = FQuery(None),
            strategy: str = FQuery(None),
            pair: str = FQuery(None),
            status: str = FQuery(None),
            mode: str = FQuery(None)
        ):
            """Filterable trade journal (last 200 rows). Params: date_from, date_to, strategy, pair, status, mode."""
            return self.metrics.get_trade_journal(date_from, date_to, strategy, pair, status, mode)

        @self.app.get("/docs", response_class=HTMLResponse)
        async def get_docs():
            """Get API documentation."""
            return """
            <html>
            <head><title>TradePanel API Docs</title></head>
            <body style="font-family: Arial; margin: 20px;">
                <h1>TradePanel API Documentation</h1>
                <h2>Endpoints</h2>
                <ul>
                    <li><code>GET /</code> — Dashboard HTML</li>
                    <li><code>GET /api/metrics</code> — All metrics</li>
                    <li><code>GET /api/portfolio</code> — Portfolio metrics</li>
                    <li><code>GET /api/health</code> — System health</li>
                    <li><code>GET /api/trading</code> — Trading summary</li>
                    <li><code>GET /api/strategies</code> — Strategy performance</li>
                </ul>
            </body>
            </html>
            """

        live_trades = self.metrics.get_live_trades()
        manual_history = self.metrics.get_manual_history()

        # Generate Log HTML
        log_html = ""
        for line in portfolio.get("logs", []):
            level = "INFO"
            if "WARNING" in line: level = "WARNING"
            if "ERROR" in line: level = "ERROR"
            log_html += f'<div class="log-entry {level}">{line}</div>'
        if not log_html:
            log_html = '<div class="log-entry">No recent activity.</div>'

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TradePanel | Pro Dashboard</title>
            <style>
                :root {{
                    --primary: #2E75B6;
                    --dark: #1a1a1a;
                    --light: #f5f5f5;
                    --success: #28a745;
                    --danger: #dc3545;
                    --warning: #ffc107;
                }}
                body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; background: var(--light); color: var(--dark); }}
                .navbar {{ background: var(--dark); color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }}
                .container {{ max-width: 1400px; margin: 2rem auto; padding: 0 1rem; }}
                h1, h2 {{ margin-bottom: 1rem; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
                .card {{ background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s; }}
                .card:hover {{ transform: translateY(-2px); }}
                .metric-label {{ color: #666; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
                .metric-value {{ font-size: 2rem; font-weight: 800; color: var(--primary); margin: 0.5rem 0; }}
                .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }}
                .badge-success {{ background: #d4edda; color: #155724; }}
                .badge-danger {{ background: #f8d7da; color: #721c24; }}
                .badge-warning {{ background: #fff3cd; color: #856404; }}
                .badge-info {{ background: #d1ecf1; color: #0c5460; }}
                table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 1rem; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                th {{ background: #fafafa; color: #666; font-weight: 600; font-size: 0.85rem; }}
                tr:last-child td {{ border-bottom: none; }}
                .pnl-pos {{ color: var(--success); font-weight: bold; }}
                .pnl-neg {{ color: var(--danger); font-weight: bold; }}
                .log-panel {{ background: #000; color: #0f0; padding: 1rem; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.8rem; height: 250px; overflow-y: auto; box-shadow: inset 0 0 10px rgba(0,255,0,0.1); }}
                .log-entry {{ margin-bottom: 0.3rem; border-bottom: 1px solid #222; opacity: 0.8; }}
                .log-entry.WARNING {{ color: #ff0; }}
                .log-entry.ERROR {{ color: #f00; }}
                .tabs {{ display: flex; gap: 1rem; margin-bottom: 1rem; border-bottom: 2px solid #ddd; }}
                .tab {{ padding: 0.5rem 1rem; cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; font-weight: bold; color: #666; }}
                .tab.active {{ border-bottom-color: var(--primary); color: var(--primary); }}
            </style>
            <meta http-equiv="refresh" content="15">
        </head>
        <body>
            <div class="navbar">
                <div><strong>TradePanel</strong> | Live Execution Platform</div>
                <div class="badge badge-success">MT5: {health.get('mt5', 'CONNECTED')}</div>
            </div>

            <div class="container">
                <div class="grid">
                    <div class="card">
                        <div class="metric-label">Account Balance</div>
                        <div class="metric-value">ZAR ---</div>
                        <div class="badge badge-info">1% Risk Active</div>
                    </div>
                    <div class="card">
                        <div class="metric-label">Signal Accuracy (7d)</div>
                        <div class="metric-value">{trading.get('win_rate', 0):.1%}</div>
                        <div class="metric-label">{trading.get('today_trades', 0)} samples</div>
                    </div>
                    <div class="card">
                        <div class="metric-label">Daily P&L</div>
                        <div class="metric-value" style="color: {'var(--success)' if trading.get('pnl_today', 0) >= 0 else 'var(--danger)'};">
                            R{trading.get('pnl_today', 0):.2f}
                        </div>
                    </div>
                    <div class="card">
                        <div class="metric-label">System Health</div>
                        <div style="margin-top: 10px;">
                            <span class="badge badge-success">DB: {health.get('database')}</span>
                            <span class="badge badge-warning">TG: {health.get('telegram')}</span>
                        </div>
                    </div>
                </div>

                <div class="grid" style="grid-template-columns: 2fr 1fr;">
                    <div class="card">
                        <h2>🚀 Live Positions (Magic Number Filtered)</h2>
                        <table>
                            <tr>
                                <th>Symbol</th>
                                <th>Dir</th>
                                <th>Lots</th>
                                <th>Entry</th>
                                <th>Time</th>
                                <th>Mode</th>
                                <th>Ticket</th>
                            </tr>
        """

        if not live_trades:
            html += "<tr><td colspan='7' style='text-align:center; padding: 2rem; color: #999;'>No active bot/manual positions.</td></tr>"
        else:
            for t in live_trades:
                icon = "🟢" if t['direction'] == "BUY" else "🔴"
                mode_badge = "badge-info" if t['mode'] == "PAPER" else "badge-warning"
                html += f"""
                            <tr>
                                <td><b>{t['pair']}</b></td>
                                <td>{icon} {t['direction']}</td>
                                <td>{t['lots']:.2f}</td>
                                <td>{t['entry']:.5f}</td>
                                <td>{t['time']}</td>
                                <td><span class="badge {mode_badge}">{t['mode']}</span></td>
                                <td><code>{t['ticket']}</code></td>
                            </tr>
                """

        html += """
                        </table>
                    </div>
                    <div class="card">
                        <h2>📜 System Logs</h2>
                        <div class="log-panel">
                            {log_html}
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h2>🖊️ Manual Trade Journal</h2>
                    <table>
                        <tr>
                            <th>Pair</th>
                            <th>Dir</th>
                            <th>Lots</th>
                            <th>Entry</th>
                            <th>Exit</th>
                            <th>P&L (Pts)</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
        """

        if not manual_history:
            html += "<tr><td colspan='8' style='text-align:center; color: #999;'>No manual trades logged.</td></tr>"
        else:
            for m in manual_history:
                pnl_class = "pnl-pos" if m['pnl'] > 0 else "pnl-neg"
                html += f"""
                        <tr>
                            <td>{m['pair']}</td>
                            <td>{m['direction']}</td>
                            <td>{m['lots']}</td>
                            <td>{m['entry']:.5f}</td>
                            <td>{m['exit']:.5f}</td>
                            <td class="{pnl_class}">{m['pnl']:.1f}</td>
                            <td>{m['time']}</td>
                            <td><span class="badge {'badge-success' if m['status']=='CLOSED' else 'badge-info'}">{m['status']}</span></td>
                        </tr>
                """

        html += """
                    </table>
                </div>

                <div class="card" style="margin-top: 2rem;">
                    <h2>📈 Strategy Performance (Top 10)</h2>
                    <table>
                        <tr>
                            <th>Strategy</th>
                            <th>Best Pair</th>
                            <th>Win Rate</th>
                            <th>Trades</th>
                        </tr>
        """

        for strategy in strategies.get("strategies", [])[:10]:
            html += f"""
                        <tr>
                            <td>{strategy.get('name', 'Unknown')}</td>
                            <td>{strategy.get('pair', 'N/A')}</td>
                            <td>{strategy.get('win_rate', 0):.1%}</td>
                            <td>{strategy.get('trades', 0)}</td>
                        </tr>
            """

        html += """
                    </table>
                </div>
            </div>
            <div style="text-align: center; color: #999; font-size: 0.7rem; padding: 2rem;">
                TradePanel Engine v2.4.0-live | Build 2026.05.03
            </div>
        </body>
        </html>
        """
        return html

    def run(self, host: str = "127.0.0.1", port: int = 5000):
        """Run the dashboard server."""
        logger.info(f"WEB: Starting TradePanel Dashboard on {host}:{port}")
        logger.info(f"WEB: Access at http://{host}:{port}")
        uvicorn.run(self.app, host=host, port=port, log_level="info")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TradePanel Dashboard - Web UI and API monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python dashboard.py --port 5000
  python dashboard.py --port 8080 --host 0.0.0.0
  python dashboard.py --mode metrics
  python dashboard.py --mode live

MODES:
  web       Web UI dashboard (default)
  metrics   API only (no web interface)
  live      Console monitoring
        """
    )

    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to listen on (default: 5000)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to listen on (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="web",
        choices=["web", "metrics", "live"],
        help="Dashboard mode (default: web)"
    )

    args = parser.parse_args()

    # Initialize dashboard
    dashboard = Dashboard()

    try:
        if args.mode == "web":
            logger.info(f"Starting web dashboard...")
            dashboard.run(host=args.host, port=args.port)
        elif args.mode == "metrics":
            logger.info(f"Starting metrics API (no web UI)...")
            dashboard.run(host=args.host, port=args.port)
        elif args.mode == "live":
            logger.info("Starting console monitoring...")
            while True:
                import time
                metrics = {
                    "portfolio": dashboard.metrics.get_portfolio_metrics(),
                    "health": dashboard.metrics.get_system_health(),
                    "trading": dashboard.metrics.get_trading_summary(),
                }
                logger.info(f"METRICS: Metrics: {json.dumps(metrics, indent=2)}")
                time.sleep(30)

    except KeyboardInterrupt:
        logger.info("\nSTOP: Shutting down dashboard...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"ERROR: Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
