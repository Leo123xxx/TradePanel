"""
Analytics Router - Exposes comprehensive performance metrics via REST API.
Used by dashboard to display performance charts, heatmaps, and breakdowns.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from analytics.performance_calculator import PerformanceCalculator

router = APIRouter(prefix="/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)


@router.get("/summary")
async def get_analytics_summary(lookback_days: int = 30):
    """
    Get comprehensive account summary.
    Includes: total trades, win rate, sharpe, drawdown, profit factor, ROI.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        if not metrics['account']:
            return {"error": "No trades found"}

        m = metrics['account']

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "account_summary": {
                "total_trades": m['total_trades'],
                "winning_trades": m['winning_trades'],
                "losing_trades": m['losing_trades'],
                "win_rate": m['win_rate'],
                "profit_factor": m['profit_factor'],
                "sharpe_ratio": m['sharpe_ratio'],
                "max_drawdown_pct": m['max_drawdown_pct'],
                "max_drawdown_usd": m['max_drawdown_usd'],
                "net_profit": m['net_profit'],
                "gross_profit": m['gross_profit'],
                "gross_loss": m['gross_loss'],
                "roi_pct": m['roi_pct'],
                "risk_reward_ratio": m['risk_reward_ratio'],
                "recovery_factor": m['recovery_factor'],
                "avg_win": m.get('avg_win_usd', 0),
                "avg_loss": m.get('avg_loss_usd', 0),
                "consecutive_wins": m['consecutive_wins'],
                "consecutive_losses": m['consecutive_losses'],
                "avg_duration_seconds": m.get('avg_duration_seconds', 0)
            }
        }
    except Exception as e:
        logger.error(f"Error in get_analytics_summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-strategy")
async def get_performance_by_strategy(lookback_days: int = 30):
    """
    Get performance metrics grouped by strategy.
    Useful for identifying which strategies are performing best.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        strategies = {}
        for strat_name, m in metrics['by_strategy'].items():
            if m:
                strategies[strat_name] = {
                    "total_trades": m['total_trades'],
                    "winning_trades": m['winning_trades'],
                    "losing_trades": m['losing_trades'],
                    "win_rate": m['win_rate'],
                    "profit_factor": m['profit_factor'],
                    "sharpe_ratio": m['sharpe_ratio'],
                    "max_drawdown_pct": m['max_drawdown_pct'],
                    "net_profit": m['net_profit'],
                    "roi_pct": m['roi_pct'],
                    "risk_reward_ratio": m['risk_reward_ratio']
                }

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "strategies": strategies
        }
    except Exception as e:
        logger.error(f"Error in get_performance_by_strategy: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-asset")
async def get_performance_by_asset(lookback_days: int = 30):
    """
    Get performance metrics grouped by trading pair (asset).
    Shows which pairs are most profitable.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        assets = {}
        for pair, m in metrics['by_asset'].items():
            if m:
                assets[pair] = {
                    "total_trades": m['total_trades'],
                    "winning_trades": m['winning_trades'],
                    "losing_trades": m['losing_trades'],
                    "win_rate": m['win_rate'],
                    "profit_factor": m['profit_factor'],
                    "sharpe_ratio": m['sharpe_ratio'],
                    "max_drawdown_pct": m['max_drawdown_pct'],
                    "net_profit": m['net_profit'],
                    "roi_pct": m['roi_pct'],
                    "risk_reward_ratio": m['risk_reward_ratio']
                }

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "assets": assets
        }
    except Exception as e:
        logger.error(f"Error in get_performance_by_asset: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/daily")
async def get_daily_pnl(lookback_days: int = 30):
    """
    Get daily P&L breakdown.
    Time series of daily profit/loss and win rates.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "daily": metrics['daily']
        }
    except Exception as e:
        logger.error(f"Error in get_daily_pnl: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weekly")
async def get_weekly_pnl(lookback_days: int = 30):
    """
    Get weekly P&L breakdown.
    Time series of weekly profit/loss and win rates.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "weekly": metrics['weekly']
        }
    except Exception as e:
        logger.error(f"Error in get_weekly_pnl: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monthly")
async def get_monthly_pnl(lookback_days: int = 30):
    """
    Get monthly P&L breakdown.
    Time series of monthly profit/loss and win rates.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "monthly": metrics['monthly']
        }
    except Exception as e:
        logger.error(f"Error in get_monthly_pnl: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heatmap")
async def get_heatmap(lookback_days: int = 30):
    """
    Get win rate heatmap: Strategy × Asset.
    Shows which strategy-pair combinations perform best.
    Useful for portfolio construction and strategy allocation.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        # Convert to list format for easier frontend consumption
        heatmap_data = []
        for strategy, pairs in metrics['heatmap'].items():
            for pair, win_rate in pairs.items():
                heatmap_data.append({
                    "strategy": strategy,
                    "pair": pair,
                    "win_rate": win_rate
                })

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "heatmap": heatmap_data,
            "heatmap_dict": metrics['heatmap']
        }
    except Exception as e:
        logger.error(f"Error in get_heatmap: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/correlation")
async def get_correlation(lookback_days: int = 30):
    """
    Get pair correlation analysis.
    Shows which pairs move together.
    High correlation pairs should be avoided (redundant exposure).
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "correlations": metrics['correlation']
        }
    except Exception as e:
        logger.error(f"Error in get_correlation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_full_dashboard(lookback_days: int = 30):
    """
    Get complete dashboard data in one call.
    Includes: summary, by-strategy, by-asset, daily/weekly/monthly, heatmap, correlation.
    """
    try:
        calculator = PerformanceCalculator(lookback_days)
        metrics = calculator.calculate_all_metrics()

        # Format summary
        summary = None
        if metrics['account']:
            m = metrics['account']
            summary = {
                "total_trades": m['total_trades'],
                "win_rate": m['win_rate'],
                "profit_factor": m['profit_factor'],
                "sharpe_ratio": m['sharpe_ratio'],
                "max_drawdown_pct": m['max_drawdown_pct'],
                "net_profit": m['net_profit'],
                "roi_pct": m['roi_pct']
            }

        # Format by-strategy
        by_strategy = {}
        for strat_name, m in metrics['by_strategy'].items():
            if m:
                by_strategy[strat_name] = {
                    "total_trades": m['total_trades'],
                    "win_rate": m['win_rate'],
                    "profit_factor": m['profit_factor'],
                    "net_profit": m['net_profit']
                }

        # Format by-asset
        by_asset = {}
        for pair, m in metrics['by_asset'].items():
            if m:
                by_asset[pair] = {
                    "total_trades": m['total_trades'],
                    "win_rate": m['win_rate'],
                    "profit_factor": m['profit_factor'],
                    "net_profit": m['net_profit']
                }

        # Format heatmap
        heatmap_data = []
        for strategy, pairs in metrics['heatmap'].items():
            for pair, win_rate in pairs.items():
                heatmap_data.append({
                    "strategy": strategy,
                    "pair": pair,
                    "win_rate": win_rate
                })

        return {
            "lookback_days": lookback_days,
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "by_strategy": by_strategy,
            "by_asset": by_asset,
            "daily": metrics['daily'],
            "weekly": metrics['weekly'],
            "monthly": metrics['monthly'],
            "heatmap": heatmap_data,
            "correlations": metrics['correlation']
        }
    except Exception as e:
        logger.error(f"Error in get_full_dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint - returns API status."""
    return {
        "status": "ok",
        "service": "analytics",
        "timestamp": datetime.now().isoformat()
    }
