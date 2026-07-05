"""
Evidence Assessment

Theory 1.0

An EvidenceAssessment represents the reasoning model's
assessment of how well the current Market Thesis is
supported by the available evidence.

It performs no reasoning itself.

It is an immutable value object produced by the
Reasoning Model.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceAssessment:
    """
    Immutable assessment of evidence quality.
    """

    level: str

    supporting_count: int

    counter_count: int

    rationale: str

    def __post_init__(self):

        if self.supporting_count < 0:
            raise ValueError(
                "Supporting evidence count cannot be negative."
            )

        if self.counter_count < 0:
            raise ValueError(
                "Counter evidence count cannot be negative."
            )

        if self.level not in (
            "STRONG",
            "MODERATE",
            "WEAK",
        ):
            raise ValueError(
                "Invalid evidence assessment level."
            )

    @property
    def net_support(self) -> int:
        """
        Difference between supporting and
        counter evidence.
        """

        return (
            self.supporting_count
            - self.counter_count
        )

    @property
    def has_counter_evidence(self) -> bool:
        return self.counter_count > 0

    @property
    def is_strong(self) -> bool:
        return self.level == "STRONG"

    @property
    def is_moderate(self) -> bool:
        return self.level == "MODERATE"

    @property
    def is_weak(self) -> bool:
        return self.level == "WEAK"

    @property
    def summary(self) -> dict:
        return {
            "level": self.level,
            "supporting": self.supporting_count,
            "counter": self.counter_count,
            "net_support": self.net_support,
        }

    def __str__(self) -> str:
        return (
            f"EvidenceAssessment("
            f"level={self.level}, "
            f"support={self.supporting_count}, "
            f"counter={self.counter_count})"
        )