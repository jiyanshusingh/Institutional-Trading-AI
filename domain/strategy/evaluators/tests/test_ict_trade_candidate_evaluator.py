from datetime import datetime

import pytest

from domain.strategy.trade_candidate import (
    TradeCandidate,
    TradeDirection,
)

from domain.strategy.trade_candidate_score import (
    TradeCandidateScore,
)

from domain.strategy.evaluators.ict.ict_trade_candidate_evaluator import (
    ICTTradeCandidateEvaluator,
)


def create_candidate():

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
            "Bullish structure",
            "Untouched FVG",
        ),
    )


def test_evaluate_returns_score():

    evaluator = ICTTradeCandidateEvaluator()

    score = evaluator.evaluate(
        create_candidate(),
    )

    assert isinstance(
        score,
        TradeCandidateScore,
    )


def test_overall_score_within_range():

    evaluator = ICTTradeCandidateEvaluator()

    score = evaluator.evaluate(
        create_candidate(),
    )

    assert 0 <= score.overall_score <= 100


def test_confidence_score_matches_candidate():

    evaluator = ICTTradeCandidateEvaluator()

    candidate = create_candidate()

    score = evaluator.evaluate(
        candidate,
    )

    assert score.confidence_score == 90.0


def test_requires_candidate():

    evaluator = ICTTradeCandidateEvaluator()

    with pytest.raises(ValueError):

        evaluator.evaluate(None)