"""
Opportunity

Version 1.0

An Opportunity represents a justified candidate for action
produced from one or more Market Theses.

It performs no reasoning.

It contains no execution details.

It is immutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple


@dataclass(frozen=True, slots=True)
class Opportunity:
    """
    Immutable Opportunity.
    """

    # ----------------------------------------------------------
    # Identity
    # ----------------------------------------------------------

    opportunity_id: str

    created_at: datetime

    # ----------------------------------------------------------
    # Scope
    # ----------------------------------------------------------

    symbol: str

    timeframe: str

    # ----------------------------------------------------------
    # Opportunity
    # ----------------------------------------------------------

    opportunity_type: str

    direction: str

    priority: str

    # ----------------------------------------------------------
    # Reasoning
    # ----------------------------------------------------------

    supporting_thesis_ids: Tuple[str, ...] = field(default_factory=tuple)

    evidence_quality: str = "UNKNOWN"

    reasoning_quality: str = "UNKNOWN"

    expected_structural_evolution: str = ""

    assumptions: Tuple[str, ...] = field(default_factory=tuple)

    invalidation: Tuple[str, ...] = field(default_factory=tuple)

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    def __post_init__(self):

        if not self.opportunity_id:
            raise ValueError(
                "Opportunity ID cannot be empty."
            )

        if not self.symbol:
            raise ValueError(
                "Symbol cannot be empty."
            )

        if not self.timeframe:
            raise ValueError(
                "Timeframe cannot be empty."
            )

        if self.opportunity_type not in (
            "LONG",
            "SHORT",
            "WAIT",
        ):
            raise ValueError(
                "Invalid opportunity type."
            )

        if self.direction not in (
            "LONG",
            "SHORT",
            "NONE",
        ):
            raise ValueError(
                "Invalid direction."
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
    def is_long(self) -> bool:
        return self.opportunity_type == "LONG"

    @property
    def is_short(self) -> bool:
        return self.opportunity_type == "SHORT"

    @property
    def is_wait(self) -> bool:
        return self.opportunity_type == "WAIT"

    @property
    def has_supporting_theses(self) -> bool:
        return len(self.supporting_thesis_ids) > 0

    @property
    def is_actionable(self) -> bool:
        return self.opportunity_type in (
            "LONG",
            "SHORT",
        )

    @property
    def summary(self) -> dict:

        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "type": self.opportunity_type,
            "direction": self.direction,
            "priority": self.priority,
            "evidence_quality": self.evidence_quality,
            "reasoning_quality": self.reasoning_quality,
        }

    def __str__(self) -> str:

        return (
            f"Opportunity("
            f"{self.symbol}, "
            f"{self.timeframe}, "
            f"{self.opportunity_type}, "
            f"{self.priority})"
        )