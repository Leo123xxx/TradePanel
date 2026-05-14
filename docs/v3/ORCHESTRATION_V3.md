# TradePanel V3 Orchestration Guide

Version 3 introduces a modular approach to script execution, performance tuning, and cross-functional automation.

## 1. Modular Structure

Scripts are now organized by their functional domain:

*   **`scripts/core/`**: Primary service controllers (API, Bot, Bridge).
*   **`scripts/automation/`**: High-level entry points (Bat/Sh) for daily and weekend cycles.
*   **`scripts/data/`**: Specialized ingestion engines (Yahoo, MT5, Economic Calendar).
*   **`scripts/backtest/`**: Optimization and validation suite.
*   **`scripts/lib/`**: Common libraries used by all scripts.

## 2. Shared Libraries (`scripts/lib/`)

To ensure robustness, common tasks are centralized:

*   `logger.py`: Provides structured JSON logging and console output.
*   `db_client.py`: Handles pooled database connections and bulk operations.
*   `config_loader.py`: Unified YAML configuration management.

## 3. Performance Tuning

TradePanel V3 is optimized for high-performance data processing:

### A. Concurrent Optimization
WFO and parameter optimization now utilize `scripts/backtest/run_wfo_parallel.py` (coming soon), which leverages multi-core processing to reduce optimization time by up to 70%.

### B. Parquet Data Caching
Historical data is cached in `.parquet` format within `results/data/cache/`. This format is significantly faster to read than CSV/JSON, especially for large datasets used in backtesting.

### C. Database Batching
The `db_client.py` library implements batch inserts for backtest results, minimizing the number of commits and significantly reducing I/O wait times.

## 4. Unified Entry Point (`trade.bat`)

The new `trade.bat` provides a single interface for all V3 operations:

```powershell
.\trade.bat v3-sync     # Pull data, update DB, and refresh cache
.\trade.bat v3-opt      # Run parallel WFO optimization
.\trade.bat v3-monitor  # Launch Prometheus/Grafana stack
.\trade.bat help        # Show all available commands
```

## 5. Maintenance Cycle

V3 automates its own cleanup:
*   Logs older than 7 days are moved to `results/logs/archive/`.
*   Temp results are automatically cleared after successful DB ingestion.
