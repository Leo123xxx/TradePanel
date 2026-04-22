"""
backtesting/engine.py — Bar-by-bar backtesting simulation engine.

Design rules (non-negotiable):
  - Entry on bar[i+1] OPEN after signal fires on bar[i] CLOSE — no look-ahead bias.
  - TP/SL checked every bar using high/low (SL wins on same-bar conflict).
  - All costs loaded from config.yaml per-pair section.
  - No random values — all costs are deterministic from config.
"""

import uuid
import yaml
import os
import pandas as pd
import numpy as np
from logging_.event_logger import EventLogger

PIP_SIZES = {
    "EURUSD": 0.0001,
    "GBPUSD": 0.0001,
    "USDJPY": 0.01,
    "XAUUSD": 0.10,
    "XAGUSD": 0.001,
    "BTCUSD": 1.0,
    "ETHUSD": 1.0,
}
DEFAULT_PIP_SIZE = 0.0001


class BacktestEngine:

    def __init__(self, config_path=None, lot_size=0.1, initial_balance=10000.0):
        self.lot_size = lot_size
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trades = []
        self.logger = EventLogger()

        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml"
            )
        with open(config_path, "r") as f:
            self._cfg = yaml.safe_load(f)

    def run(self, strategy, symbol, timeframe, data_df, silent=False):
        if not silent:
            print(f"\nBacktest: {strategy.name} | {symbol} | {timeframe}")
            print(f"  Bars   : {len(data_df):,}")
            print(f"  Period : {data_df.index[0].date()}  to  {data_df.index[-1].date()}")

            self.logger.log_event(
                "BACKTEST_START", "INFO",
                f"Starting backtest for {symbol} on {timeframe}.",
                {"strategy": strategy.name, "symbol": symbol, "timeframe": timeframe, "bars": len(data_df)}
            )

        pair_cfg = self._load_pair_cfg(symbol)
        pip_size = PIP_SIZES.get(symbol, DEFAULT_PIP_SIZE)

        df = strategy.generate_signals(data_df.copy())
        atr_period = strategy.params.get("atr_period", 14)
        df = self._add_atr(df, atr_period, pip_size)

        tp_mult = strategy.params.get("tp_atr_mult", 2.0)
        sl_mult = strategy.params.get("sl_atr_mult", 1.0)

        self.trades = []
        active_trade = None

        for i in range(1, len(df)):
            bar = df.iloc[i]
            prev_bar = df.iloc[i - 1]
            ts = df.index[i]

            if active_trade is not None:
                closed = self._check_exit(active_trade, bar, ts, prev_bar, pair_cfg, pip_size)
                if closed:
                    active_trade = None

            if active_trade is None and prev_bar["signal"] != 0:
                direction = "BUY" if prev_bar["signal"] == 1 else "SELL"
                atr_val = prev_bar.get("atr", np.nan)
                active_trade = self._open_trade(
                    strategy, symbol, direction,
                    bar["open"], ts, atr_val,
                    tp_mult, sl_mult, pair_cfg, pip_size
                )

        if active_trade is not None:
            self._close_trade(
                active_trade, df.iloc[-1]["close"],
                df.index[-1], "END_OF_DATA", pair_cfg, pip_size
            )

        if not silent:
            print(f"  Trades : {len(self.trades)}")

            self.logger.log_event(
                "BACKTEST_END", "SUCCESS",
                f"Backtest completed for {symbol} on {timeframe}.",
                {
                    "strategy": strategy.name,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "trade_count": len(self.trades),
                    "initial_balance": self.initial_balance,
                    "final_balance": self.balance
                }
            )
        return pd.DataFrame(self.trades) if self.trades else pd.DataFrame(), df

    def _load_pair_cfg(self, symbol):
        pairs = self._cfg.get("pairs", {})
        if symbol in pairs:
            return pairs[symbol]
        return {
            "spread_pips": self._cfg.get("default_spread", 2.0),
            "slippage_pips": 1.0,
            "commission_per_lot": 7.0,
            "pip_value_per_lot": 10.0,
        }

    def _add_atr(self, df, period, pip_size):
        prev_close = df["close"].shift(1)
        tr = pd.concat([
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ], axis=1).max(axis=1)
        df["atr"] = tr.ewm(alpha=1.0 / period, adjust=False).mean() / pip_size
        return df

    def _open_trade(self, strategy, symbol, direction, entry_open, ts,
                    atr_pips, tp_mult, sl_mult, pair_cfg, pip_size):
        spread = pair_cfg.get("spread_pips", 2.0)
        slip = pair_cfg.get("slippage_pips", 1.0)
        total_cost_pips = spread + slip

        if direction == "BUY":
            entry_price = entry_open + total_cost_pips * pip_size
        else:
            entry_price = entry_open - total_cost_pips * pip_size

        tp_price = sl_price = None
        if atr_pips is not None and not np.isnan(atr_pips) and atr_pips > 0:
            tp_dist = atr_pips * tp_mult * pip_size
            sl_dist = atr_pips * sl_mult * pip_size
            if direction == "BUY":
                tp_price = entry_open + tp_dist
                sl_price = entry_open - sl_dist
            else:
                tp_price = entry_open - tp_dist
                sl_price = entry_open + sl_dist

        return {
            "trade_id": str(uuid.uuid4()),
            "strategy": strategy.name,
            "pair": symbol,
            "direction": direction,
            "lot_size": self.lot_size,
            "entry_open": entry_open,
            "entry_price": entry_price,
            "entry_cost_pips": total_cost_pips,
            "tp_price": tp_price,
            "sl_price": sl_price,
            "open_time": ts,
            "status": "OPEN",
        }

    def _check_exit(self, trade, bar, ts, prev_bar, pair_cfg, pip_size):
        direction = trade["direction"]
        tp = trade.get("tp_price")
        sl = trade.get("sl_price")
        exit_price = None
        reason = None

        if direction == "BUY":
            if sl is not None and bar["low"] <= sl:
                exit_price, reason = sl, "SL_HIT"
            elif tp is not None and bar["high"] >= tp:
                exit_price, reason = tp, "TP_HIT"
        else:
            if sl is not None and bar["high"] >= sl:
                exit_price, reason = sl, "SL_HIT"
            elif tp is not None and bar["low"] <= tp:
                exit_price, reason = tp, "TP_HIT"

        if exit_price is None:
            if (direction == "BUY" and prev_bar["signal"] == -1) or \
               (direction == "SELL" and prev_bar["signal"] == 1):
                exit_price = bar["open"]
                reason = "SIGNAL_REVERSAL"

        if exit_price is not None:
            self._close_trade(trade, exit_price, ts, reason, pair_cfg, pip_size)
            return True
        return False

    def _close_trade(self, trade, exit_price, ts, reason, pair_cfg, pip_size):
        pip_val = pair_cfg.get("pip_value_per_lot", 10.0)
        commission = pair_cfg.get("commission_per_lot", 7.0)
        spread = pair_cfg.get("spread_pips", 2.0)

        direction = trade["direction"]
        entry_price = trade["entry_price"]
        lot = trade["lot_size"]

        price_diff = (exit_price - entry_price) if direction == "BUY" \
            else (entry_price - exit_price)
        gross_pips = price_diff / pip_size
        gross_usd = gross_pips * pip_val * lot

        commission_cost = commission * lot * 2
        spread_cost = spread * pip_val * lot
        net_pnl = gross_usd - commission_cost - spread_cost

        open_time = trade["open_time"]
        try:
            duration_secs = (ts - open_time).total_seconds()
        except Exception:
            duration_secs = 0

        trade.update({
            "exit_price": exit_price,
            "close_time": ts,
            "close_reason": reason,
            "duration_seconds": duration_secs,
            "gross_pnl_pips": round(gross_pips, 2),
            "gross_pnl_usd": round(gross_usd, 4),
            "commission_cost": round(commission_cost, 4),
            "spread_cost": round(spread_cost, 4),
            "net_pnl": round(net_pnl, 4),
            "status": "CLOSED",
        })
        self.trades.append(dict(trade))
