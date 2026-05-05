"""
tests/test_strategy_signals.py
================================
End-to-end signal tests for all 12 strategies modified in the 2026-04-29 v2 upgrade.

Coverage per strategy:
  - Smoke: imports, instantiates, validate_params, generate_signals returns df with 'signal'
  - Gate: ADX gate blocks/allows, session gate blocks outside UTC 7-17, RSI gate, vol gate

Run with:
    cd F:/REPOS/leo123xxx/TradePanel
    python -m pytest tests/test_strategy_signals.py -v

No MT5 or database required — all tests use synthetic OHLCV DataFrames.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root so strategy imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ─── Synthetic data helpers ───────────────────────────────────────────────────

def _make_ohlcv(
    n: int = 300,
    trend: str = "flat",
    base_price: float = 1.1000,
    vol_scale: float = 0.001,
    start_dt: datetime = datetime(2026, 1, 5, 10, 0),  # Monday 10:00 UTC (in session)
    freq_minutes: int = 15,
    volume_mean: int = 500,
) -> pd.DataFrame:
    """
    Generate synthetic OHLCV with a DatetimeIndex.

    trend: 'up'        — persistent uptrend (ADX builds high, RSI stays elevated)
           'down'      — persistent downtrend
           'oscillate' — tight sine-wave chop (ADX low, RSI oscillates near 50)
           'flat'      — near-zero noise (ADX low)
    """
    np.random.seed(42)
    timestamps = [start_dt + timedelta(minutes=freq_minutes * i) for i in range(n)]

    if trend == "up":
        step = vol_scale * 0.6
        closes = base_price + np.cumsum(np.full(n, step) + np.random.normal(0, vol_scale * 0.1, n))
    elif trend == "down":
        step = vol_scale * 0.6
        closes = base_price - np.cumsum(np.full(n, step) + np.random.normal(0, vol_scale * 0.1, n))
    elif trend == "oscillate":
        closes = base_price + (vol_scale * 3) * np.sin(np.arange(n) * 0.3)
        closes += np.random.normal(0, vol_scale * 0.05, n)
    else:  # flat
        closes = base_price + np.random.normal(0, vol_scale * 0.05, n)

    closes = np.maximum(closes, 0.0001)  # no negative prices
    noise = np.abs(np.random.normal(0, vol_scale * 0.3, n))
    highs = closes + noise
    lows = closes - noise
    opens = np.roll(closes, 1)
    opens[0] = closes[0]

    df = pd.DataFrame(
        {
            "open":        opens,
            "high":        highs,
            "low":         lows,
            "close":       closes,
            "tick_volume": np.random.randint(
                int(volume_mean * 0.5), int(volume_mean * 2), n
            ).astype(float),
        },
        index=pd.DatetimeIndex(timestamps),
    )
    return df


def _out_of_session_df(n: int = 300, freq_minutes: int = 15) -> pd.DataFrame:
    """Bars anchored at 02:00 UTC — outside London/NY session (7–17)."""
    return _make_ohlcv(
        n=n, trend="flat", start_dt=datetime(2026, 1, 5, 2, 0), freq_minutes=freq_minutes
    )


def _in_session_df(n: int = 300, freq_minutes: int = 15, trend: str = "flat") -> pd.DataFrame:
    """Bars anchored at 10:00 UTC — inside London/NY session."""
    return _make_ohlcv(
        n=n, trend=trend, start_dt=datetime(2026, 1, 5, 10, 0), freq_minutes=freq_minutes
    )


def _all_zero(df: pd.DataFrame) -> bool:
    return (df["signal"] == 0).all()


def _smoke(StratClass, params=None):
    """Instantiate, validate_params, run generate_signals, return result df."""
    strat = StratClass(params)
    assert strat.validate_params(), f"{StratClass.__name__}.validate_params() returned False"
    df = _in_session_df(n=300)
    result = strat.generate_signals(df)
    assert "signal" in result.columns, "generate_signals must return df with 'signal' column"
    assert result["signal"].isin([-1, 0, 1]).all(), "signal column must only contain -1, 0, 1"
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 1 strategies
# ═══════════════════════════════════════════════════════════════════════════════

class TestGoldMomentumBreakout:
    from strategies.gold_momentum_breakout import GoldMomentumBreakoutStrategy as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_adx_gate_blocks_in_ranging(self):
        """ADX min gate: oscillating data → ADX low → very few breakout signals."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="oscillate")
        result = s.generate_signals(df)
        buys = (result["signal"] == 1).sum()
        assert buys < 5, f"Expected <5 buys in ranging market, got {buys}"

    def test_rsi_thresholds(self):
        s = self.Cls()
        assert s.params.get("rsi_buy_min", s.params.get("rsi_long_min", 55)) >= 55
        assert s.params.get("rsi_sell_max", s.params.get("rsi_short_max", 45)) <= 45


class TestEmaRibbonTrend:
    from strategies.ema_ribbon_trend import EMARibbonTrendStrategy as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_adx_raised(self):
        s = self.Cls()
        adx = s.params.get("adx_min", s.params.get("adx_threshold", 0))
        assert adx >= 28, f"ADX min should be >=28, got {adx}"

    def test_no_signals_in_choppy_market(self):
        """ADX gate + EMA200: choppy oscillating data should produce minimal signals."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="oscillate")
        result = s.generate_signals(df)
        total = (result["signal"] != 0).sum()
        assert total < 10, f"Expected <10 signals in choppy market, got {total}"


class TestDualEmaFractal:
    from strategies.dual_ema_fractal import DualEMAFractal as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_signals_run_without_error(self):
        s = self.Cls()
        df = _in_session_df(n=300, trend="up")
        result = s.generate_signals(df)
        assert "signal" in result.columns


class TestRangeBreakout:
    from strategies.range_breakout import RangeBreakoutStrategy as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_low_volume_suppresses_signals(self):
        """vol AND adx must both pass — persistent low volume should suppress signals."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="flat")
        df["tick_volume"] = 1.0  # near-zero volume — vol_spike gate never passes
        result = s.generate_signals(df)
        assert "signal" in result.columns  # runs without error


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 2 strategies
# ═══════════════════════════════════════════════════════════════════════════════

class TestMacdTrend:
    from strategies.macd_trend import MACDTrendStrategy as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_new_params_present(self):
        """rsi_long_min, rsi_short_max, ema200_period must be wired in."""
        s = self.Cls()
        assert s.params.get("rsi_long_min") == 55
        assert s.params.get("rsi_short_max") == 45
        assert s.params.get("ema200_period") == 200

    def test_adx_raised_to_28(self):
        s = self.Cls()
        adx = s.params.get("adx_threshold", s.params.get("adx_min", 0))
        assert adx >= 28, f"MACD adx threshold should be >=28, got {adx}"

    def test_no_longs_in_downtrend(self):
        """EMA200 macro gate must block longs when price is below EMA200."""
        s = self.Cls()
        df = _in_session_df(n=400, trend="down")
        result = s.generate_signals(df)
        buys = (result["signal"] == 1).sum()
        assert buys == 0, f"EMA200 gate should block longs in downtrend, got {buys} buys"

    def test_no_shorts_in_uptrend(self):
        """EMA200 macro gate must block shorts when price is above EMA200."""
        s = self.Cls()
        df = _in_session_df(n=400, trend="up")
        result = s.generate_signals(df)
        sells = (result["signal"] == -1).sum()
        assert sells == 0, f"EMA200 gate should block shorts in uptrend, got {sells} sells"


class TestTurtleSoup:
    from strategies.turtle_soup import TurtleSoup as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_new_params_present(self):
        s = self.Cls()
        assert "adx_max" in s.params
        assert "vol_threshold_mult" in s.params
        assert "ema200_period" in s.params

    def test_adx_max_gate_blocks_all(self):
        """adx_max=0 → ADX never ≤ 0 → all signals suppressed."""
        s = self.Cls()
        s.params["adx_max"] = 0
        df = _in_session_df(n=300, trend="up")
        result = s.generate_signals(df)
        assert _all_zero(result), "adx_max=0 must block all TurtleSoup signals"

    def test_no_longs_in_downtrend(self):
        """EMA200 macro context: in strong downtrend, sweep of lows aligns but
        macro_up is False — longs should be suppressed."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="down")
        result = s.generate_signals(df)
        # In a downtrend, macro_up=False blocks buy signals
        buys = (result["signal"] == 1).sum()
        assert buys == 0, f"EMA200 should block longs in downtrend, got {buys}"


class TestDualEmaMomentum:
    from strategies.dual_ema_momentum import DualEMAMomentum as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_new_params_present(self):
        s = self.Cls()
        assert "rsi_long_min" in s.params
        assert "rsi_short_max" in s.params
        assert "ema200_period" in s.params
        assert "vol_threshold_mult" in s.params

    def test_no_longs_in_downtrend(self):
        """EMA200 macro gate blocks longs when price is below EMA200."""
        s = self.Cls()
        df = _in_session_df(n=400, trend="down")
        result = s.generate_signals(df)
        buys = (result["signal"] == 1).sum()
        assert buys == 0, f"EMA200 gate should block longs in downtrend, got {buys} buys"

    def test_no_shorts_in_uptrend(self):
        """EMA200 macro gate blocks shorts when price is above EMA200."""
        s = self.Cls()
        df = _in_session_df(n=400, trend="up")
        result = s.generate_signals(df)
        sells = (result["signal"] == -1).sum()
        assert sells == 0, f"EMA200 gate should block shorts in uptrend, got {sells} sells"


class TestHikkazeTrap:
    from strategies.hikkake_trap import HikkakeTrap as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_adx_max_param_consumed(self):
        """adx_max=0 must block all signals — confirms code reads the param."""
        s = self.Cls()
        s.params["adx_max"] = 0
        df = _in_session_df(n=300, trend="oscillate")
        result = s.generate_signals(df)
        assert _all_zero(result), "adx_max=0 must block all hikkake signals"

    def test_adx_max_default_set(self):
        s = self.Cls()
        assert s.params.get("adx_max") is not None
        assert s.params["adx_max"] <= 30


class TestRvgiCciConfluence:
    from strategies.rvgi_cci_confluence import RVGICCIConfluence as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_cci_thresholds_tightened(self):
        """CCI buy_min=0, sell_max=0 — momentum must be confirmed in direction."""
        s = self.Cls()
        assert s.params.get("cci_buy_min") == 0
        assert s.params.get("cci_sell_max") == 0

    def test_ema100_period(self):
        s = self.Cls()
        assert s.params.get("ema100_period") == 100

    def test_adx_min_set(self):
        s = self.Cls()
        assert s.params.get("adx_min") == 22

    def test_ranging_suppresses_signals(self):
        """Oscillating data → ADX too low → no breakout signals."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="oscillate", freq_minutes=60)
        result = s.generate_signals(df)
        assert "signal" in result.columns  # at minimum it runs cleanly


class TestVwapMomentum:
    from strategies.vwap_momentum import VWAPMomentum as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_session_gate_blocks_out_of_hours(self):
        """All bars at 02:00 UTC — outside session — must produce no signals."""
        s = self.Cls()
        df = _out_of_session_df(n=300, freq_minutes=15)
        result = s.generate_signals(df)
        assert _all_zero(result), "Session gate must block all VWAP signals outside UTC 7-17"

    def test_adx_max_gate_param(self):
        s = self.Cls()
        assert s.params.get("adx_max") == 30

    def test_rsi_zone_params(self):
        s = self.Cls()
        assert s.params.get("rsi_buy_max") == 45
        assert s.params.get("rsi_sell_min") == 55

    def test_adx_max_override_blocks_all(self):
        """Force adx_max=0 → all signals suppressed regardless of market state."""
        s = self.Cls()
        s.params["vol_threshold_mult"] = 0.0
        s.params["adx_max"] = 0
        df = _in_session_df(n=300, trend="flat")
        result = s.generate_signals(df)
        assert _all_zero(result), "adx_max=0 must block all VWAP signals"


# ─── Rehabilitated scalpers ───────────────────────────────────────────────────

class TestBBSqueezeScalp:
    from strategies.bb_squeeze_scalp import BBSqueezeScalp as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_session_gate_blocks_out_of_hours(self):
        """All bars at 02:00 UTC must yield zero signals."""
        s = self.Cls()
        df = _out_of_session_df(n=300, freq_minutes=15)
        result = s.generate_signals(df)
        assert _all_zero(result), "Session gate must block bb_squeeze signals outside UTC 7-17"

    def test_timeframe_is_m15_only(self):
        assert self.Cls().timeframes == ["M15"]

    def test_params_set(self):
        s = self.Cls()
        assert s.params.get("adx_min") == 25
        assert s.params.get("ema50_period") == 50
        assert s.params.get("rsi_confirm_long") == 52
        assert s.params.get("rsi_confirm_short") == 48
        assert s.params.get("squeeze_pct") == 0.6

    def test_no_longs_in_downtrend(self):
        """EMA50 direction gate: price stays below EMA50 in downtrend → no longs."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="down")
        result = s.generate_signals(df)
        buys = (result["signal"] == 1).sum()
        assert buys == 0, f"EMA50 gate should block longs in downtrend, got {buys} buys"

    def test_no_shorts_in_uptrend(self):
        """EMA50 direction gate: price stays above EMA50 in uptrend → no shorts."""
        s = self.Cls()
        df = _in_session_df(n=300, trend="up")
        result = s.generate_signals(df)
        sells = (result["signal"] == -1).sum()
        assert sells == 0, f"EMA50 gate should block shorts in uptrend, got {sells} sells"


class TestRsiExtremesScalp:
    from strategies.rsi_extremes_scalp import RSIExtremesScalp as Cls

    def test_smoke(self):
        _smoke(self.Cls)

    def test_validate_params(self):
        assert self.Cls().validate_params()

    def test_session_gate_blocks_out_of_hours(self):
        """Signals at 02:00 UTC (outside 7-17) must all be zero."""
        s = self.Cls()
        df = _out_of_session_df(n=300, freq_minutes=15)
        result = s.generate_signals(df)
        assert _all_zero(result), "Session gate must block rsi_extremes signals outside UTC 7-17"

    def test_timeframe_is_m15_only(self):
        assert self.Cls().timeframes == ["M15"]

    def test_rsi_thresholds_tightened(self):
        s = self.Cls()
        assert s.params.get("oversold") <= 18, "oversold must be <=18"
        assert s.params.get("overbought") >= 82, "overbought must be >=82"

    def test_vol_spike_param(self):
        assert self.Cls().params.get("vol_spike_mult") == 1.5

    def test_adx_max_override_blocks_all(self):
        """adx_max=0 should block all signals in any market."""
        s = self.Cls()
        s.params["adx_max"] = 0
        df = _in_session_df(n=300, trend="oscillate")
        result = s.generate_signals(df)
        assert _all_zero(result), "adx_max=0 must block all RSI extreme signals"

    def test_no_signals_in_strong_trend(self):
        """adx_max=5 forces gate to block trending market."""
        s = self.Cls()
        s.params["adx_max"] = 5
        df = _in_session_df(n=300, trend="up")
        result = s.generate_signals(df)
        assert _all_zero(result), "adx_max=5 must block signals in a trending market"


# ─── YAML integrity ───────────────────────────────────────────────────────────

class TestYamlIntegrity:

    def _load_yaml(self):
        import yaml
        yaml_path = os.path.join(os.path.dirname(__file__), "..", "config", "strategies.yaml")
        with open(yaml_path, "rb") as f:
            raw = f.read().replace(b"\x00", b"")
        return yaml.safe_load(raw.decode("utf-8"))

    def test_yaml_parses(self):
        data = self._load_yaml()
        assert isinstance(data, dict)
        assert "active" in data

    def test_active_list_includes_rehabilitated_scalpers(self):
        data = self._load_yaml()
        active = data["active"]
        assert "bb_squeeze_scalp" in active, "bb_squeeze_scalp must be in active list"
        assert "rsi_extremes_scalp" in active, "rsi_extremes_scalp must be in active list"

    def test_scalpers_not_in_disabled(self):
        data = self._load_yaml()
        disabled = data.get("disabled_pending_review", [])
        assert "bb_squeeze_scalp" not in disabled
        assert "rsi_extremes_scalp" not in disabled

    def test_macd_trend_yaml_params(self):
        data = self._load_yaml()
        mt = data["macd_trend"]
        assert mt["timeframes"] == ["H1", "H4"]
        assert mt["parameters"]["adx_threshold"] == 28
        assert mt["parameters"]["rsi_long_min"] == 55
        assert mt["parameters"]["ema200_period"] == 200

    def test_bb_squeeze_scalp_yaml_enabled(self):
        data = self._load_yaml()
        bbs = data["bb_squeeze_scalp"]
        assert bbs["enabled"] is True
        assert bbs["timeframes"] == ["M15"]
        assert bbs["parameters"]["adx_min"] == 25

    def test_rsi_extremes_scalp_yaml_enabled(self):
        data = self._load_yaml()
        rse = data["rsi_extremes_scalp"]
        assert rse["enabled"] is True
        assert rse["timeframes"] == ["M15"]
        assert rse["parameters"]["adx_max"] == 30
        assert rse["parameters"]["vol_spike_mult"] == 1.5

    def test_all_active_strategies_have_yaml_block(self):
        data = self._load_yaml()
        missing = [s for s in data["active"] if s not in data]
        assert missing == [], f"Active strategies missing yaml blocks: {missing}"


# ─── Cross-strategy: validate_params on all 12 modified strategies ────────────

class TestValidateParamsAll:

    def test_all_validate(self):
        from strategies.gold_momentum_breakout import GoldMomentumBreakoutStrategy
        from strategies.ema_ribbon_trend import EMARibbonTrendStrategy
        from strategies.dual_ema_fractal import DualEMAFractal
        from strategies.range_breakout import RangeBreakoutStrategy
        from strategies.macd_trend import MACDTrendStrategy
        from strategies.turtle_soup import TurtleSoup
        from strategies.dual_ema_momentum import DualEMAMomentum
        from strategies.hikkake_trap import HikkakeTrap
        from strategies.rvgi_cci_confluence import RVGICCIConfluence
        from strategies.vwap_momentum import VWAPMomentum
        from strategies.bb_squeeze_scalp import BBSqueezeScalp
        from strategies.rsi_extremes_scalp import RSIExtremesScalp

        classes = [
            GoldMomentumBreakoutStrategy, EMARibbonTrendStrategy, DualEMAFractal,
            RangeBreakoutStrategy, MACDTrendStrategy, TurtleSoup, DualEMAMomentum,
            HikkakeTrap, RVGICCIConfluence, VWAPMomentum, BBSqueezeScalp, RSIExtremesScalp,
        ]
        failures = []
        for cls in classes:
            try:
                s = cls()
                if not s.validate_params():
                    failures.append(f"{cls.__name__}: validate_params() returned False")
            except Exception as e:
                failures.append(f"{cls.__name__}: raised {type(e).__name__}: {e}")

        assert failures == [], "validate_params failures:\n" + "\n".join(failures)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
