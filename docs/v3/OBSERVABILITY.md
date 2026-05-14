# TradePanel V3 Observability Master Document

This document outlines the strategy for ingesting logs and metrics into modern observability tools like Prometheus, Grafana, and Loki.

## 1. Log Ingestion (Loki)

TradePanel V3 uses **Structured Logging** (JSON) to facilitate automated ingestion.

### Log Format
Logs are written to `logs/*.json.log` in the following format:
```json
{"timestamp": "2026-05-11T18:16:10Z", "level": "INFO", "service": "backtest", "message": "Optimization complete", "metrics": {"win_rate": 0.65, "profit_factor": 1.5}}
```

### Ingestion Pipeline
1.  **Promtail**: A Promtail instance runs on the host machine, watching the `logs/` directory.
2.  **Loki**: Promtail pushes logs to a centralized Loki instance.
3.  **Grafana**: Logs are queried via the Loki datasource for real-time log tailing and error alerting.

## 2. Metrics Collection (Prometheus)

We use the `prometheus_client` library to expose a `/metrics` endpoint on the core services.

### Key Metrics Tracked
| Metric Name | Type | Description |
| :--- | :--- | :--- |
| `tradepanel_trade_count_total` | Counter | Total number of trades executed. |
| `tradepanel_pnl_current` | Gauge | Current account equity. |
| `tradepanel_latency_ms` | Histogram | Latency between signal generation and MT5 execution. |
| `tradepanel_backtest_duration_seconds` | Summary | Time taken for a backtest run. |

### Scraping Configuration
Add the following to your `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'tradepanel'
    static_configs:
      - targets: ['localhost:8000'] # Backend API
```

## 3. Visualization (Grafana)

A pre-built Grafana dashboard is available in `docs/v3/assets/dashboard.json`.

### Features
*   **Real-time Equity Curve**: Live balance/equity tracking.
*   **Strategy Heatmap**: Visualizing win rates across different pairs and timeframes.
*   **System Health**: CPU/RAM usage of TradePanel containers.
*   **Alerting**: Configured to send alerts to the Telegram bot if:
    *   Drawdown exceeds 10%.
    *   MT5 connection is lost for > 60 seconds.

## 4. Troubleshooting
If metrics are not appearing:
1.  Check if `scripts/core/dashboard_api.py` is running and accessible at port 8000.
2.  Verify `logs/bridge_stdout.log` for any "Loki push failed" errors.
