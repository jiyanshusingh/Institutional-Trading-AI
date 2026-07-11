"""
==========================================================
Validation Result
==========================================================

Purpose
-------
Represents the complete validation result of one feature
against one research target.

A ValidationResult aggregates multiple statistical tests
into one final research decision.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from research.statistics.statistical_result import (
    StatisticalResult,
)


# ==========================================================
# Validation Result
# ==========================================================

@dataclass(slots=True)
class ValidationResult:
    """
    Complete validation result for one feature.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    feature: str

    target: str

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    statistical_results: list[
        StatisticalResult
    ] = field(default_factory=list)

    # ------------------------------------------------------
    # Final Score
    # ------------------------------------------------------

    score: float = 0.0

    rank: int | None = None

    status: str = "UNVALIDATED"

    confidence: float = 0.0

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # ======================================================
    # Public API
    # ======================================================

    def add_result(
        self,
        result: StatisticalResult,
    ) -> None:

        self.statistical_results.append(
            result
        )

    # ======================================================
    # Statistics
    # ======================================================

    @property
    def total_tests(self) -> int:

        return len(
            self.statistical_results
        )

    @property
    def significant_tests(self) -> int:

        return sum(

            1

            for result in self.statistical_results

            if result.significant

        )

    @property
    def significance_ratio(
        self,
    ) -> float:

        if self.total_tests == 0:

            return 0.0

        return (

            self.significant_tests
            / self.total_tests

        )

    # ======================================================
    # Metadata
    # ======================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    # ======================================================
    # Export
    # ======================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {

            "feature": self.feature,

            "target": self.target,

            "score": self.score,

            "rank": self.rank,

            "status": self.status,

            "confidence": self.confidence,

            "total_tests": self.total_tests,

            "significant_tests": self.significant_tests,

            "significance_ratio": self.significance_ratio,

            "created_at": self.created_at,

        }

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(
        self,
    ) -> str:

        return (

            "ValidationResult("

            f"feature='{self.feature}', "

            f"target='{self.target}', "

            f"score={self.score:.3f}, "

            f"status='{self.status}'"

            ")"

        )