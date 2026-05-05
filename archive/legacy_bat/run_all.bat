@echo off
set PYTHONIOENCODING=utf-8
python scripts/run_backtest.py --strategy ma_crossover --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy range_breakout --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy rsi_pullback --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy bb_mean_reversion --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy swing_pullback --pair XAUUSD --timeframe H4
python scripts/run_backtest.py --strategy session_momentum --pair XAUUSD --timeframe H1
python scripts/run_backtest.py --strategy stoch_divergence --pair XAUUSD --timeframe H4
