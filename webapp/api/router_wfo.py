from fastapi import APIRouter, HTTPException
from data.db_client import DBClient
from datetime import datetime
import logging

router = APIRouter(prefix="/wfo", tags=["wfo"])
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_wfo_status():
    """Returns the current progress of the master WFO sweep."""
    try:
        db = DBClient()
        
        # Count strategies with at least one window result
        res = db.execute_query("SELECT COUNT(DISTINCT strategy_id) FROM walk_forward_results")
        completed_count = res[0][0] if res else 0
        
        # Total strategies (hardcoded or from config, let's guess 40 for now or query strategies table)
        res_total = db.execute_query("SELECT COUNT(*) FROM strategies")
        total_strategies = res_total[0][0] if res_total else 40
        
        # Get last 5 results
        recent = db.execute_query("""
            SELECT s.name, w.symbol, w.timeframe, w.oos_sharpe, w.oos_win_rate, w.created_at
            FROM walk_forward_results w
            JOIN strategies s ON w.strategy_id = s.strategy_id
            ORDER BY w.created_at DESC
            LIMIT 5
        """)
        
        recent_list = []
        for r in recent:
            recent_list.append({
                "strategy": r[0],
                "symbol": r[1],
                "timeframe": r[2],
                "sharpe": float(r[3]) if r[3] else 0.0,
                "win_rate": float(r[4]) if r[4] else 0.0,
                "timestamp": r[5].isoformat() if r[5] else None
            })
            
        return {
            "completed": completed_count,
            "total": total_strategies,
            "progress_pct": round((completed_count / total_strategies) * 100, 1) if total_strategies > 0 else 0,
            "recent_results": recent_list,
            "last_update": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in get_wfo_status: {e}")
        return {"error": str(e)}

@router.get("/top-alphas")
async def get_top_alphas(limit: int = 10):
    """Returns the top performing strategy-pair-timeframe combinations from WFO."""
    try:
        db = DBClient()
        rows = db.execute_query("""
            SELECT s.name, w.symbol, w.timeframe, 
                   AVG(w.oos_sharpe) as avg_sharpe, 
                   AVG(w.oos_win_rate) as avg_wr,
                   COUNT(*) as windows
            FROM walk_forward_results w
            JOIN strategies s ON w.strategy_id = s.strategy_id
            GROUP BY s.name, w.symbol, w.timeframe
            HAVING COUNT(*) >= 2
            ORDER BY avg_sharpe DESC
            LIMIT %s
        """, (limit,))
        
        alphas = []
        for r in rows:
            alphas.append({
                "strategy": r[0],
                "symbol": r[1],
                "timeframe": r[2],
                "avg_sharpe": float(r[3]),
                "avg_win_rate": float(r[4]),
                "windows": r[5]
            })
        return alphas
    except Exception as e:
        logger.error(f"Error in get_top_alphas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
