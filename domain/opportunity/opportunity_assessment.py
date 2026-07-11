"""
Opportunity Assessment

Version 1.0

An OpportunityAssessment represents the evaluation of a
single Opportunity.

It performs no computation.

It is immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class OpportunityAssessment:
    """
    Immutable Opportunity Assessment.
    """

    # ----------------------------------------------------------
    # Identity
    # ----------------------------------------------------------

    assessment_id: str

    created_at: datetime

    opportunity_id: str

    # ----------------------------------------------------------
    # Assessment
    # ----------------------------------------------------------

    assessment_level: str

    overall_score: int

    actionable: bool

    objective_alignment: bool

    constraint_satisfaction: bool

    # ----------------------------------------------------------
    # Explanation
    # ----------------------------------------------------------

    rationale: str

    # ----------------------------------------------------------
    # Opportunity Info (carried forward, after required fields)
    # ----------------------------------------------------------

    symbol: str = ""

    timeframe: str = ""

    direction: str = ""

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    def __post_init__(self):

        if not self.assessment_id:
            raise ValueError(
                "Assessment ID cannot be empty."
            )

        if not self.opportunity_id:
            raise ValueError(
                "Opportunity ID cannot be empty."
            )

        if self.assessment_level not in (
            "HIGH",
            "MEDIUM",
            "LOW",
        ):
            raise ValueError(
                "Invalid assessment level."
            )

        if not (0 <= self.overall_score <= 100):
            raise ValueError(
                "Overall score must be between 0 and 100."
            )

    # ----------------------------------------------------------
    # Convenience
    # ----------------------------------------------------------

    @property
    def is_high(self) -> bool:
        return self.assessment_level == "HIGH"

    @property
    def is_medium(self) -> bool:
        return self.assessment_level == "MEDIUM"

    @property
    def is_low(self) -> bool:
        return self.assessment_level == "LOW"

    @property
    def ready_for_ranking(self) -> bool:
        """
        Indicates whether this Opportunity should
        proceed to the Opportunity Ranking layer.
        """

        return self.actionable

    @property
    def summary(self) -> dict:

        return {
            "assessment_level": self.assessment_level,
            "overall_score": self.overall_score,
            "actionable": self.actionable,
            "objective_alignment": self.objective_alignment,
            "constraint_satisfaction": self.constraint_satisfaction,
        }

    def __str__(self) -> str:

        return (
            f"OpportunityAssessment("
            f"level={self.assessment_level}, "
            f"score={self.overall_score}, "
            f"actionable={self.actionable})"
        )