import os
import json
import logging
from datetime import datetime, timedelta
from data.db_client import DBClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WeeklyArchive")

def run_archival():
    db = DBClient()
    now = datetime.now()
    
    logger.info(f"Starting weekly archival process: {now}")
    
    try:
        # 1. Fetch active intelligence that hasn't been updated in 1 week
        # (Or as per user request: everything from the last week moves to long term storage)
        # Actually, user says: "moved to long term storage once a week on Thursdays night to make sure we always work with the latest results"
        # This implies we keep the LATEST in active, and move OLDER or ALL HISTORICAL TWEAKS to archive.
        
        # We'll archive records from strategy_intelligence that are older than 7 days
        # and move historical tweaks to the archive table.
        
        query_fetch = """
            SELECT intel_id, strategy_name, pair, timeframe, maturity_score, 
                   latest_sharpe, latest_win_rate, recommended_tweaks, findings, created_at
            FROM strategy_intelligence
            WHERE created_at < %s
        """
        cutoff = now - timedelta(days=7)
        rows = db.execute_query(query_fetch, (cutoff,))
        
        if not rows:
            logger.info("No records found for archival.")
        else:
            logger.info(f"Archiving {len(rows)} records...")
            for r in rows:
                intel_id, s_name, pair, tf, maturity, sharpe, wr, tweaks, findings, created = r
                
                # Prepare summary report
                report = {
                    "maturity_at_archive": maturity,
                    "sharpe_at_archive": float(sharpe) if sharpe else 0,
                    "win_rate_at_archive": float(wr) if wr else 0,
                    "tweaks": tweaks,
                    "findings": findings,
                    "created_at": created.isoformat()
                }
                
                # Insert into archive
                db.execute_query("""
                    INSERT INTO intelligence_archive (original_intel_id, strategy_name, pair, timeframe, summary_report)
                    VALUES (%s, %s, %s, %s, %s)
                """, (intel_id, s_name, pair, tf, json.dumps(report)))
                
                # Delete from active (or mark as archived)
                db.execute_query("DELETE FROM strategy_intelligence WHERE intel_id = %s", (intel_id,))
        
        # 2. Also move old WFO results to long-term storage (if any older than 30 days)
        # to keep the active table lean.
        wfo_cutoff = now - timedelta(days=30)
        db.execute_query("""
            INSERT INTO intelligence_archive (strategy_name, pair, timeframe, summary_report)
            SELECT s.name, w.symbol, w.timeframe, 
                   jsonb_build_object('type', 'WFO_RESULT', 'sharpe', w.oos_sharpe, 'wr', w.oos_win_rate, 'date', w.created_at)
            FROM walk_forward_results w
            JOIN strategies s ON w.strategy_id = s.strategy_id
            WHERE w.created_at < %s
        """, (wfo_cutoff,))
        
        db.execute_query("DELETE FROM walk_forward_results WHERE created_at < %s", (wfo_cutoff,))
        
        logger.info("Archival process completed successfully.")
        
    except Exception as e:
        logger.error(f"Archival failed: {e}")

if __name__ == "__main__":
    run_archival()
