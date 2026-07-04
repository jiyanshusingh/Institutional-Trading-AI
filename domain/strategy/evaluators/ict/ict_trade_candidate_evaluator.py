"""
ICT Trade Candidate Evaluator

Theory 1.0

Initial placeholder evaluator.
"""

from domain.strategy.trade_candidate import (
    TradeCandidate,
)

from domain.strategy.trade_candidate_score import (
    TradeCandidateScore,
)

from ..trade_candidate_evaluator import (
    TradeCandidateEvaluator,
)


class ICTTradeCandidateEvaluator(
    TradeCandidateEvaluator
):

    def evaluate(
        self,
        candidate: TradeCandidate,
    ) -> TradeCandidateScore:

        if candidate is None:
            raise ValueError(
                "TradeCandidate is required."
            )

        #
        # Theory 1.0 placeholder implementation.
        #
        # Later versions will derive these from:
        #
        # - Market Interpretation
        # - Structure quality
        # - Liquidity
        # - Reward / Risk
        #

        confidence_score = candidate.confidence * 100.0

        structural_score = confidence_score

        liquidity_score = confidence_score

        reward_risk_score = min(
            candidate.expected_reward_risk * 25.0,
            100.0,
        )

        overall_score = (
            confidence_score +
            structural_score +
            liquidity_score +
            reward_risk_score
        ) / 4.0

        reasoning = (
            "Initial ICT evaluation.",
            "Placeholder scoring model.",
        )

        return TradeCandidateScore(
            overall_score=overall_score,
            confidence_score=confidence_score,
            structural_score=structural_score,
            liquidity_score=liquidity_score,
            reward_risk_score=reward_risk_score,
            reasoning=reasoning,
        )