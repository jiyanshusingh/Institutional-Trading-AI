"""
Fair Value Gap Candidate

Theory 1.0

Represents a potential FairValueGap before
confirmation.

A FairValueGapCandidate is discovered from
existing semantic constructs but is not yet
authoritative.
"""

from dataclasses import dataclass
from datetime import datetime

from domain.ontology.fair_value_gap import (
    FairValueGapDirection,
)


@dataclass(frozen=True, slots=True)
class FairValueGapCandidate:
    """
    Immutable Fair Value Gap Candidate.
    """

    source_origin_region_index: int

    start_timestamp: datetime

    end_timestamp: datetime

    upper_price: float

    lower_price: float

    direction: FairValueGapDirection

    def __post_init__(self):

        if self.source_origin_region_index < 0:
            raise ValueError(
                "Source origin region index cannot be negative."
            )

        if self.upper_price <= 0:
            raise ValueError(
                "Upper price must be positive."
            )

        if self.lower_price <= 0:
            raise ValueError(
                "Lower price must be positive."
            )

        if self.upper_price < self.lower_price:
            raise ValueError(
                "Upper price cannot be less than lower price."
            )

        if self.end_timestamp < self.start_timestamp:
            raise ValueError(
                "End timestamp cannot be before start timestamp."
            )