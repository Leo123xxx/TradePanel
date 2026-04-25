# Analytics Dashboard - Frontend Implementation Guide

This guide shows how to consume the analytics API endpoints to build a comprehensive dashboard.

## Architecture Overview

```
Database (PostgreSQL)
    ↓
PerformanceCalculator (Python)
    ↓
FastAPI Endpoints (/api/analytics/*)
    ↓
Frontend (React/Vue/HTML)
    ↓
Dashboard Visualizations
```

## Dashboard Layout Recommendation

### 1. Summary Card (Top-Left)
Displays key account metrics at a glance.

**Endpoint:** `GET /api/analytics/summary?lookback_days=30`

**Display:**
```
┌─────────────────────────────┐
│  Account Summary (30 days)  │
├─────────────────────────────┤
│  Total Trades:    125       │
│  Win Rate:        54.4%     │
│  Profit Factor:   1.85      │
│  Sharpe Ratio:    1.42      │
│  Max Drawdown:    8.5%      │
│  Net Profit:      $2,350    │
│  ROI:             23.5%     │
└─────────────────────────────┘
```

### 2. Performance Trend Chart (Top-Right)
Shows P&L evolution over time.

**Endpoint:** `GET /api/analytics/daily?lookback_days=30`

**Chart Type:** Line Chart
- X-axis: Date
- Y-axis: Cumulative P&L ($)
- Color: Green if profit, Red if loss

**Example:**
```
Daily P&L
         │                    ╱╲
   2000  ├─────────────────╱──┤─╲
   1500  │                ╱    │  ╲
   1000  │              ╱      │   ╲
    500  │            ╱        │    ╲
      0  ├──────────╱──────────┤─────╲──
   -500  │                     │      ╲
        └──────────────────────┴──────────
         Apr 1  Apr 10  Apr 20  Apr 30
```

### 3. Strategy Performance Table (Middle-Left)
Breakdown by strategy.

**Endpoint:** `GET /api/analytics/by-strategy?lookback_days=30`

**Table Columns:**
| Strategy | Trades | WR% | PF | Sharpe | Profit |
|----------|--------|-----|----|----|--------|
| rsi_bounce | 45 | 52% | 1.6 | 1.2 | $850 |
| dual_ema_fractal | 32 | 56% | 1.9 | 1.5 | $680 |
| bb_squeeze | 28 | 50% | 1.5 | 0.8 | $520 |
| fast_ma_scalper | 20 | 55% | 1.8 | 1.1 | $300 |

**Sorting:** Click column headers to sort (WR%, PF, Sharpe, Profit)

### 4. Asset Performance Table (Middle-Right)
Breakdown by trading pair.

**Endpoint:** `GET /api/analytics/by-asset?lookback_days=30`

**Table Columns:**
| Pair | Trades | WR% | PF | Sharpe | Profit |
|------|--------|-----|----|----|--------|
| EURUSD | 50 | 56% | 1.9 | 1.4 | $1,200 |
| XAUUSD | 40 | 48% | 1.6 | 1.1 | $680 |
| GBPUSD | 25 | 60% | 2.1 | 1.6 | $520 |
| XAGUSD | 10 | 40% | 1.2 | 0.5 | $-50 |

### 5. Win Rate Heatmap (Bottom-Left)
Strategy × Asset performance matrix.

**Endpoint:** `GET /api/analytics/heatmap?lookback_days=30`

**Visualization:**
```
                EURUSD  XAUUSD  GBPUSD  XAGUSD  BTCUSD
RSI Bounce        58%     48%     62%     40%     35%
Dual EMA          60%     52%     55%     45%     42%
BB Squeeze        50%     55%     48%     42%     38%
Fast MA Scalper   62%     50%     58%     52%     45%

Color Scale:
  ████ High (60%+)
  ███  Good (50-60%)
  ██   Fair (40-50%)
  █    Poor (<40%)
```

**Interaction:** 
- Hover over cells to see exact % and trade count
- Click cells to filter trades by strategy + pair

### 6. Correlation Analysis (Bottom-Right)
Pair correlation and diversification metrics.

**Endpoint:** `GET /api/analytics/correlation?lookback_days=30`

**Display:**
```
Pair Correlations

XAUUSD ↔ XAGUSD: 0.78 (HIGH)
  → Gold & Silver move together (expected)
  → Avoid running same strategy on both

EURUSD ↔ GBPUSD: 0.65 (MEDIUM)
  → EUR/GBP linked, but decent diversification
  → Safe to run on both

EURUSD ↔ XAUUSD: 0.12 (LOW)
  → Uncorrelated, excellent diversification
  → Ideal for portfolio construction

Correlation Risk:
  High-correlation pairs: ⚠ 3 detected
  Recommendation: Diversify with uncorrelated assets
```

## Sample Frontend Code

### React Example

```javascript
import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, HeatMapChart } from 'recharts';

function AnalyticsDashboard() {
  const [summary, setSummary] = useState(null);
  const [byStrategy, setByStrategy] = useState({});
  const [byAsset, setByAsset] = useState({});
  const [daily, setDaily] = useState([]);
  const [heatmap, setHeatmap] = useState([]);
  const [lookback, setLookback] = useState(30);

  useEffect(() => {
    // Fetch all data
    const fetchData = async () => {
      const baseUrl = '/api/analytics';
      const params = `?lookback_days=${lookback}`;

      try {
        const [summaryRes, stratRes, assetRes, dailyRes, heatRes] = 
          await Promise.all([
            fetch(`${baseUrl}/summary${params}`),
            fetch(`${baseUrl}/by-strategy${params}`),
            fetch(`${baseUrl}/by-asset${params}`),
            fetch(`${baseUrl}/daily${params}`),
            fetch(`${baseUrl}/heatmap${params}`)
          ]);

        setSummary(await summaryRes.json());
        setByStrategy(await stratRes.json());
        setByAsset(await assetRes.json());
        setDaily(await dailyRes.json());
        setHeatmap(await heatRes.json());
      } catch (error) {
        console.error('Error fetching analytics:', error);
      }
    };

    fetchData();
  }, [lookback]);

  if (!summary) return <div>Loading...</div>;

  return (
    <div className="analytics-dashboard">
      {/* Lookback Period Selector */}
      <div className="controls">
        <label>Analysis Period:</label>
        <select value={lookback} onChange={(e) => setLookback(parseInt(e.target.value))}>
          <option value={7}>Last 7 Days</option>
          <option value={30}>Last 30 Days</option>
          <option value={90}>Last 90 Days</option>
          <option value={365}>Last Year</option>
        </select>
      </div>

      {/* Summary Card */}
      <div className="summary-card">
        <h2>Account Summary</h2>
        <div className="metrics-grid">
          <div className="metric">
            <label>Total Trades</label>
            <value>{summary.account_summary.total_trades}</value>
          </div>
          <div className="metric">
            <label>Win Rate</label>
            <value className={summary.account_summary.win_rate >= 50 ? 'positive' : 'negative'}>
              {summary.account_summary.win_rate.toFixed(1)}%
            </value>
          </div>
          <div className="metric">
            <label>Profit Factor</label>
            <value className={summary.account_summary.profit_factor > 1.5 ? 'positive' : 'warning'}>
              {summary.account_summary.profit_factor.toFixed(2)}
            </value>
          </div>
          <div className="metric">
            <label>Sharpe Ratio</label>
            <value className={summary.account_summary.sharpe_ratio > 1.0 ? 'positive' : 'warning'}>
              {summary.account_summary.sharpe_ratio.toFixed(2)}
            </value>
          </div>
          <div className="metric">
            <label>Max Drawdown</label>
            <value className="warning">
              {summary.account_summary.max_drawdown_pct.toFixed(2)}%
            </value>
          </div>
          <div className="metric">
            <label>Net Profit</label>
            <value className={summary.account_summary.net_profit > 0 ? 'positive' : 'negative'}>
              ${summary.account_summary.net_profit.toLocaleString('en-US', {maximumFractionDigits: 0})}
            </value>
          </div>
        </div>
      </div>

      {/* Daily P&L Chart */}
      <div className="chart-container">
        <h3>Daily P&L</h3>
        <LineChart width={500} height={300} data={daily.daily}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="pnl" stroke="#82ca9d" />
        </LineChart>
      </div>

      {/* Strategy Table */}
      <div className="table-container">
        <h3>Performance by Strategy</h3>
        <table>
          <thead>
            <tr>
              <th>Strategy</th>
              <th>Trades</th>
              <th>WR%</th>
              <th>PF</th>
              <th>Sharpe</th>
              <th>Profit</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(byStrategy.strategies).map(([name, metrics]) => (
              <tr key={name}>
                <td>{name}</td>
                <td>{metrics.total_trades}</td>
                <td>{metrics.win_rate.toFixed(1)}%</td>
                <td>{metrics.profit_factor.toFixed(2)}</td>
                <td>{metrics.sharpe_ratio.toFixed(2)}</td>
                <td className={metrics.net_profit > 0 ? 'positive' : 'negative'}>
                  ${metrics.net_profit.toFixed(0)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Heatmap */}
      <div className="heatmap-container">
        <h3>Win Rate Heatmap (Strategy × Asset)</h3>
        <HeatmapVisualization data={heatmap.heatmap_dict} />
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
```

### HTML Example

```html
<!DOCTYPE html>
<html>
<head>
  <title>TradePanel Analytics</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    .summary-card {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin: 20px;
    }
    .metric {
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
      text-align: center;
    }
    .metric label { display: block; font-size: 12px; color: #666; }
    .metric value { display: block; font-size: 24px; font-weight: bold; }
    .positive { color: green; }
    .negative { color: red; }
  </style>
</head>
<body>
  <h1>TradePanel Analytics Dashboard</h1>
  
  <div id="summary"></div>
  <div id="chart"></div>
  
  <script>
    async function loadDashboard() {
      // Fetch summary
      const res = await fetch('/api/analytics/summary?lookback_days=30');
      const data = await res.json();
      
      // Display summary
      const summary = data.account_summary;
      document.getElementById('summary').innerHTML = `
        <div class="summary-card">
          <div class="metric">
            <label>Trades</label>
            <value>${summary.total_trades}</value>
          </div>
          <div class="metric">
            <label>Win Rate</label>
            <value>${summary.win_rate.toFixed(1)}%</value>
          </div>
          <div class="metric">
            <label>Profit Factor</label>
            <value>${summary.profit_factor.toFixed(2)}</value>
          </div>
          <div class="metric">
            <label>Sharpe</label>
            <value>${summary.sharpe_ratio.toFixed(2)}</value>
          </div>
          <div class="metric">
            <label>Max DD</label>
            <value>${summary.max_drawdown_pct.toFixed(2)}%</value>
          </div>
          <div class="metric">
            <label>Profit</label>
            <value>$${summary.net_profit.toLocaleString()}</value>
          </div>
        </div>
      `;
    }
    
    loadDashboard();
  </script>
</body>
</html>
```

## API Response Flow

### Request Flow:
```
User Action (e.g., select lookback period)
    ↓
Frontend JS fetches /api/analytics/{endpoint}?lookback_days=X
    ↓
Router receives request
    ↓
PerformanceCalculator.calculate_all_metrics()
    ↓
Queries database for trades
    ↓
Calculates metrics
    ↓
Returns JSON
    ↓
Frontend renders visualization
```

### Performance Optimization:

For real-time dashboards, consider:

1. **Caching** (5-10 minute TTL):
   ```python
   from functools import lru_cache
   from datetime import timedelta
   
   @lru_cache(maxsize=10)
   def get_cached_metrics(lookback_days: int):
       return PerformanceCalculator(lookback_days).calculate_all_metrics()
   ```

2. **Background Computation**:
   - Pre-calculate metrics every 5 minutes
   - Store in Redis
   - Serve from cache

3. **Database Indexing**:
   ```sql
   CREATE INDEX idx_trades_exit_time ON trades(exit_time);
   CREATE INDEX idx_trades_strategy ON trades(strategy_id);
   CREATE INDEX idx_trades_pair ON trades(pair);
   ```

## Real-Time Updates (WebSocket)

For live dashboards, stream updates:

```python
from fastapi import WebSocket

@app.websocket("/ws/analytics")
async def websocket_analytics(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        # Recalculate every 30 seconds
        await asyncio.sleep(30)
        metrics = calculator.calculate_all_metrics()
        await websocket.send_json({
            "type": "metrics_update",
            "data": metrics
        })
```

Frontend receives live updates:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analytics');
ws.onmessage = (event) => {
  const { data } = JSON.parse(event.data);
  updateDashboard(data);
};
```

---

**Dashboard Version:** 1.0  
**Last Updated:** April 24, 2026
