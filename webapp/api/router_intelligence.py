from fastapi import APIRouter, HTTPException
from data.db_client import DBClient
from datetime import datetime
import logging
import json

router = APIRouter(prefix="/intelligence", tags=["intelligence"])
logger = logging.getLogger(__name__)

@router.get("/best-strategies")
async def get_best_strategies(limit: int = 15):
    """Returns best strategies with maturity and performance history for histograms."""
    try:
        db = DBClient()
        # Querying strategy_intelligence with latest WFO results
        query = """
            SELECT 
                strategy_name, 
                pair, 
                timeframe, 
                maturity_score, 
                latest_sharpe, 
                latest_win_rate, 
                recommended_tweaks,
                findings,
                created_at
            FROM strategy_intelligence
            WHERE status = 'ACTIVE'
            ORDER BY maturity_score DESC, latest_sharpe DESC
            LIMIT %s
        """
        rows = db.execute_query(query, (limit,))
        
        # If empty, try to populate from WFO results as a fallback/initial state
        if not rows:
            logger.info("Intelligence table empty, fetching from WFO results.")
            fallback_query = """
                SELECT s.name, w.symbol, w.timeframe, COUNT(*) as maturity, 
                       AVG(w.oos_sharpe) as sharpe, AVG(w.oos_win_rate) as wr
                FROM walk_forward_results w
                JOIN strategies s ON w.strategy_id = s.strategy_id
                GROUP BY s.name, w.symbol, w.timeframe
                ORDER BY sharpe DESC
                LIMIT %s
            """
            fallback_rows = db.execute_query(fallback_query, (limit,))
            results = []
            for r in fallback_rows:
                results.append({
                    "strategy": r[0],
                    "symbol": r[1],
                    "timeframe": r[2],
                    "maturity": r[3],
                    "sharpe": float(r[4]) if r[4] else 0.0,
                    "win_rate": float(r[5]) if r[5] else 0.0,
                    "tweaks": [],
                    "findings": "Initial WFO assessment completed."
                })
            return results

        results = []
        for r in rows:
            results.append({
                "strategy": r[0],
                "symbol": r[1],
                "timeframe": r[2],
                "maturity": r[3],
                "sharpe": float(r[4]) if r[4] else 0.0,
                "win_rate": float(r[5]) if r[5] else 0.0,
                "tweaks": r[6] if r[6] else [],
                "findings": r[7],
                "created_at": r[8].isoformat() if r[8] else None
            })
        return results
    except Exception as e:
        logger.error(f"Error in get_best_strategies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/archive-stats")
async def get_archive_stats():
    """Returns stats about the long-term archive."""
    try:
        db = DBClient()
        res = db.execute_query("SELECT COUNT(*) FROM intelligence_archive")
        count = res[0][0] if res else 0
        
        last_archive = db.execute_query("SELECT MAX(archived_at) FROM intelligence_archive")
        last_date = last_archive[0][0].isoformat() if last_archive and last_archive[0][0] else None
        
        return {
            "total_archived_records": count,
            "last_archival_date": last_date,
            "next_archival_date": "Next Thursday 23:59 UTC"
        }
    except Exception as e:
        logger.error(f"Error in get_archive_stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
