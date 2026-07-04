from dataclasses import FrozenInstanceError

import pytest

from domain.strategy.trade_candidate_score import (
    TradeCandidateScore,
)


def create_score():

    return TradeCandidateScore(
        overall_score=92,
        confidence_score=90,
        structural_score=95,
        liquidity_score=88,
        reward_risk_score=94,
        reasoning=(
            "Strong structure",
            "Excellent reward-risk",
            "High confidence",
        ),
    )


def test_create_trade_candidate_score():

    score = create_score()

    assert score.overall_score == 92
    assert score.confidence_score == 90
    assert score.structural_score == 95
    assert score.liquidity_score == 88
    assert score.reward_risk_score == 94
    assert len(score.reasoning) == 3


def test_scores_must_be_between_zero_and_hundred():

    with pytest.raises(ValueError):

        TradeCandidateScore(
            overall_score=101,
            confidence_score=90,
            structural_score=90,
            liquidity_score=90,
            reward_risk_score=90,
            reasoning=("Reason",),
        )


def test_reasoning_cannot_be_empty():

    with pytest.raises(ValueError):

        TradeCandidateScore(
            overall_score=90,
            confidence_score=90,
            structural_score=90,
            liquidity_score=90,
            reward_risk_score=90,
            reasoning=(),
        )


def test_is_excellent():

    score = create_score()

    assert score.is_excellent
    assert not score.is_good
    assert not score.is_average
    assert not score.is_poor


def test_good_score():

    score = TradeCandidateScore(
        overall_score=82,
        confidence_score=80,
        structural_score=83,
        liquidity_score=81,
        reward_risk_score=84,
        reasoning=("Reason",),
    )

    assert score.is_good


def test_average_score():

    score = TradeCandidateScore(
        overall_score=60,
        confidence_score=60,
        structural_score=60,
        liquidity_score=60,
        reward_risk_score=60,
        reasoning=("Reason",),
    )

    assert score.is_average


def test_poor_score():

    score = TradeCandidateScore(
        overall_score=40,
        confidence_score=40,
        structural_score=40,
        liquidity_score=40,
        reward_risk_score=40,
        reasoning=("Reason",),
    )

    assert score.is_poor


def test_trade_candidate_score_is_immutable():

    score = create_score()

    with pytest.raises(FrozenInstanceError):
        score.overall_score = 95