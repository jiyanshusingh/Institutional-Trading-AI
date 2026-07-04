from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from domain.strategy.trade_candidate import (
    TradeCandidate,
    TradeDirection,
)


def create_trade_candidate():

    return TradeCandidate(
        symbol="RELIANCE",
        direction=TradeDirection.LONG,
        entry_price=2500,
        stop_loss=2450,
        target_price=2650,
        confidence=0.90,
        expected_reward_risk=3.0,
        generated_timestamp=datetime.now(),
        reasoning=(
            "Bullish market bias",
            "Expansion active",
            "Order block respected",
        ),
    )


def test_create_trade_candidate():

    candidate = create_trade_candidate()

    assert candidate.symbol == "RELIANCE"
    assert candidate.direction == TradeDirection.LONG
    assert candidate.entry_price == 2500
    assert candidate.stop_loss == 2450
    assert candidate.target_price == 2650
    assert candidate.confidence == 0.90
    assert candidate.expected_reward_risk == 3.0
    assert len(candidate.reasoning) == 3


def test_symbol_cannot_be_empty():

    with pytest.raises(ValueError):

        TradeCandidate(
            symbol="",
            direction=TradeDirection.LONG,
            entry_price=100,
            stop_loss=95,
            target_price=120,
            confidence=0.8,
            expected_reward_risk=2.5,
            generated_timestamp=datetime.now(),
            reasoning=("Reason",),
        )


def test_prices_must_be_positive():

    with pytest.raises(ValueError):

        TradeCandidate(
            symbol="TEST",
            direction=TradeDirection.LONG,
            entry_price=-1,
            stop_loss=95,
            target_price=120,
            confidence=0.8,
            expected_reward_risk=2.5,
            generated_timestamp=datetime.now(),
            reasoning=("Reason",),
        )


def test_confidence_must_be_between_zero_and_one():

    with pytest.raises(ValueError):

        TradeCandidate(
            symbol="TEST",
            direction=TradeDirection.LONG,
            entry_price=100,
            stop_loss=95,
            target_price=120,
            confidence=1.5,
            expected_reward_risk=2.5,
            generated_timestamp=datetime.now(),
            reasoning=("Reason",),
        )


def test_expected_reward_risk_must_be_positive():

    with pytest.raises(ValueError):

        TradeCandidate(
            symbol="TEST",
            direction=TradeDirection.LONG,
            entry_price=100,
            stop_loss=95,
            target_price=120,
            confidence=0.8,
            expected_reward_risk=0,
            generated_timestamp=datetime.now(),
            reasoning=("Reason",),
        )


def test_reasoning_cannot_be_empty():

    with pytest.raises(ValueError):

        TradeCandidate(
            symbol="TEST",
            direction=TradeDirection.LONG,
            entry_price=100,
            stop_loss=95,
            target_price=120,
            confidence=0.8,
            expected_reward_risk=2.5,
            generated_timestamp=datetime.now(),
            reasoning=(),
        )


def test_is_long():

    candidate = create_trade_candidate()

    assert candidate.is_long
    assert not candidate.is_short


def test_trade_candidate_is_immutable():

    candidate = create_trade_candidate()

    with pytest.raises(FrozenInstanceError):
        candidate.entry_price = 2600