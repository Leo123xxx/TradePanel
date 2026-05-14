# 🚀 OPTIMIZATION & AUTOMATION ROADMAP

This document outlines the high-priority enhancements for the next major update of the **TradePanel** platform.

## 🎯 Phase 4: Full Automation

### 1. ⚡ Auto-Tiering & Parameter Sync
Currently, WFO results must be manually transferred to `strategies.yaml`.
*   **Goal**: Create a service that runs WFO weekly and automatically updates the strategy registry with the most robust parameters.
*   **Automation**: `scripts/auto_optimize.py` running via GitHub Actions or locally as a Cron job.

### 2. ⚖️ Adaptive Risk Management (Kelly Criterion)
Trade sizing is currently fixed at a percentage of equity.
*   **Goal**: Integrate the Kelly Criterion to dynamically adjust position size based on the individual strategy's historical win rate and payoff ratio.
*   **Benefit**: Maximizes geometric growth while minimizing risk of ruin.

### 📊 Phase 5: Advanced Analytics

### 3. 🕸️ Correlation Matrix Engine
*   **Goal**: Real-time monitoring of strategy correlations to prevent "cluster trades" (e.g., 5 different strategies all going long on XAUUSD simultaneously).
*   **Logic**: If correlation > 0.8, the system will only allow the signal with the highest "Optimization Score" to execute.

### 4. 🗄️ HFT Data Resampling
*   **Goal**: Efficiently handle M1 data for H1/H4 strategies to reduce DB query latency.
*   **Architecture**: Aggregation of M1 bars into a specialized `ohlc_high_res` table for faster signal generation.

## 🛠️ Infrastructure Improvements

### 5. CI/CD for Algorithmic Trading
*   **Goal**: Automated backtesting of the entire strategy library on every Git push.
*   **Check**: If any Tier 1 strategy PF drops < 1.0 on most recent data, the build "fails" and alerts the developer.

---
*Back to [GETTING_STARTED.md](GETTING_STARTED.md).*
