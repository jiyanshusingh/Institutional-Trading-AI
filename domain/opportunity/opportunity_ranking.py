"""
Opportunity Ranking

Version 1.0

An OpportunityRanking represents the relative priority of a
single OpportunityAssessment among competing Opportunities.

It performs no computation.

It is immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class OpportunityRanking:
    """
    Immutable Opportunity Ranking.
    """

    # ----------------------------------------------------------
    # Identity
    # ----------------------------------------------------------

    ranking_id: str

    created_at: datetime

    assessment_id: str

    # ----------------------------------------------------------
    # Ranking
    # ----------------------------------------------------------

    rank_position: int

    ranking_score: int

    priority: str

    portfolio_eligible: bool

    # ----------------------------------------------------------
    # Explanation
    # ----------------------------------------------------------

    rationale: str

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    def __post_init__(self):

        if not self.ranking_id:
            raise ValueError(
                "Ranking ID cannot be empty."
            )

        if not self.assessment_id:
            raise ValueError(
                "Assessment ID cannot be empty."
            )

        if self.rank_position <= 0:
            raise ValueError(
                "Rank position must be positive."
            )

        if not (0 <= self.ranking_score <= 100):
            raise ValueError(
                "Ranking score must be between 0 and 100."
            )

        if self.priority not in (
            "HIGH",
            "MEDIUM",
            "LOW",
        ):
            raise ValueError(
                "Invalid priority."
            )

    # ----------------------------------------------------------
    # Convenience
    # ----------------------------------------------------------

    @property
    def is_high_priority(self) -> bool:
        return self.priority == "HIGH"

    @property
    def is_medium_priority(self) -> bool:
        return self.priority == "MEDIUM"

    @property
    def is_low_priority(self) -> bool:
        return self.priority == "LOW"

    @property
    def is_top_ranked(self) -> bool:
        """
        True if this is the highest-ranked Opportunity.
        """
        return self.rank_position == 1

    @property
    def ready_for_portfolio(self) -> bool:
        """
        Indicates whether this ranking is eligible for
        Portfolio Decision.
        """
        return self.portfolio_eligible

    @property
    def summary(self) -> dict:

        return {
            "rank_position": self.rank_position,
            "ranking_score": self.ranking_score,
            "priority": self.priority,
            "portfolio_eligible": self.portfolio_eligible,
        }

    def __str__(self) -> str:

        return (
            f"OpportunityRanking("
            f"rank={self.rank_position}, "
            f"score={self.ranking_score}, "
            f"priority={self.priority})"
        )