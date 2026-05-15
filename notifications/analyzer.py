import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from forward_test.signal_checker import SignalChecker
import ta_compat as ta


class MarketAnalyzer:
    def __init__(self):
        self.checker = SignalChecker()
        self.symbols = ["XAUUSD", "EURUSD", "USDJPY", "GBPUSD", "ETHUSD", "BTCUSD"] # Fallback
        
        # Load from config.yaml
        import os, yaml
        from pathlib import Path
        try:
            cfg_path = Path(__file__).parent.parent / "config" / "config.yaml"
            if cfg_path.exists():
                with open(cfg_path) as f:
                    full_cfg = yaml.safe_load(f)
                self.symbols = [p for p, p_def in full_cfg.get("pairs", {}).items() if p_def.get("enabled", True)]
        except Exception:
            pass

    def get_analysis_summary(self):
        """Generates a comprehensive market analysis summary."""
        if not mt5.initialize():
            return "❌ MT5 Connection Failed"

        summary = "📊 <b>Market Analysis Summary</b>\n\n"

        for symbol in self.symbols:
            symbol_summary = self._analyze_symbol(symbol)
            summary += symbol_summary + "\n"

        mt5.shutdown()
        return summary

    # ── Symbol Analysis ───────────────────────────────────────────────────────

    def _analyze_symbol(self, symbol):
        """Analyzes a single symbol across H1, H4, and D1."""
        try:
            df_h1 = self.checker.get_latest_data(symbol, mt5.TIMEFRAME_H1, 100)
            df_h4 = self.checker.get_latest_data(symbol, mt5.TIMEFRAME_H4, 100)
            df_d1 = self.checker.get_latest_data(symbol, mt5.TIMEFRAME_D1, 100)

            if df_h1 is None or df_h4 is None or df_d1 is None:
                return f"<b>{symbol}</b>: Data unavailable"

            lines = [f"<b>{symbol}</b>"]

            # 1. Multi-TF Trend (SMA50 + EMA200)
            lines.append(self._trend_line(df_h1, df_h4, df_d1))

            # 2. MACD Momentum (H4)
            lines.append(self._macd_line(df_h4))

            # 3. ADX Trend Strength (H4)
            lines.append(self._adx_line(df_h4))

            # 4. RSI (H4)
            lines.append(self._rsi_line(df_h4))

            # 5. Bollinger Squeeze (H4)
            squeeze = self._bb_squeeze_line(df_h4)
            if squeeze:
                lines.append(squeeze)

            # 6. ATR Volatility (H4)
            lines.append(self._atr_line(df_h4))

            # 7. Candlestick Patterns (H1 + H4 + D1)
            patterns = self._detect_patterns(df_h1, df_h4, df_d1)
            if patterns:
                lines.append(patterns)
            else:
                lines.append("└ No major patterns")

            return "\n".join(lines)

        except Exception as e:
            return f"<b>{symbol}</b>: Error {e}"

    # ── Trend Analysis ────────────────────────────────────────────────────────

    def _trend_line(self, df_h1, df_h4, df_d1):
        """Multi-TF trend: SMA50 direction + EMA200 bias."""
        def trend_icon(df):
            close = df['close'].iloc[-1]
            sma50 = df['close'].rolling(50).mean().iloc[-1]
            return "🟢▲" if close > sma50 else "🔴▼"

        # EMA200 bias on H4 and D1
        ema200_h4 = ta.ema(df_h4['close'], length=200).iloc[-1]
        ema200_d1 = ta.ema(df_d1['close'], length=200).iloc[-1]
        close_h4 = df_h4['close'].iloc[-1]
        close_d1 = df_d1['close'].iloc[-1]

        h4_above_200 = close_h4 > ema200_h4
        d1_above_200 = close_d1 > ema200_d1

        if h4_above_200 and d1_above_200:
            bias = "🟢 Long bias"
        elif not h4_above_200 and not d1_above_200:
            bias = "🔴 Short bias"
        else:
            bias = "🟡 Mixed"

        return (f"├ Trend: H1({trend_icon(df_h1)}) H4({trend_icon(df_h4)}) "
                f"D1({trend_icon(df_d1)}) | {bias}")

    # ── MACD Momentum ─────────────────────────────────────────────────────────

    def _macd_line(self, df_h4):
        """MACD histogram direction on H4."""
        macd_df = ta.macd(df_h4['close'], fast=12, slow=26, signal=9)
        hist_col = macd_df.columns[1]  # MACDh column
        hist = macd_df[hist_col]

        curr_hist = hist.iloc[-1]
        prev_hist = hist.iloc[-2]

        if curr_hist > 0 and curr_hist > prev_hist:
            momentum = "🟢▲ Bullish accelerating"
        elif curr_hist > 0 and curr_hist <= prev_hist:
            momentum = "🟡▲ Bullish fading"
        elif curr_hist < 0 and curr_hist < prev_hist:
            momentum = "🔴▼ Bearish accelerating"
        elif curr_hist < 0 and curr_hist >= prev_hist:
            momentum = "🟡▼ Bearish fading"
        else:
            momentum = "⚪ Neutral"

        # Check for MACD crossover
        macd_col = macd_df.columns[0]
        sig_col = macd_df.columns[2]
        macd_curr = macd_df[macd_col].iloc[-1]
        macd_prev = macd_df[macd_col].iloc[-2]
        sig_curr = macd_df[sig_col].iloc[-1]
        sig_prev = macd_df[sig_col].iloc[-2]

        cross = ""
        if macd_prev < sig_prev and macd_curr > sig_curr:
            cross = " ⚡ CROSS UP"
        elif macd_prev > sig_prev and macd_curr < sig_curr:
            cross = " ⚡ CROSS DN"

        return f"├ MACD(H4): {momentum}{cross}"

    # ── ADX Trend Strength ────────────────────────────────────────────────────

    def _adx_line(self, df_h4):
        """ADX trend strength on H4."""
        adx_df = ta.adx(df_h4['high'], df_h4['low'], df_h4['close'], length=14)
        adx_val = adx_df.iloc[-1, 0]  # ADX value
        di_plus = adx_df.iloc[-1, 2]  # DI+
        di_minus = adx_df.iloc[-1, 3]  # DI-

        if adx_val >= 40:
            strength = "🔥 Very Strong"
        elif adx_val >= 25:
            strength = "💪 Trending"
        elif adx_val >= 20:
            strength = "〰️ Weak"
        else:
            strength = "📦 Ranging"

        direction = "🟢 DI+" if di_plus > di_minus else "🔴 DI−"
        return f"├ ADX(H4): {adx_val:.0f} {strength} | {direction}"

    # ── RSI ────────────────────────────────────────────────────────────────────

    def _rsi_line(self, df_h4):
        """RSI with divergence hint on H4."""
        rsi = ta.rsi(df_h4['close'], length=14)
        rsi_val = rsi.iloc[-1]

        if rsi_val > 70:
            status = "🔥 Overbought"
        elif rsi_val > 60:
            status = "🟢 Bullish"
        elif rsi_val < 30:
            status = "❄️ Oversold"
        elif rsi_val < 40:
            status = "🔴 Bearish"
        else:
            status = "Neutral"

        # Simple divergence check: price makes higher high but RSI makes lower high
        div = ""
        if len(df_h4) >= 20:
            price_recent_high = df_h4['high'].iloc[-10:].max()
            price_prev_high = df_h4['high'].iloc[-20:-10].max()
            rsi_recent_high = rsi.iloc[-10:].max()
            rsi_prev_high = rsi.iloc[-20:-10].max()

            if price_recent_high > price_prev_high and rsi_recent_high < rsi_prev_high:
                div = " ⚠️ Bear div"
            elif price_recent_high < price_prev_high and rsi_recent_high > rsi_prev_high:
                div = " ⚠️ Bull div"

        return f"├ RSI(H4): {rsi_val:.1f} ({status}){div}"

    # ── Bollinger Squeeze ─────────────────────────────────────────────────────

    def _bb_squeeze_line(self, df_h4):
        """Detect Bollinger Band squeeze — imminent breakout signal."""
        bb_df = ta.bbands(df_h4['close'], length=20, std=2.0)
        upper = bb_df.iloc[:, 2]
        lower = bb_df.iloc[:, 0]
        mid = bb_df.iloc[:, 1]

        # Bandwidth = (upper - lower) / middle
        bandwidth = (upper - lower) / mid.replace(0, np.nan)
        curr_bw = bandwidth.iloc[-1]
        avg_bw = bandwidth.rolling(20).mean().iloc[-1]

        if pd.isna(curr_bw) or pd.isna(avg_bw):
            return None

        ratio = curr_bw / avg_bw if avg_bw > 0 else 1.0

        if ratio < 0.5:
            return "├ BB(H4): 🔶 TIGHT SQUEEZE — breakout imminent"
        elif ratio < 0.75:
            return "├ BB(H4): 🟡 Compression building"
        else:
            return None  # Normal width — not worth reporting

    # ── ATR Volatility ────────────────────────────────────────────────────────

    def _atr_line(self, df_h4):
        """ATR change — volatility expansion or contraction."""
        atr_vals = ta.atr(df_h4['high'], df_h4['low'], df_h4['close'], length=14)
        curr_atr = atr_vals.iloc[-1]
        avg_atr = atr_vals.rolling(20).mean().iloc[-1]

        if pd.isna(avg_atr) or avg_atr == 0:
            return f"├ ATR(H4): {curr_atr:.2f}"

        ratio = curr_atr / avg_atr
        if ratio > 1.5:
            vol = "🔥 High volatility"
        elif ratio > 1.2:
            vol = "📈 Expanding"
        elif ratio < 0.7:
            vol = "📉 Low — consolidation"
        elif ratio < 0.85:
            vol = "〰️ Contracting"
        else:
            vol = "Normal"

        return f"├ Vol(H4): {vol} (ATR {curr_atr:.2f})"

    # ── Candlestick Patterns ──────────────────────────────────────────────────

    def _detect_patterns(self, df_h1, df_h4, df_d1):
        """Detect key candlestick patterns on H1, H4, and D1."""
        found = []

        for tf_name, df in [("H1", df_h1), ("H4", df_h4), ("D1", df_d1)]:
            patterns = self._scan_candles(df)
            for p in patterns:
                found.append(f"{p} ({tf_name})")

        if not found:
            return None

        # Show up to 3 most recent patterns
        display = found[:3]
        extra = f" +{len(found) - 3} more" if len(found) > 3 else ""
        return "└ 🕯 " + " | ".join(display) + extra

    def _scan_candles(self, df):
        """Scan last 3 candles for key patterns."""
        if len(df) < 3:
            return []

        patterns = []
        o, h, l, c = df['open'].values, df['high'].values, df['low'].values, df['close'].values

        # Last candle
        i = -1
        body = abs(c[i] - o[i])
        upper_wick = h[i] - max(o[i], c[i])
        lower_wick = min(o[i], c[i]) - l[i]
        candle_range = h[i] - l[i]

        if candle_range == 0:
            return []

        body_ratio = body / candle_range

        # Hammer / Shooting Star (strong reversal signals)
        if lower_wick > 2 * body and upper_wick < body * 0.5 and body_ratio < 0.35:
            patterns.append("🟢▲ Hammer")
        elif upper_wick > 2 * body and lower_wick < body * 0.5 and body_ratio < 0.35:
            patterns.append("🔴▼ Shooting Star")

        # Pin Bar (long wick rejection)
        if lower_wick > 2.5 * body and c[i] > o[i]:
            patterns.append("🟢▲ Bull Pin Bar")
        elif upper_wick > 2.5 * body and c[i] < o[i]:
            patterns.append("🔴▼ Bear Pin Bar")

        # Doji (indecision)
        if body_ratio < 0.1 and candle_range > 0:
            patterns.append("⚪ Doji")

        # Engulfing (using last 2 candles)
        prev_body = abs(c[-2] - o[-2])
        if (c[i] > o[i] and c[-2] < o[-2] and
                c[i] > o[-2] and o[i] < c[-2] and body > prev_body):
            patterns.append("🟢▲ Bullish Engulfing")
        elif (c[i] < o[i] and c[-2] > o[-2] and
              c[i] < o[-2] and o[i] > c[-2] and body > prev_body):
            patterns.append("🔴▼ Bearish Engulfing")

        # Morning Star / Evening Star (3-candle reversal)
        if len(df) >= 3:
            body_2ago = abs(c[-3] - o[-3])
            body_mid = abs(c[-2] - o[-2])

            # Morning Star: big red → small body → big green
            if (c[-3] < o[-3] and body_2ago > 0 and
                    body_mid < body_2ago * 0.3 and
                    c[i] > o[i] and body > body_2ago * 0.5):
                patterns.append("🟢▲ Morning Star")

            # Evening Star: big green → small body → big red
            if (c[-3] > o[-3] and body_2ago > 0 and
                    body_mid < body_2ago * 0.3 and
                    c[i] < o[i] and body > body_2ago * 0.5):
                patterns.append("🔴▼ Evening Star")

        # Deduplicate (e.g. hammer + pin bar overlap)
        seen = set()
        unique = []
        for p in patterns:
            key = p.split(" ", 1)[1] if " " in p else p
            if key not in seen:
                seen.add(key)
                unique.append(p)

        return unique

    # ── Legacy helper ─────────────────────────────────────────────────────────

    def _calculate_rsi(self, series, period=14):
        """Legacy RSI calculation — kept for backwards compatibility."""
        return ta.rsi(series, length=period)
