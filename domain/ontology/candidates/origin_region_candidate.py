"""
Origin Region Candidate

Theory 1.0

Represents a potential OriginRegion before
confirmation.

An OriginRegionCandidate is discovered from
existing semantic constructs but is not yet
authoritative.
"""

from dataclasses import dataclass
from datetime import datetime

from domain.ontology.origin_region import (
    OriginRegionDirection,
)


@dataclass(frozen=True, slots=True)
class OriginRegionCandidate:
    """
    Immutable Origin Region Candidate.
    """

    source_expansion_index: int

    start_timestamp: datetime

    end_timestamp: datetime

    upper_price: float

    lower_price: float

    direction: OriginRegionDirection

    def __post_init__(self):

        if self.source_expansion_index < 0:
            raise ValueError(
                "Source expansion index cannot be negative."
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