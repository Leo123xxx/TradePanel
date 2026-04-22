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

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOGS_DIR / "dashboard.log")
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

    def _get_html_dashboard(self) -> str:
        """Generate HTML dashboard."""
        portfolio = self.metrics.get_portfolio_metrics()
        health = self.metrics.get_system_health()
        trading = self.metrics.get_trading_summary()
        strategies = self.metrics.get_strategies()

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
            <title>TradePanel Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{ color: #333; border-bottom: 3px solid #2E75B6; padding-bottom: 10px; }}
                .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .metric-label {{ color: #666; font-size: 12px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2E75B6; }}
                .status {{ padding: 10px; border-radius: 4px; }}
                .status-ok {{ background: #d4edda; color: #155724; }}
                .status-error {{ background: #f8d7da; color: #721c24; }}
                .status-warning {{ background: #fff3cd; color: #856404; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #2E75B6; color: white; }}
                tr:hover {{ background: #f5f5f5; }}
                .refresh-info {{ color: #666; font-size: 12px; text-align: right; }}
                .log-panel {{
                    background: #272822;
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 10px;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 0.85rem;
                    height: 200px;
                    overflow-y: auto;
                    color: #f8f8f2;
                }}
                .log-entry {{ margin-bottom: 4px; border-bottom: 1px solid #3e3d32; }}
                .log-entry.WARNING {{ color: #f1fa8c; }}
                .log-entry.ERROR {{ color: #ff5555; }}
            </style>
            <meta http-equiv="refresh" content="30">
        </head>
        <body>
            <div class="container">
                <h1>TradePanel Dashboard</h1>
                <p class="refresh-info">Auto-refreshing every 30 seconds</p>

                <div class="section">
                    <h2>Portfolio Status</h2>
                    <div class="metric">
                        <div class="metric-label">Strategies</div>
                        <div class="metric-value">{portfolio.get('strategy_count', 0)}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Pass Rate</div>
                        <div class="metric-value">{portfolio.get('test_pass_rate', 0):.1%}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Status</div>
                        <div class="metric-value" style="color: #28a745;">✓ {os.getenv("TRADING_MODE", "unknown").upper()}</div>
                    </div>
                </div>

                <div class="section">
                    <h2>System Health</h2>
                    <div class="status status-ok">
                        <strong>Database:</strong> {health.get('database', 'UNKNOWN')} |
                        <strong>MT5:</strong> {health.get('mt5', 'UNKNOWN')} |
                        <strong>Telegram:</strong> {health.get('telegram', 'UNKNOWN')}
                    </div>
                    <p>Last checked: {health.get('last_check', 'N/A')}</p>
                </div>

                <div class="section">
                    <h2>Trading Summary</h2>
                    <div class="metric">
                        <div class="metric-label">Today Trades</div>
                        <div class="metric-value">{trading.get('today_trades', 0)}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Win Rate</div>
                        <div class="metric-value">{trading.get('win_rate', 0):.1%}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">P&L Today</div>
                        <div class="metric-value" style="color: {'#28a745' if trading.get('pnl_today', 0) >= 0 else '#dc3545'};">
                            ${trading.get('pnl_today', 0):.2f}
                        </div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Drawdown</div>
                        <div class="metric-value">{trading.get('drawdown', 0):.1%}</div>
                    </div>
                </div>

                <div class="section">
                    <h2>System Activity</h2>
                    <div class="log-panel" id="logPanel">
                        {log_html}
                    </div>
                </div>

                <div class="section">
                    <h2>Top Strategies</h2>
                    <table>
                        <tr>
                            <th>Strategy</th>
                            <th>Pair</th>
                            <th>Win Rate</th>
                            <th>Trades</th>
                            <th>Avg P&L</th>
                        </tr>
        """

        for strategy in strategies.get("strategies", [])[:10]:
            html += f"""
                        <tr>
                            <td>{strategy.get('name', 'Unknown')}</td>
                            <td>{strategy.get('pair', 'N/A')}</td>
                            <td>{strategy.get('win_rate', 0):.1%}</td>
                            <td>{strategy.get('trades', 0)}</td>
                            <td>${strategy.get('avg_pnl', 0):.2f}</td>
                        </tr>
            """

        html += """
                    </table>
                </div>
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
