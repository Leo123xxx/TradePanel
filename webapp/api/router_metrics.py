from fastapi import APIRouter, Response
from data.db_client import DBClient
from datetime import datetime
import logging

router = APIRouter(prefix="/metrics", tags=["metrics"])
logger = logging.getLogger(__name__)

@router.get("")
async def get_prometheus_metrics():
    """
    Exposes account metrics in Prometheus text format.
    Scrapable by Prometheus at /api/metrics
    """
    db = DBClient()
    try:
        # Get latest snapshot
        snapshot = db.execute_query(
            "SELECT timestamp, equity, balance, margin_level, floating_pnl, realized_pnl_today, drawdown_pct, active_positions "
            "FROM account_metrics ORDER BY timestamp DESC LIMIT 1"
        )
        
        if not snapshot:
            return Response(content="# No metrics available yet", media_type="text/plain")

        s = snapshot[0]
        ts = int(s[0].timestamp() * 1000) # Epoch ms
        
        metrics = [
            f"# HELP tradepanel_account_equity Current account equity",
            f"# TYPE tradepanel_account_equity gauge",
            f"tradepanel_account_equity {s[1]}",
            
            f"# HELP tradepanel_account_balance Current account balance",
            f"# TYPE tradepanel_account_balance gauge",
            f"tradepanel_account_balance {s[2]}",
            
            f"# HELP tradepanel_account_margin_level Current margin level percentage",
            f"# TYPE tradepanel_account_margin_level gauge",
            f"tradepanel_account_margin_level {s[3]}",
            
            f"# HELP tradepanel_account_floating_pnl Current floating P&L",
            f"# TYPE tradepanel_account_floating_pnl gauge",
            f"tradepanel_account_floating_pnl {s[4]}",
            
            f"# HELP tradepanel_account_realized_pnl_today Realized P&L for today",
            f"# TYPE tradepanel_account_realized_pnl_today gauge",
            f"tradepanel_account_realized_pnl_today {s[5]}",
            
            f"# HELP tradepanel_account_drawdown_pct Current drawdown percentage",
            f"# TYPE tradepanel_account_drawdown_pct gauge",
            f"tradepanel_account_drawdown_pct {s[6]}",
            
            f"# HELP tradepanel_account_active_positions Number of open positions",
            f"# TYPE tradepanel_account_active_positions gauge",
            f"tradepanel_account_active_positions {s[7]}",
            
            f"# HELP tradepanel_metrics_last_updated_timestamp Timestamp of last metrics update",
            f"# TYPE tradepanel_metrics_last_updated_timestamp gauge",
            f"tradepanel_metrics_last_updated_timestamp {ts}"
        ]
        
        content = "\n".join(metrics) + "\n"
        return Response(content=content, media_type="text/plain")
        
    except Exception as e:
        logger.error(f"Error generating Prometheus metrics: {e}")
        return Response(content=f"# Error: {str(e)}", media_type="text/plain", status_code=500)
