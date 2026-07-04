"""
Expansion Candidate

Theory 1.0

Represents a potential Expansion before confirmation.

An ExpansionCandidate is discovered from existing semantic
constructs but is not yet authoritative.
"""

from dataclasses import dataclass
from datetime import datetime

from domain.ontology.expansion import (
    ExpansionDirection,
)


@dataclass(frozen=True, slots=True)
class ExpansionCandidate:
    """
    Immutable Expansion Candidate.
    """

    base_swing_index: int

    confirmation_event_index: int

    start_timestamp: datetime

    end_timestamp: datetime

    start_price: float

    end_price: float

    direction: ExpansionDirection

    def __post_init__(self):

        if self.base_swing_index < 0:
            raise ValueError(
                "Base swing index cannot be negative."
            )

        if self.confirmation_event_index < 0:
            raise ValueError(
                "Confirmation event index cannot be negative."
            )

        if self.start_price <= 0:
            raise ValueError(
                "Start price must be positive."
            )

        if self.end_price <= 0:
            raise ValueError(
                "End price must be positive."
            )

        if self.end_timestamp < self.start_timestamp:
            raise ValueError(
                "End timestamp cannot be before start timestamp."
            )