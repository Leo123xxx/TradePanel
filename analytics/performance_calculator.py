"""Performance Calculator for Trade Analytics"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.db_client import DBClient
from functools import lru_cache
import time

# Module-level cache for performance wins
_METRICS_CACHE = {}
_CACHE_TTL = 300  # 5 minutes

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Container for calculated performance metrics."""
    win_rate: float
    sharpe_ratio: float
    profit_factor: float
    max_drawdown_pct: float
    max_drawdown_usd: float
    avg_win_usd: float
    avg_loss_usd: float
    risk_reward_ratio: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    gross_profit: float
    gross_loss: float
    net_profit: float
    roi_pct: float
    recovery_factor: float
    consecutive_wins: int
    consecutive_losses: int

class PerformanceCalculator:
    """Comprehensive performance analytics for trading system."""

    def __init__(self, lookback_days: int = 30):
        self.db = DBClient()
        self.lookback_days = lookback_days
        self.start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"PerformanceCalculator: {lookback_days} days ({self.start_date} to {self.end_date})")

    def calculate_all_metrics(self) -> Dict:
        """Calculate all metrics across all dimensions with in-memory caching."""
        try:
            # Task 1.2: Check cache first
            now = time.time()
            if self.lookback_days in _METRICS_CACHE:
                cache_time, cached_data = _METRICS_CACHE[self.lookback_days]
                if now - cache_time < _CACHE_TTL:
                    logger.info(f"Returning cached metrics for {self.lookback_days} days")
                    return cached_data

            logger.info("Starting metrics calculation...")
            trades_df = self._fetch_trades()

            if trades_df.empty:
                logger.warning("No trades found in lookback period")
                return {
                    'account': None,
                    'by_strategy': {},
                    'by_asset': {},
                    'daily': [],
                    'weekly': [],
                    'monthly': [],
                    'heatmap': {},
                    'correlation': []
                }

            logger.info(f"Fetched {len(trades_df)} trades")

            # Task 1.3: Mix of DF analytics and SQL aggregation for performance
            results = {
                'account': self._calculate_account_metrics(trades_df),
                'by_strategy': self._calculate_by_strategy(trades_df),
                'by_asset': self._calculate_by_asset(trades_df),
                'daily': self._calculate_daily_pnl_sql(),  # Vectorized via SQL
                'weekly': self._calculate_weekly_pnl(trades_df),
                'monthly': self._calculate_monthly_pnl(trades_df),
                'heatmap': self._calculate_heatmap(trades_df),
                'correlation': self._calculate_correlation(trades_df)
            }

            logger.info("Metrics calculation completed, sanitizing results...")
            sanitized_results = self._sanitize(results)
            
            # Update cache
            _METRICS_CACHE[self.lookback_days] = (now, sanitized_results)
            
            return sanitized_results

        except Exception as e:
            logger.error(f"Error calculating metrics: {e}", exc_info=True)
            raise

    def _sanitize(self, obj):
        """Recursively replace NaN and Inf with None (JSON null)."""
        if obj is None:
            return None
        if isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, np.ndarray)):
            return [self._sanitize(v) for v in obj]
        elif isinstance(obj, (float, np.floating)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, (int, np.integer)):
            return int(obj)
        elif hasattr(obj, "__dict__"):
            # Convert objects/dataclasses to dicts
            return {k: self._sanitize(v) for k, v in obj.__dict__.items()}
        return obj

    def _fetch_trades(self) -> pd.DataFrame:
        """Fetch all trades from database."""
        query = """
            SELECT t.trade_id, t.strategy_id, s.name as strategy_name, t.pair,
                   t.entry_price, t.exit_price, t.mode, t.created_at,
                   t.net_pnl, t.gross_pnl, t.lot_size
            FROM trades t
            LEFT JOIN strategies s ON t.strategy_id = s.strategy_id
            WHERE t.created_at >= %s::timestamp AND t.created_at <= %s::timestamp
            ORDER BY t.created_at ASC
        """

        rows = self.db.execute_query(query, (self.start_date, self.end_date))

        if not rows:
            return pd.DataFrame()

        columns = [
            'trade_id', 'strategy_id', 'strategy_name', 'pair',
            'entry_price', 'exit_price', 'mode', 'created_at',
            'net_pnl', 'gross_pnl', 'lot_size'
        ]

        df = pd.DataFrame(rows, columns=columns)

        # Convert to numeric
        df['net_pnl'] = pd.to_numeric(df['net_pnl'], errors='coerce').fillna(0)
        df['gross_pnl'] = pd.to_numeric(df['gross_pnl'], errors='coerce').fillna(0)
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

        # Use net_pnl from DB
        df['pnl'] = df['net_pnl']
        
        return df

    def _calculate_account_metrics(self, trades_df: pd.DataFrame) -> PerformanceMetrics:
        """Calculate overall account performance."""
        if trades_df.empty:
            return None

        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] <= 0])

        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['pnl'] <= 0]['pnl'].sum())
        net_profit = trades_df['pnl'].sum()

        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (1.0 if gross_profit > 0 else 0)

        avg_win = (gross_profit / winning_trades) if winning_trades > 0 else 0
        avg_loss = (gross_loss / losing_trades) if losing_trades > 0 else 0

        risk_reward = (avg_win / avg_loss) if avg_loss > 0 else 0

        # Dynamic Initial Capital from account_profiles
        try:
            cap_query = "SELECT SUM(initial_balance) FROM account_profiles WHERE is_active = true"
            cap_res = self.db.execute_query(cap_query)
            initial_capital = float(cap_res[0][0] or 10000)
        except Exception:
            initial_capital = 10000

        # Calculate PnL % based on actual capital for accurate Sharpe/ROI
        pnl_pcts = (trades_df['pnl'].values / initial_capital)
        sharpe = self._calculate_sharpe(pnl_pcts) 
        max_dd_pct, max_dd_usd = self._calculate_max_drawdown(trades_df['pnl'].values)

        roi = (net_profit / initial_capital) * 100
        recovery_factor = (net_profit / max_dd_usd) if max_dd_usd > 0 else 0

        pnl_sign = (trades_df['pnl'] > 0).astype(int)
        consecutive_wins = self._max_consecutive(pnl_sign.values, 1)
        consecutive_losses = self._max_consecutive(pnl_sign.values, 0)

        return PerformanceMetrics(
            win_rate=round(win_rate / 100, 4),
            sharpe_ratio=round(sharpe, 2),
            profit_factor=round(profit_factor, 2),
            max_drawdown_pct=round(max_dd_pct / 100, 4),
            max_drawdown_usd=round(max_dd_usd, 2),
            avg_win_usd=round(avg_win, 2),
            avg_loss_usd=round(avg_loss, 2),
            risk_reward_ratio=round(risk_reward, 2),
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            gross_profit=round(gross_profit, 2),
            gross_loss=round(gross_loss, 2),
            net_profit=round(net_profit, 2),
            roi_pct=round(roi / 100, 4),
            recovery_factor=round(recovery_factor, 2),
            consecutive_wins=consecutive_wins,
            consecutive_losses=consecutive_losses
        )

    def _calculate_by_strategy(self, trades_df: pd.DataFrame) -> Dict[str, PerformanceMetrics]:
        """Calculate performance by strategy."""
        results = {}
        for strategy in trades_df['strategy_name'].unique():
            if pd.isna(strategy):
                continue
            strat_trades = trades_df[trades_df['strategy_name'] == strategy]
            results[strategy] = self._calculate_account_metrics(strat_trades)
        return results

    def _calculate_by_asset(self, trades_df: pd.DataFrame) -> Dict[str, PerformanceMetrics]:
        """Calculate performance by asset."""
        results = {}
        for pair in trades_df['pair'].unique():
            if pd.isna(pair):
                continue
            pair_trades = trades_df[trades_df['pair'] == pair]
            results[pair] = self._calculate_account_metrics(pair_trades)
        return results

    def _calculate_daily_pnl_sql(self) -> List[Dict]:
        """Task 1.3: Calculate daily P&L using PostgreSQL aggregation (much faster)."""
        query = """
            SELECT 
                DATE(created_at) as trade_date,
                SUM(net_pnl) as pnl,
                COUNT(*) as trades,
                ROUND(SUM(CASE WHEN net_pnl > 0 THEN 1 ELSE 0 END)::NUMERIC / COUNT(*), 4) as win_rate
            FROM trades
            WHERE created_at >= %s::timestamp AND created_at <= %s::timestamp
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at) ASC
        """
        rows = self.db.execute_query(query, (self.start_date, self.end_date))
        return [
            {
                'date': str(r[0]),
                'pnl': float(r[1] or 0),
                'trades': int(r[2] or 0),
                'win_rate': float(r[3] or 0)
            } for r in rows
        ] if rows else []

    def _calculate_daily_pnl(self, trades_df: pd.DataFrame) -> List[Dict]:
        """Calculate daily P&L."""
        trades_df = trades_df.copy()
        trades_df['date'] = trades_df['created_at'].dt.date

        daily_results = []
        for date, group in trades_df.groupby('date'):
            if pd.isna(date):
                continue
            daily_pnl = group['pnl'].sum()
            daily_trades = len(group)
            daily_wr = (len(group[group['pnl'] > 0]) / daily_trades * 100) if daily_trades > 0 else 0
            daily_results.append({
                'date': str(date),
                'pnl': round(daily_pnl, 2),
                'trades': daily_trades,
                'win_rate': round(daily_wr, 2)
            })
        return daily_results

    def _calculate_weekly_pnl(self, trades_df: pd.DataFrame) -> List[Dict]:
        """Calculate weekly P&L."""
        trades_df = trades_df.copy()
        trades_df['week'] = trades_df['created_at'].dt.to_period('W')

        weekly_results = []
        for week, group in trades_df.groupby('week'):
            if pd.isna(week):
                continue
            weekly_pnl = group['pnl'].sum()
            weekly_trades = len(group)
            weekly_wr = (len(group[group['pnl'] > 0]) / weekly_trades * 100) if weekly_trades > 0 else 0
            weekly_results.append({
                'week': str(week),
                'pnl': round(weekly_pnl, 2),
                'trades': weekly_trades,
                'win_rate': round(weekly_wr, 2)
            })
        return weekly_results

    def _calculate_monthly_pnl(self, trades_df: pd.DataFrame) -> List[Dict]:
        """Calculate monthly P&L."""
        trades_df = trades_df.copy()
        trades_df['month'] = trades_df['created_at'].dt.to_period('M')

        monthly_results = []
        for month, group in trades_df.groupby('month'):
            if pd.isna(month):
                continue
            monthly_pnl = group['pnl'].sum()
            monthly_trades = len(group)
            monthly_wr = (len(group[group['pnl'] > 0]) / monthly_trades * 100) if monthly_trades > 0 else 0
            monthly_results.append({
                'month': str(month),
                'pnl': round(monthly_pnl, 2),
                'trades': monthly_trades,
                'win_rate': round(monthly_wr, 2)
            })
        return monthly_results

    def _calculate_heatmap(self, trades_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Create heatmap of win rates by strategy × asset."""
        heatmap = {}
        for strategy in trades_df['strategy_name'].unique():
            if pd.isna(strategy):
                continue
            heatmap[strategy] = {}
            strat_trades = trades_df[trades_df['strategy_name'] == strategy]
            for pair in strat_trades['pair'].unique():
                if pd.isna(pair):
                    continue
                pair_trades = strat_trades[strat_trades['pair'] == pair]
                if len(pair_trades) == 0:
                    continue
                win_rate = (len(pair_trades[pair_trades['pnl'] > 0]) / len(pair_trades) * 100)
                heatmap[strategy][pair] = round(win_rate, 1)
        return heatmap

    def _calculate_correlation(self, trades_df: pd.DataFrame) -> List[Dict]:
        """Calculate pair correlations."""
        correlations = []
        pairs = [p for p in trades_df['pair'].unique() if not pd.isna(p)]

        if len(pairs) < 2:
            return []

        pair_pnl = {}
        for pair in pairs:
            pair_trades = trades_df[trades_df['pair'] == pair].sort_values('created_at')
            if len(pair_trades) > 0:
                pair_pnl[pair] = pair_trades.set_index('created_at')['pnl'].resample('D').sum()

        for i, pair1 in enumerate(pairs):
            for pair2 in pairs[i+1:]:
                if pair1 in pair_pnl and pair2 in pair_pnl:
                    aligned = pd.DataFrame({
                        pair1: pair_pnl[pair1],
                        pair2: pair_pnl[pair2]
                    }).dropna()

                    if len(aligned) > 1:
                        corr = aligned[pair1].corr(aligned[pair2])
                        correlations.append({
                            'pair1': pair1,
                            'pair2': pair2,
                            'correlation': round(corr, 3),
                            'strength': 'high' if abs(corr) > 0.7 else 'medium' if abs(corr) > 0.4 else 'low'
                        })

        return correlations

    def _calculate_sharpe(self, returns: np.ndarray, rf_rate: float = 0.02) -> float:
        """Calculate annualized Sharpe ratio."""
        if len(returns) < 2:
            return 0.0
        
        # Remove NaNs and Infs
        returns = returns[~np.isnan(returns) & ~np.isinf(returns)]
        
        if len(returns) < 2:
            return 0.0
            
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        if std_return == 0 or np.isnan(std_return):
            return 0.0
            
        sharpe = (mean_return - (rf_rate / 252)) / std_return * np.sqrt(252)
        return float(sharpe) if not (np.isnan(sharpe) or np.isinf(sharpe)) else 0.0

    def _calculate_max_drawdown(self, pnl_series: np.ndarray) -> Tuple[float, float]:
        """Calculate maximum drawdown."""
        if len(pnl_series) == 0:
            return 0.0, 0.0
            
        # Clean data
        pnl_series = np.nan_to_num(pnl_series, nan=0.0, posinf=0.0, neginf=0.0)
        
        cumulative_pnl = np.cumsum(pnl_series)
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdown = cumulative_pnl - running_max
        max_dd_usd = np.min(drawdown) if len(drawdown) > 0 else 0.0
        
        if len(running_max) == 0 or running_max[-1] == 0 or np.isnan(running_max[-1]):
            max_dd_pct = 0.0
        else:
            max_dd_pct = (max_dd_usd / running_max[-1]) * 100 if running_max[-1] > 0 else 0
            
        return abs(float(max_dd_pct)), abs(float(max_dd_usd))

    def _max_consecutive(self, series: np.ndarray, value: int) -> int:
        """Find maximum consecutive occurrences."""
        if len(series) == 0:
            return 0
        max_consecutive = 0
        current_consecutive = 0
        for val in series:
            if val == value:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        return max_consecutive

def generate_report(lookback_days: int = 30) -> str:
    """Generate human-readable performance report."""
    calculator = PerformanceCalculator(lookback_days)
    metrics = calculator.calculate_all_metrics()

    report = f"\n{'='*80}\n"
    report += f"TRADEPANEL PERFORMANCE REPORT\n"
    report += f"Period: Last {lookback_days} days\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"{'='*80}\n\n"

    if metrics['account']:
        m = metrics['account']
        report += "ACCOUNT SUMMARY\n"
        report += f"  Total Trades:        {m.total_trades}\n"
        report += f"  Win Rate:            {m.win_rate*100:.2f}%\n"
        report += f"  Profit Factor:       {m.profit_factor:.2f}\n"
        report += f"  Sharpe Ratio:        {m.sharpe_ratio:.2f}\n"
        report += f"  Max Drawdown:        {m.max_drawdown_pct*100:.2f}% (${m.max_drawdown_usd:,.2f})\n"
        report += f"  Net Profit:          ${m.net_profit:,.2f}\n"
        report += f"  ROI:                 {m.roi_pct*100:.2f}%\n"
        report += f"  Risk/Reward Ratio:   {m.risk_reward_ratio:.2f}\n\n"

    if metrics['by_strategy']:
        report += "PERFORMANCE BY STRATEGY\n"
        report += f"{'Strategy':<30} {'WR%':<8} {'Trades':<8} {'PF':<8} {'Sharpe':<8}\n"
        report += f"{'-'*65}\n"
        for strat_name, m in metrics['by_strategy'].items():
            if m:
                report += f"{strat_name:<30} {m.win_rate:<8.1f} {m.total_trades:<8} {m.profit_factor:<8.2f} {m.sharpe_ratio:<8.2f}\n"
        report += "\n"

    if metrics['by_asset']:
        report += "PERFORMANCE BY ASSET\n"
        report += f"{'Pair':<15} {'WR%':<8} {'Trades':<8} {'PF':<8} {'PnL':<15}\n"
        report += f"{'-'*55}\n"
        for pair, m in metrics['by_asset'].items():
            if m:
                report += f"{pair:<15} {m.win_rate:<8.1f} {m.total_trades:<8} {m.profit_factor:<8.2f} ${m.net_profit:<14,.2f}\n"
        report += "\n"

    report += f"{'='*80}\n"
    return report

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(generate_report(lookback_days=30))
