# 🚀 GETTING STARTED

Welcome to **TradePanel**, a robust MT5-integrated algorithmic trading platform. This guide will walk you through the setup and initial configuration of your trading environment.

## 🏗️ Setup Flow

```mermaid
graph TD
    A[Start] --> B[Install Python 3.12+]
    B --> C[Install MT5 & Login]
    C --> D[Setup Docker / PostgreSQL]
    D --> E[Create .env File]
    E --> F[Run scripts/setup_all.py]
    F --> G{All Checks Pass?}
    G -- No --> H[Fix Missing Deps/Data]
    H --> F
    G -- Yes --> I[Backtest Strategies]
    I --> J[Run WFO Suite]
    J --> K[Paper Trading Launch]
```

## 📋 Requirements

*   **Python 3.12+**: Ensure Python is in your PATH.
*   **MetaTrader 5**: Installed and logged into an active account (Demo recommended for setup).
*   **PostgreSQL 16**: Recommended via Docker.
*   **Telegram Bot**: Access to a bot token and your Chat ID for notifications.

## 🛠️ Initial Installation

### 1. Repository Preparation
Clone the repository and create your local environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory with the following variables:

```ini
DB_URI=postgresql://postgres:postgres@localhost:5433/trading_platform
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. Automated Setup
Run the unified setup script to initialize the database and verify connectivity:

```powershell
python scripts/setup_all.py
```

## 📈 First Backtest
Verify your installation by running a baseline backtest:

```powershell
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4
```

## 🤖 Operation Modes
*   **Backtesting**: Use `scripts/run_backtest.py` to test strategy logic.
*   **Optimization**: Use `scripts/run_walk_forward.py` or `scripts/run_full_wfo_suite.py`.
*   **Execution**: Use `scripts/run_paper.py` for live/paper trading.

---
*For more technical details, refer to [ARCHITECTURE.md](ARCHITECTURE.md).*
