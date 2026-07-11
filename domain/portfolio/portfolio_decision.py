"""
Portfolio Decision

Version 1.0

A PortfolioDecision represents the final allocation of
capital across one or more ranked Opportunities.

It performs no computation.

It is immutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple


@dataclass(frozen=True, slots=True)
class PortfolioDecision:
    """
    Immutable Portfolio Decision.
    """

    # ----------------------------------------------------------
    # Identity
    # ----------------------------------------------------------

    decision_id: str

    created_at: datetime

    # ----------------------------------------------------------
    # Portfolio
    # ----------------------------------------------------------

    selected_ranking_ids: Tuple[str, ...] = field(
        default_factory=tuple
    )

    capital_allocations: Tuple[float, ...] = field(
        default_factory=tuple
    )

    symbols: Tuple[str, ...] = field(
        default_factory=tuple
    )

    timeframes: Tuple[str, ...] = field(
        default_factory=tuple
    )

    directions: Tuple[str, ...] = field(
        default_factory=tuple
    )

    allocation_method: str = "FIXED_WEIGHT"

    total_allocated: float = 0.0

    cash_reserve: float = 100.0

    constraints: Tuple[str, ...] = field(
        default_factory=tuple
    )

    rationale: str = ""

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    def __post_init__(self):

        if not self.decision_id:
            raise ValueError(
                "Decision ID cannot be empty."
            )

        n_ids = len(self.selected_ranking_ids)
        if n_ids != len(self.capital_allocations):
            raise ValueError(
                "Ranking IDs and capital allocations "
                "must have the same length."
            )

        if n_ids != len(self.symbols):
            raise ValueError(
                "Symbols must have the same length as ranking IDs."
            )

        if n_ids != len(self.timeframes):
            raise ValueError(
                "Timeframes must have the same length as ranking IDs."
            )

        if n_ids != len(self.directions):
            raise ValueError(
                "Directions must have the same length as ranking IDs."
            )

        if self.total_allocated < 0:
            raise ValueError(
                "Total allocated cannot be negative."
            )

        if self.cash_reserve < 0:
            raise ValueError(
                "Cash reserve cannot be negative."
            )

        total = (
            self.total_allocated
            + self.cash_reserve
        )

        if abs(total - 100.0) > 1e-6:
            raise ValueError(
                "Allocated capital plus cash reserve "
                "must equal 100%."
            )

        if any(
            allocation < 0
            for allocation in self.capital_allocations
        ):
            raise ValueError(
                "Capital allocations cannot be negative."
            )

    # ----------------------------------------------------------
    # Convenience
    # ----------------------------------------------------------

    @property
    def opportunity_count(self) -> int:
        return len(self.selected_ranking_ids)

    @property
    def is_fully_invested(self) -> bool:
        return self.cash_reserve == 0.0

    @property
    def has_cash_reserve(self) -> bool:
        return self.cash_reserve > 0.0

    @property
    def average_allocation(self) -> float:

        if not self.capital_allocations:
            return 0.0

        return (
            sum(self.capital_allocations)
            / len(self.capital_allocations)
        )

    @property
    def summary(self) -> dict:

        return {
            "opportunities": self.opportunity_count,
            "allocation_method": self.allocation_method,
            "total_allocated": self.total_allocated,
            "cash_reserve": self.cash_reserve,
        }

    def __str__(self) -> str:

        return (
            f"PortfolioDecision("
            f"opportunities={self.opportunity_count}, "
            f"allocated={self.total_allocated:.1f}%, "
            f"cash={self.cash_reserve:.1f}%)"
        )