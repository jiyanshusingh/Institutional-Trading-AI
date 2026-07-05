from datetime import UTC, datetime

import pytest

from domain.trade.trade_candidate import TradeCandidate


def make_trade() -> TradeCandidate:

    return TradeCandidate(
        trade_id="TRADE-001",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        direction="LONG",

        capital_allocation=40.0,

        position_size=100.0,

        entry_price=None,
        stop_loss=None,
        take_profit=None,

        risk_reward_ratio=None,

        order_type="UNKNOWN",

        validity="UNKNOWN",

        rationale="Test trade.",
    )


# ==========================================================
# Creation
# ==========================================================

def test_trade_creation():

    trade = make_trade()

    assert trade.symbol == "RELIANCE"
    assert trade.timeframe == "15m"
    assert trade.direction == "LONG"


# ==========================================================
# Direction
# ==========================================================

def test_is_long():

    trade = make_trade()

    assert trade.is_long


def test_is_not_short():

    trade = make_trade()

    assert not trade.is_short


def test_is_not_wait():

    trade = make_trade()

    assert not trade.is_wait


# ==========================================================
# Execution Fields
# ==========================================================

def test_has_no_entry_price():

    trade = make_trade()

    assert not trade.has_entry_price


def test_has_no_stop_loss():

    trade = make_trade()

    assert not trade.has_stop_loss


def test_has_no_take_profit():

    trade = make_trade()

    assert not trade.has_take_profit


def test_not_executable():

    trade = make_trade()

    assert not trade.is_executable


# ==========================================================
# Summary
# ==========================================================

def test_summary():

    trade = make_trade()

    summary = trade.summary

    assert summary["symbol"] == "RELIANCE"
    assert summary["timeframe"] == "15m"
    assert summary["direction"] == "LONG"
    assert summary["capital_allocation"] == 40.0


# ==========================================================
# Validation
# ==========================================================

def test_invalid_direction():

    with pytest.raises(ValueError):

        TradeCandidate(
            trade_id="1",
            created_at=datetime.now(UTC),

            symbol="RELIANCE",
            timeframe="15m",

            direction="BUY",

            capital_allocation=40.0,

            position_size=100.0,
        )


def test_invalid_capital_allocation():

    with pytest.raises(ValueError):

        TradeCandidate(
            trade_id="1",
            created_at=datetime.now(UTC),

            symbol="RELIANCE",
            timeframe="15m",

            direction="LONG",

            capital_allocation=120.0,

            position_size=100.0,
        )


def test_negative_position_size():

    with pytest.raises(ValueError):

        TradeCandidate(
            trade_id="1",
            created_at=datetime.now(UTC),

            symbol="RELIANCE",
            timeframe="15m",

            direction="LONG",

            capital_allocation=40.0,

            position_size=-10.0,
        )


# ==========================================================
# Executable Trade
# ==========================================================

def test_trade_becomes_executable():

    trade = TradeCandidate(
        trade_id="TRADE-002",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        direction="LONG",

        capital_allocation=40.0,

        position_size=100.0,

        entry_price=2500.0,
        stop_loss=2450.0,
        take_profit=2650.0,

        risk_reward_ratio=3.0,

        order_type="LIMIT",

        validity="DAY",

        rationale="Executable trade.",
    )

    assert trade.has_entry_price
    assert trade.has_stop_loss
    assert trade.has_take_profit

    assert trade.is_executable