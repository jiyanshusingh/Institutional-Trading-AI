"""
Tests for the Institutional Probability Engine — new factors and SHORT R:R fix.

Run with: pytest test/test_institutional_probability.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from engines.institutional_probability_engine import InstitutionalProbabilityEngine
from strategies.institutional_strategy import InstitutionalStrategy


def _make_df(n: int = 120, seed: int = 1, trend: float = 0.0) -> pd.DataFrame:
    """Synthetic OHLCV with optional upward/downward trend."""
    np.random.seed(seed)
    idx = pd.date_range("2024-01-01 09:15", periods=n, freq="15min")
    close = 100 + np.cumsum(np.random.randn(n) * 0.5 + trend)
    close = np.maximum(close, 10)
    open_ = close + np.random.randn(n) * 0.2
    high = np.maximum(open_, close) + np.abs(np.random.randn(n)) * 0.3
    low = np.minimum(open_, close) - np.abs(np.random.randn(n)) * 0.3
    volume = np.random.randint(1000, 5000, n)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close,
         "volume": volume, "timestamp": idx}
    )


def _make_daily(n: int = 150, seed: int = 2, trend: float = 0.0) -> pd.DataFrame:
    np.random.seed(seed)
    idx = pd.date_range("2023-09-01", periods=n, freq="1d")
    close = 100 + np.cumsum(np.random.randn(n) * 0.5 + trend)
    close = np.maximum(close, 10)
    return pd.DataFrame({"close": close, "timestamp": idx})


# ── SHORT R:R fix ─────────────────────────────────────────────

def test_short_rr_is_at_least_one():
    """SHORT SL/TP must yield RR >= 1 (not the old 0.5)."""
    df = _make_df(trend=0.1)
    strat = InstitutionalStrategy()  # uses engine RR when available
    sl, tp = strat._compute_sltp(df, float(df["close"].iloc[-1]), is_short=True)
    entry = float(df["close"].iloc[-1])
    risk = abs(entry - sl)
    reward = abs(entry - tp)
    assert risk > 0
    assert (reward / risk) >= 1.0, f"SHORT RR={reward/risk:.2f} < 1.0"


def test_long_rr_is_at_least_one():
    df = _make_df(trend=0.1)
    strat = InstitutionalStrategy()
    sl, tp = strat._compute_sltp(df, float(df["close"].iloc[-1]), is_short=False)
    entry = float(df["close"].iloc[-1])
    risk = abs(entry - sl)
    reward = abs(entry - tp)
    assert (reward / risk) >= 1.0


# ── New factors present ──────────────────────────────────────

def test_engine_has_new_factors():
    df = _make_df()
    eng = InstitutionalProbabilityEngine()
    res = eng.compute(df, entry_time="2024-01-01T10:30:00")
    assert "session_timing" in res["factors"]
    assert "historical_performance" in res["factors"]
    # total factor capacity should be 100
    total_max = sum(f["max"] for f in res["factors"].values())
    assert total_max == 100, f"Factor capacity = {total_max}, expected 100"


def test_session_factor_detects_session():
    df = _make_df()
    eng = InstitutionalProbabilityEngine()
    res = eng.compute(df, entry_time="2024-01-01T10:30:00")
    sess = res["factors"]["session_timing"]["detail"].get("session")
    assert sess in ("opening", "morning", "midday", "afternoon", "closing", "unknown")


def test_historical_factor_uses_daily():
    df = _make_df()
    daily = _make_daily(trend=0.2)  # positive momentum
    eng = InstitutionalProbabilityEngine()
    res = eng.compute(df, stock_daily=daily, entry_time="2024-01-01T10:30:00")
    detail = res["factors"]["historical_performance"]["detail"]
    assert "ret_5d" in detail
    assert "ret_20d" in detail
    # Positive momentum should produce some bullish score
    assert res["factors"]["historical_performance"]["bullish"] >= 0


def test_historical_factor_no_daily_is_neutral():
    df = _make_df()
    eng = InstitutionalProbabilityEngine()
    res = eng.compute(df, stock_daily=None, entry_time="2024-01-01T10:30:00")
    assert res["factors"]["historical_performance"]["bullish"] == 0
    assert res["factors"]["historical_performance"]["bearish"] == 0


# ── Risk sizing (conservative 0.5%) ──────────────────────────

def test_risk_per_trade_pct_in_config():
    from config.trading_config import MAX_RISK_PER_TRADE
    assert MAX_RISK_PER_TRADE == 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
