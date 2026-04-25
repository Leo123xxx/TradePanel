# Analytics Module - Trade Performance Analysis

Comprehensive analytics engine for calculating performance metrics, generating reports, and powering dashboard visualizations.

## Overview

The analytics module calculates detailed performance metrics from trading data stored in PostgreSQL:

- **Sharpe Ratio** — Risk-adjusted return (annualized)
- **Win Rate** — Percentage of profitable trades
- **Profit Factor** — Gross profit / gross loss ratio
- **Max Drawdown** — Peak-to-trough decline (USD and %)
- **Risk/Reward Ratio** — Avg win / avg loss
- **ROI** — Return on investment
- **Recovery Factor** — Net profit / max drawdown
- **Heatmaps** — Win rate by strategy × asset
- **Correlation Analysis** — Pair movement correlation

## Components

### performance_calculator.py

Core analytics engine.

**Classes:**
- `PerformanceMetrics` — Data container for calculated metrics
- `PerformanceCalculator` — Main calculator class

**Usage:**
```python
from analytics.performance_calculator import PerformanceCalculator

# Calculate metrics for last 30 days
calculator = PerformanceCalculator(lookback_days=30)
metrics = calculator.calculate_all_metrics()

# Access account-wide metrics
print(f"Win rate: {metrics['account'].win_rate}%")
print(f"Sharpe: {metrics['account'].sharpe_ratio}")

# By strategy
for strategy, m in metrics['by_strategy'].items():
    print(f"{strategy}: {m.win_rate}% WR, {m.profit_factor} PF")

# By asset
for pair, m in metrics['by_asset'].items():
    print(f"{pair}: ${m.net_profit}")

# Time series
for day in metrics['daily']:
    print(f"{day['date']}: ${day['pnl']} ({day['trades']} trades)")

# Heatmap and correlation
print(metrics['heatmap'])  # {strategy: {pair: win_rate, ...}, ...}
print(metrics['correlation'])  # [{pair1, pair2, correlation, strength}, ...]
```

**Generate Report:**
```python
from analytics.performance_calculator import generate_report

report = generate_report(lookback_days=30)
print(report)
```

## API Endpoints

All endpoints are available at `/api/analytics/` prefix.

### Summary Endpoints

#### `/analytics/summary`
Get account-wide summary metrics.

**Query Params:**
- `lookback_days` (int, default=30) — Analysis period

**Response:**
```json
{
  "lookback_days": 30,
  "generated_at": "2026-04-24T12:30:00",
  "account_summary": {
    "total_trades": 125,
    "winning_trades": 68,
    "losing_trades": 57,
    "win_rate": 54.4,
    "profit_factor": 1.85,
    "sharpe_ratio": 1.42,
    "max_drawdown_pct": 8.5,
    "max_drawdown_usd": 850,
    "net_profit": 2350,
    "roi_pct": 23.5,
    ...
  }
}
```

#### `/analytics/by-strategy`
Performance broken down by strategy.

**Response:**
```json
{
  "lookback_days": 30,
  "strategies": {
    "rsi_bounce": {
      "total_trades": 45,
      "win_rate": 52,
      "profit_factor": 1.6,
      ...
    },
    "dual_ema_fractal": {
      ...
    }
  }
}
```

#### `/analytics/by-asset`
Performance broken down by trading pair.

**Response:**
```json
{
  "lookback_days": 30,
  "assets": {
    "EURUSD": {
      "total_trades": 50,
      "win_rate": 56,
      "profit_factor": 1.9,
      "net_profit": 1200,
      ...
    },
    "XAUUSD": {...}
  }
}
```

#### `/analytics/by-timeframe`
Performance broken down by timeframe (M5, H1, H4, D1, etc).

**Response:**
```json
{
  "lookback_days": 30,
  "timeframes": {
    "M5": {
      "total_trades": 60,
      "win_rate": 50,
      ...
    },
    "H1": {...}
  }
}
```

### Time Series Endpoints

#### `/analytics/daily`
Daily P&L breakdown.

**Response:**
```json
{
  "daily": [
    {
      "date": "2026-04-20",
      "pnl": 350,
      "trades": 8,
      "win_rate": 62.5
    },
    {
      "date": "2026-04-21",
      "pnl": -125,
      "trades": 5,
      "win_rate": 40
    }
  ]
}
```

#### `/analytics/weekly`
Weekly P&L breakdown.

#### `/analytics/monthly`
Monthly P&L breakdown.

### Analysis Endpoints

#### `/analytics/heatmap`
Strategy × Asset win rate heatmap.

**Response:**
```json
{
  "heatmap": [
    {
      "strategy": "rsi_bounce",
      "pair": "EURUSD",
      "win_rate": 58.5
    },
    {
      "strategy": "rsi_bounce",
      "pair": "XAUUSD",
      "win_rate": 48.2
    }
  ],
  "heatmap_dict": {
    "rsi_bounce": {
      "EURUSD": 58.5,
      "XAUUSD": 48.2
    }
  }
}
```

**Use Cases:**
- Identify which strategy-pair combinations work best
- Avoid combinations with low win rates
- Allocate capital to high-performing combinations
- Detect strategies that are asset-specific

#### `/analytics/correlation`
Pairwise correlation of assets based on P&L patterns.

**Response:**
```json
{
  "correlations": [
    {
      "pair1": "XAUUSD",
      "pair2": "XAGUSD",
      "correlation": 0.78,
      "strength": "high"
    },
    {
      "pair1": "EURUSD",
      "pair2": "GBPUSD",
      "correlation": 0.65,
      "strength": "medium"
    }
  ]
}
```

**Use Cases:**
- Avoid trading highly correlated pairs (redundant exposure)
- Diversify portfolio with uncorrelated pairs
- Detect market regime shifts (correlation changes)

#### `/analytics/dashboard`
Complete dashboard data in one request (combines all endpoints).

**Response:** Aggregates all the above into a single JSON object.

## Database Schema

The analytics module expects the following PostgreSQL tables:

### trades
```sql
CREATE TABLE trades (
  trade_id SERIAL PRIMARY KEY,
  strategy_id INT,
  pair VARCHAR(10),
  timeframe VARCHAR(5),
  entry_time TIMESTAMP,
  exit_time TIMESTAMP,
  entry_price FLOAT,
  exit_price FLOAT,
  lot_size FLOAT,
  stop_loss FLOAT,
  take_profit FLOAT,
  pnl FLOAT,           -- Absolute P&L in USD
  pnl_pct FLOAT,       -- Percentage return
  status VARCHAR(20),  -- OPEN, CLOSED, etc.
  mode VARCHAR(10),    -- PAPER, LIVE
  created_at TIMESTAMP
);
```

### strategies
```sql
CREATE TABLE strategies (
  strategy_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  category VARCHAR(50),
  ...
);
```

## Configuration

### Lookback Period
All endpoints support `lookback_days` query parameter (default 30):
```
GET /api/analytics/summary?lookback_days=90
```

### Risk-Free Rate
Sharpe ratio calculation uses 2% annual risk-free rate (configurable in code).

### Assumptions
- 252 trading days per year (for annualization)
- 10,000 USD starting capital (for ROI calculation)
- Daily returns for Sharpe calculation

## Performance Metrics Explained

### Sharpe Ratio
**Formula:** (Mean Return - Risk-Free Rate) / Volatility × √252

**Interpretation:**
- > 1.0 — Excellent (good return per unit risk)
- 0.5 - 1.0 — Good
- 0 - 0.5 — Poor
- < 0 — Strategy is underwater

**Example:** Sharpe of 1.5 means 1.5% return per 1% of volatility.

### Win Rate
**Formula:** Winning Trades / Total Trades × 100%

**Note:** Win rate ≥50% is not required if risk/reward ratio is good.
- 40% win rate + 3:1 RR = profitable
- 60% win rate + 1:1 RR = also profitable

### Profit Factor
**Formula:** Gross Profit / Gross Loss

**Interpretation:**
- > 1.0 — Profitable
- 1.5+ — Good
- 2.0+ — Excellent
- < 1.0 — Money-losing

### Max Drawdown
**Formula:** (Trough - Peak) / Peak × 100%

**Example:** $10,000 → $9,150 → $11,000 = max drawdown of 8.5%

### Recovery Factor
**Formula:** Net Profit / Max Drawdown

**Interpretation:**
- > 2.0 — Strategy recovers quickly
- > 1.0 — Strategy is recovering
- < 1.0 — Max loss > net profit (risky)

### Risk/Reward Ratio
**Formula:** Average Win Size / Average Loss Size

**Example:** $250 avg win / $100 avg loss = 2.5:1 RR

## Error Handling

If no trades are found for the lookback period, endpoints return:
```json
{
  "error": "No trades found"
}
```

## Logging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tips

- Lookback periods > 365 days may be slow (optimize database indexes)
- Cache results for dashboards (recompute every 5-10 minutes)
- Pre-calculate daily metrics for faster heatmap generation

## Future Enhancements

- [ ] Monte Carlo analysis (trade sequence randomization)
- [ ] Walk-forward analysis (in-sample vs out-of-sample split)
- [ ] Regime detection (bull, bear, sideways markets)
- [ ] Strategy clustering (similar strategies grouped)
- [ ] Performance attribution (what drives returns?)
- [ ] Real-time streaming updates (WebSocket)

---

**Version:** 1.0  
**Last Updated:** April 24, 2026  
**Status:** Production Ready
