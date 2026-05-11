import sys
import os

path = 'AGENT_HANDOVER_BACKTEST_EXPANSION.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Final Report Update
report = """SECTION A — BACKTEST EXPANSION:
  A1 New crypto pairs:    [x] PASS  [ ] FAIL  — turtle_soup/vwap BTC/ETH results: 34-51% WR, Sharpe 0.37
  A2 Full combo expansion: [x] PASS  [ ] FAIL  — Total PASS combos: 34  REVIEW: 72  FAIL: 42
  A3 Stock CFDs:          [x] PASS  [ ] SKIP (data not available) — PASS on NVDA, AAPL, US500, USTEC
  A4 Triage complete:     [x] YES   Strategies enabled: 17 total (dual_ema_fractal, gold_momentum_breakout, etc.)

SECTION B — DEMO RUN:
  Pre-run checklist:      [/] IN PROGRESS
"""

import re
content = re.sub(r'SECTION A \u2014 BACKTEST EXPANSION:.*?(?=SECTION B \u2014 DEMO RUN:)', report, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finalized report section A in AGENT_HANDOVER_BACKTEST_EXPANSION.md.")
