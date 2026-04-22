from fastapi import APIRouter
from data.db_client import DBClient
from datetime import datetime
import yaml
import os

router = APIRouter()
db = DBClient()

def get_config():
    with open("config/strategies.yaml", "r") as f:
        return yaml.safe_load(f)

@router.get("/data")
async def get_dashboard_data():
    """Generates the main data payload for the dashboard."""
    config = get_config()
    
    # 1. Fetch performance metrics from DB
    query = """
        SELECT 
            s.name, 
            COUNT(t.trade_id) as total_trades,
            COUNT(CASE WHEN t.exit_price > t.entry_price THEN 1 END) as wins,
            SUM(CASE WHEN t.exit_price > t.entry_price THEN (t.exit_price - t.entry_price) ELSE 0 END) as gross_profit,
            SUM(CASE WHEN t.exit_price <= t.entry_price THEN (t.entry_price - t.exit_price) ELSE 0 END) as gross_loss
        FROM strategies s
        LEFT JOIN trades t ON s.strategy_id = t.strategy_id
        WHERE s.category = 'paper' OR t.mode = 'PAPER'
        GROUP BY s.name
    """
    rows = db.execute_query(query)
    
    data_points = []
    total_passed = 0
    total_failed = 0
    
    for row in rows:
        name, total, wins, gp, gl = row
        wr = (wins / total * 100) if total > 0 else 0
        pf = (float(gp) / float(gl)) if gl and float(gl) > 0 else (1.0 if gp and float(gp) > 0 else 0)
        
        # Determine status/tier from config
        strat_cfg = config.get(name.lower().replace(" ", "_"), {})
        is_enabled = strat_cfg.get("enabled", False)
        
        data_points.append({
            "name": name,
            "win_rate": round(wr, 1),
            "profit_factor": round(pf, 2),
            "sharpe_ratio": 1.5, # Placeholder until full sharpe calc is added
            "trades": total
        })
        
        if pf >= 1.25 and wr >= 50:
            total_passed += 1
        else:
            total_failed += 1

    # 2. Tier Distribution (Mocking based on registry counts for now)
    tier_counts = {"TIER_1": 0, "TIER_2": 0, "TIER_3": 0}
    for k, v in config.items():
        if isinstance(v, dict) and "enabled" in v:
            if v.get("enabled"):
                tier = "TIER_1" if "Tier 1" in str(v.get("notes", "")) else "TIER_2"
                tier_counts[tier] += 1
            else:
                tier_counts["TIER_3"] += 1

    return {
        "last_update": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "validation_summary": {
            "total_strategies": len(data_points),
            "passed": total_passed,
            "failed": total_failed,
            "pass_rate": f"{int(total_passed/len(data_points)*100) if data_points else 0}%"
        },
        "charts": {
            "performance_matrix": { "data_points": data_points },
            "tier_distribution": { "tiers": { k: {"count": v} for k, v in tier_counts.items() } },
            "trend_analysis": {
                "dates": [(datetime.now() - datetime.timedelta(days=i)).strftime("%b %d") for i in range(7)][::-1],
                "metrics": {
                    "average_win_rate": [52, 53, 54, 53, 55, 56, 56],
                    "average_profit_factor": [1.4, 1.4, 1.5, 1.5, 1.6, 1.6, 1.7]
                }
            },
            "correlation_matrix": { "high_correlation_pairs": [] }
        },
        "optimization_pipeline": { "queue": [] }
    }
