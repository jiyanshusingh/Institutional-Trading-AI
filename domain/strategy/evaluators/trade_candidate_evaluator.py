"""
Trade Candidate Evaluator

Defines the contract for evaluating a TradeCandidate.
"""

from abc import ABC, abstractmethod

from domain.strategy.trade_candidate import (
    TradeCandidate,
)

from domain.strategy.trade_candidate_score import (
    TradeCandidateScore,
)


class TradeCandidateEvaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        candidate: TradeCandidate,
    ) -> TradeCandidateScore:
        """
        Evaluate a TradeCandidate and produce a score.
        """
        pass