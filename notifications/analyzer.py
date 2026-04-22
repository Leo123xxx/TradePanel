import pandas as pd
import MetaTrader5 as mt5
from forward_test.signal_checker import SignalChecker

class MarketAnalyzer:
    def __init__(self):
        self.checker = SignalChecker()
        self.symbols = ["XAUUSD", "EURUSD", "USDJPY", "GBPUSD", "ETHUSD", "BTCUSD"]

    def get_analysis_summary(self):
        """Generates a summary of the market for the top symbols."""
        if not mt5.initialize():
            return "❌ MT5 Connection Failed"

        summary = "📊 <b>Market Analysis Summary</b>\n\n"
        
        for symbol in self.symbols:
            symbol_summary = self._analyze_symbol(symbol)
            summary += symbol_summary + "\n"

        mt5.shutdown()
        return summary

    def _analyze_symbol(self, symbol):
        """Analyzes a single symbol across H1, H4, and D1."""
        try:
            # Fetch data for H1, H4, D1
            df_h1 = self.checker.get_latest_data(symbol, mt5.TIMEFRAME_H1, 100)
            df_h4 = self.checker.get_latest_data(symbol, mt5.TIMEFRAME_H4, 100)
            df_d1 = self.checker.get_latest_data(symbol, mt5.TIMEFRAME_D1, 100)

            if df_h1 is None or df_h4 is None or df_d1 is None:
                return f"<b>{symbol}</b>: Data unavailable"

            # 1. Trend Analysis (Price vs SMA 50)
            trend_h1 = "🐂 Bullish" if df_h1['close'].iloc[-1] > df_h1['close'].rolling(50).mean().iloc[-1] else "🐻 Bearish"
            trend_h4 = "🐂 Bullish" if df_h4['close'].iloc[-1] > df_h4['close'].rolling(50).mean().iloc[-1] else "🐻 Bearish"
            trend_d1 = "🐂 Bullish" if df_d1['close'].iloc[-1] > df_d1['close'].rolling(50).mean().iloc[-1] else "🐻 Bearish"

            # 2. RSI Analysis (H4)
            rsi_h4 = self._calculate_rsi(df_h4['close'], 14).iloc[-1]
            status_h4 = "Normal"
            if rsi_h4 > 70: status_h4 = "🔥 Overbought"
            elif rsi_h4 < 30: status_h4 = "❄️ Oversold"

            # 3. Simple Pattern Check (Engulfing on D1)
            pattern = ""
            last_close = df_d1['close'].iloc[-1]
            last_open = df_d1['open'].iloc[-1]
            prev_close = df_d1['close'].iloc[-2]
            prev_open = df_d1['open'].iloc[-2]

            if last_close > last_open and prev_close < prev_open and last_close > prev_open and last_open < prev_close:
                pattern = "✨ Bullish Engulfing (D1)"
            elif last_close < last_open and prev_close > prev_open and last_close < prev_open and last_open > prev_close:
                pattern = "☄️ Bearish Engulfing (D1)"

            return (
                f"<b>{symbol}</b>\n"
                f"├ Trend: H1({trend_h1}), H4({trend_h4}), D1({trend_d1})\n"
                f"├ RS I(H4): {rsi_h4:.1f} ({status_h4})\n"
                f"{'└ Pattern: ' + pattern if pattern else '└ No major D1 patterns'}"
            )

        except Exception as e:
            return f"<b>{symbol}</b>: Error {e}"

    def _calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
