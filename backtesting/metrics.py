"""
backtesting/metrics.py — 28-metric performance scorecard (master plan Section 8.3).
"""

import pandas as pd
import numpy as np


class BacktestMetrics:

    TRADING_DAYS_PER_YEAR = 252

    def __init__(self, signals_df, trades_df, initial_balance=10000.0):
        self.signals = signals_df
        self.trades = trades_df
        self.initial_balance = initial_balance

    def calculate_all(self):
        if self.trades is None or self.trades.empty:
            return {"error": "No trades generated — check strategy signals and data."}

        t = self.trades
        ib = self.initial_balance

        equity = t["net_pnl"].cumsum() + ib
        peak = equity.cummax()
        drawdown_abs = equity - peak
        drawdown_pct = (drawdown_abs / peak) * 100

        wins = t[t["net_pnl"] > 0]
        losses = t[t["net_pnl"] <= 0]
        n = len(t)

        total_pnl = t["net_pnl"].sum()
        gross_profit = wins["net_pnl"].sum()
        gross_loss_abs = abs(losses["net_pnl"].sum())

        win_rate = (len(wins) / n) * 100
        profit_factor = (gross_profit / gross_loss_abs) if gross_loss_abs > 0 else float("inf")

        avg_win = wins["net_pnl"].mean() if not wins.empty else 0.0
        avg_loss = losses["net_pnl"].mean() if not losses.empty else 0.0
        win_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else float("inf")
        expectancy = (win_rate / 100) * avg_win + (1 - win_rate / 100) * avg_loss

        max_dd_pct = abs(drawdown_pct.min())
        max_dd_abs = abs(drawdown_abs.min())
        avg_dd_pct = abs(drawdown_pct[drawdown_pct < 0].mean()) if (drawdown_pct < 0).any() else 0.0

        longs = t[t["direction"] == "BUY"]
        shorts = t[t["direction"] == "SELL"]
        long_win_rate = (len(longs[longs["net_pnl"] > 0]) / len(longs) * 100) if not longs.empty else 0.0
        short_win_rate = (len(shorts[shorts["net_pnl"] > 0]) / len(shorts) * 100) if not shorts.empty else 0.0

        outcomes = (t["net_pnl"] > 0).astype(int)
        max_consec_wins = self._max_consecutive(outcomes, 1)
        max_consec_losses = self._max_consecutive(outcomes, 0)

        avg_duration_hrs = t["duration_seconds"].mean() / 3600 if "duration_seconds" in t.columns else 0.0

        sharpe = self._sharpe(t["net_pnl"], ib)
        sortino = self._sortino(t["net_pnl"], ib)
        calmar = ((total_pnl / ib) * 100) / max_dd_pct if max_dd_pct > 0 else float("inf")
        recovery_factor = total_pnl / max_dd_abs if max_dd_abs > 0 else float("inf")

        total_commission = t["commission_cost"].sum() if "commission_cost" in t.columns else 0.0
        total_spread_cost = t["spread_cost"].sum() if "spread_cost" in t.columns else 0.0

        return {
            "total_trades":           int(n),
            "total_wins":             int(len(wins)),
            "total_losses":           int(len(losses)),
            "total_pnl":              round(float(total_pnl), 2),
            "total_return_pct":       round(float((total_pnl / ib) * 100), 2),
            "final_equity":           round(float(equity.iloc[-1]), 2),
            "win_rate":               round(float(win_rate), 2),
            "profit_factor":          round(float(profit_factor), 4),
            "win_loss_ratio":         round(float(win_loss_ratio), 4),
            "expectancy":             round(float(expectancy), 4),
            "gross_profit":           round(float(gross_profit), 2),
            "gross_loss":             round(float(gross_loss_abs), 2),
            "avg_win":                round(float(avg_win), 4),
            "avg_loss":               round(float(avg_loss), 4),
            "best_trade":             round(float(t["net_pnl"].max()), 4),
            "worst_trade":            round(float(t["net_pnl"].min()), 4),
            "max_consecutive_wins":   int(max_consec_wins),
            "max_consecutive_losses": int(max_consec_losses),
            "avg_trade_duration_hrs": round(float(avg_duration_hrs), 2),
            "max_drawdown_pct":       round(float(max_dd_pct), 2),
            "avg_drawdown_pct":       round(float(avg_dd_pct), 2),
            "recovery_factor":        round(float(recovery_factor), 4),
            "sharpe_ratio":           round(float(sharpe), 4),
            "sortino_ratio":          round(float(sortino), 4),
            "calmar_ratio":           round(float(calmar), 4),
            "long_win_rate":          round(float(long_win_rate), 2),
            "short_win_rate":         round(float(short_win_rate), 2),
            "total_commission_paid":  round(float(total_commission), 2),
            "total_spread_cost":      round(float(total_spread_cost), 2),
        }

    @staticmethod
    def _max_consecutive(series, target):
        max_run = cur_run = 0
        for v in series:
            if v == target:
                cur_run += 1
                max_run = max(max_run, cur_run)
            else:
                cur_run = 0
        return max_run

    def _sharpe(self, pnl, ib, risk_free=0.0):
        if len(pnl) < 2:
            return 0.0
        returns = pnl / ib
        std_r = returns.std(ddof=1)
        if std_r == 0:
            return 0.0
        return float(((returns.mean() - risk_free) / std_r) * np.sqrt(self.TRADING_DAYS_PER_YEAR))

    def _sortino(self, pnl, ib, risk_free=0.0):
        if len(pnl) < 2:
            return 0.0
        returns = pnl / ib
        downside = returns[returns < risk_free]
        if downside.empty:
            return float("inf")
        downside_std = np.sqrt((downside ** 2).mean())
        if downside_std == 0:
            return 0.0
        return float(((returns.mean() - risk_free) / downside_std) * np.sqrt(self.TRADING_DAYS_PER_YEAR))
