# Strategy Execution Logic Reference

| Strategy | Symbol | Timeframe | Entry Logic | Exit Logic | Filters | Trade Management |
|----------|--------|-----------|-------------|------------|---------|------------------|
| **RSI Pullback** | XAUUSD, EURUSD | H4 | Price above EMA 200 + RSI < 35 (Long) or Price below EMA 200 + RSI > 65 (Short) | Fixed TP/SL based on ATR mult | ADX > 20 | Partial TP (1:1) + BE |
| **Dual EMA Fractal** | EURUSD, XAUUSD | H1, H4 | Price above EMA 200 + Fractal Breakout (High) or Price below EMA 200 + Fractal Breakout (Low) | ATR-based TP/SL | ADX > 25, RSI Confirmation | Partial TP (1:1) + BE |
| **SuperTrend** | EURUSD | H4 | SuperTrend line flip (Green/Red) | Opposite flip or ATR TP/SL | ADX > 25 | Partial TP + Trailing BE |
| **Gold Breakout** | XAUUSD | H1 | Volatility Squeeze (BB) + Momentum Breakout | High/Low of breakout bar or ATR TP/SL | Volume > 1.2x Avg | Partial TP + BE |
| **Session Momentum** | EURUSD, XAUUSD | H1 | London/NY High/Low Breakout during session overlap | Session end or ATR TP/SL | Time-window (08:00-16:00 UTC) | Partial TP + BE |
| **RSI Bounce** | EURUSD | H1 | RSI Oversold (<30) + Bullish Engulfing or RSI Overbought (>70) + Bearish Engulfing | Mean reversion to EMA 20 | Ranging Market (ADX < 20) | Full TP (No Partials) |
| **MA Crossover** | EURUSD, GBPUSD | H1 | Fast EMA (10) crosses Slow EMA (50) | Reversal Cross or ATR TP/SL | ADX > 20, RSI > 55/45 | Partial TP + BE |

## Implementation Steps for Web UI
1. Create `/api/strategies/logic` endpoint in FastAPI.
2. Return this JSON-formatted table.
3. Update Dashboard frontend to include a "Strategy Logic" tab.
