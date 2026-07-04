"""
Origin Region

Theory 1.0

An OriginRegion is an immutable semantic construct representing
the structural price region from which a confirmed Expansion
originated.

It performs no computation.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OriginRegionDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


@dataclass(frozen=True, slots=True)
class OriginRegion:
    """
    Immutable Origin Region.
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

    @property
    def is_bullish(self) -> bool:
        return (
            self.direction
            == OriginRegionDirection.BULLISH
        )

    @property
    def is_bearish(self) -> bool:
        return (
            self.direction
            == OriginRegionDirection.BEARISH
        )

    @property
    def height(self) -> float:
        return (
            self.upper_price
            - self.lower_price
        )