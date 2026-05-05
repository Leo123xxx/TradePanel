python scripts/setup_wf_db.py
python -c "from data.db_client import DBClient; db=DBClient(); db.execute_query('DELETE FROM walk_forward_results')"
python -m scripts.run_walk_forward --strategy range_breakout --pair XAUUSD --timeframe H4 >> wf_output.txt 2>&1
python -m scripts.run_walk_forward --strategy rsi_pullback --pair XAUUSD --timeframe H4 >> wf_output.txt 2>&1
python -m scripts.run_walk_forward --strategy swing_pullback --pair XAUUSD --timeframe H4 >> wf_output.txt 2>&1
python -m scripts.run_walk_forward --strategy stoch_divergence --pair XAUUSD --timeframe H4 >> wf_output.txt 2>&1
python -m scripts.run_walk_forward --strategy ma_crossover --pair XAUUSD --timeframe H1 >> wf_output.txt 2>&1
python -m scripts.run_walk_forward --strategy bb_mean_reversion --pair XAUUSD --timeframe H1 >> wf_output.txt 2>&1
python -m scripts.run_walk_forward --strategy session_momentum --pair XAUUSD --timeframe H1 >> wf_output.txt 2>&1
echo Done > wf_done.txt
