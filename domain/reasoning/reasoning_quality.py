"""
Reasoning Quality

Theory 1.0

A ReasoningQuality represents an assessment of the quality
of the reasoning used to construct a MarketThesis.

It evaluates the reasoning process itself.

It performs no reasoning.

It is an immutable value object produced by the
Reasoning Model.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReasoningQuality:
    """
    Immutable assessment of reasoning quality.
    """

    level: str

    complete: bool

    explainable: bool

    falsifiable: bool

    internally_consistent: bool

    evidence_supported: bool

    rationale: str

    def __post_init__(self):

        if self.level not in (
            "HIGH",
            "MEDIUM",
            "LOW",
        ):
            raise ValueError(
                "Invalid reasoning quality level."
            )

    @property
    def is_high(self) -> bool:
        return self.level == "HIGH"

    @property
    def is_medium(self) -> bool:
        return self.level == "MEDIUM"

    @property
    def is_low(self) -> bool:
        return self.level == "LOW"

    @property
    def score(self) -> int:
        """
        Number of satisfied reasoning criteria.
        """

        return sum(
            (
                self.complete,
                self.explainable,
                self.falsifiable,
                self.internally_consistent,
                self.evidence_supported,
            )
        )

    @property
    def summary(self) -> dict:
        return {
            "level": self.level,
            "score": self.score,
            "complete": self.complete,
            "explainable": self.explainable,
            "falsifiable": self.falsifiable,
            "internally_consistent": self.internally_consistent,
            "evidence_supported": self.evidence_supported,
        }

    def __str__(self) -> str:
        return (
            f"ReasoningQuality("
            f"level={self.level}, "
            f"score={self.score}/5)"
        )