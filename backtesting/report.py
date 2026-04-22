"""
backtesting/report.py — Scorecard printer and database persistence for backtest runs.
"""

import json
from data.db_client import DBClient


# Metrics that should be displayed with a % suffix
_PCT_KEYS = {
    "total_return_pct", "win_rate", "long_win_rate", "short_win_rate",
    "max_drawdown_pct", "avg_drawdown_pct",
}

# Section groupings for the printed scorecard
_SECTIONS = {
    "Overview": [
        "total_trades", "total_wins", "total_losses",
        "total_pnl", "total_return_pct", "final_equity",
    ],
    "Win / Loss": [
        "win_rate", "profit_factor", "win_loss_ratio", "expectancy",
        "gross_profit", "gross_loss", "avg_win", "avg_loss",
        "best_trade", "worst_trade",
    ],
    "Streak": ["max_consecutive_wins", "max_consecutive_losses"],
    "Duration": ["avg_trade_duration_hrs"],
    "Drawdown": ["max_drawdown_pct", "avg_drawdown_pct", "recovery_factor"],
    "Risk-Adjusted": ["sharpe_ratio", "sortino_ratio", "calmar_ratio"],
    "Direction": ["long_win_rate", "short_win_rate"],
    "Costs": ["total_commission_paid", "total_spread_cost"],
}


class StatsReport:
    def __init__(self):
        self.db = DBClient()

    def generate_scorecard(self, metrics: dict):
        """Pretty-print the full 25-metric scorecard to stdout."""
        if "error" in metrics:
            print(f"\n  [!] {metrics['error']}\n")
            return

        print("\n" + "=" * 52)
        print("         BACKTEST PERFORMANCE SCORECARD")
        print("=" * 52)

        for section, keys in _SECTIONS.items():
            print(f"\n  -- {section} " + "-" * (44 - len(section)))
            for k in keys:
                if k not in metrics:
                    continue
                v = metrics[k]
                label = k.replace("_", " ").title()
                if k in _PCT_KEYS:
                    print(f"  {label:<30} {v:>8.2f} %")
                elif isinstance(v, float):
                    print(f"  {label:<30} {v:>10.4f}")
                else:
                    print(f"  {label:<30} {v:>10}")

        print("\n" + "=" * 52 + "\n")

    def _clean_metrics(self, d):
        """Replaces Infinity/NaN with None for JSON compliance."""
        import math
        clean = {}
        for k, v in d.items():
            if isinstance(v, float) and (math.isinf(v) or math.isnan(v)):
                clean[k] = None
            elif isinstance(v, dict):
                clean[k] = self._clean_metrics(v)
            else:
                clean[k] = v
        return clean

    def save_run(self, strategy_id: int, symbol: str, timeframe: str,
                 metrics: dict, trades_df) -> int | None:
        """Persist backtest results to the backtest_runs table."""
        print("Saving backtest run to database...")

        start_date = trades_df["open_time"].min() if not trades_df.empty else None
        end_date = trades_df["close_time"].max() if not trades_df.empty else None

        clean_metrics = self._clean_metrics(metrics)

        query = """
            INSERT INTO backtest_runs
                (strategy_id, pair, timeframe, start_date, end_date, metrics, scorecard)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING run_id
        """
        params = (
            strategy_id,
            symbol,
            timeframe,
            start_date,
            end_date,
            json.dumps(clean_metrics),
            json.dumps(clean_metrics),
        )

        result = self.db.execute_query(query, params)
        run_id = result[0][0] if result else None
        print(f"  Run saved — ID: {run_id}")
        return run_id
