"""
Trade Candidate Score

Theory 1.0

Represents the evaluation of a TradeCandidate.

A TradeCandidateScore is immutable and explainable.

It is not a ranking.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TradeCandidateScore:
    """
    Immutable score assigned to a TradeCandidate.
    """

    overall_score: float

    confidence_score: float

    structural_score: float

    liquidity_score: float

    reward_risk_score: float

    reasoning: tuple[str, ...]

    def __post_init__(self):

        scores = (
            self.overall_score,
            self.confidence_score,
            self.structural_score,
            self.liquidity_score,
            self.reward_risk_score,
        )

        for score in scores:

            if not (0.0 <= score <= 100.0):
                raise ValueError(
                    "Scores must be between 0 and 100."
                )

        if len(self.reasoning) == 0:
            raise ValueError(
                "Reasoning cannot be empty."
            )

    @property
    def is_excellent(self) -> bool:
        return self.overall_score >= 90

    @property
    def is_good(self) -> bool:
        return 75 <= self.overall_score < 90

    @property
    def is_average(self) -> bool:
        return 50 <= self.overall_score < 75

    @property
    def is_poor(self) -> bool:
        return self.overall_score < 50