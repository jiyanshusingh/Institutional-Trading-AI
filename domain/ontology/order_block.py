"""
Order Block

Theory 1.0

An OrderBlock is an immutable semantic construct representing
a confirmed institutional price region.

It performs no computation.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderBlockDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


@dataclass(frozen=True, slots=True)
class OrderBlock:
    """
    Immutable Order Block.
    """

    source_fair_value_gap_index: int

    start_timestamp: datetime

    end_timestamp: datetime

    upper_price: float

    lower_price: float

    direction: OrderBlockDirection

    def __post_init__(self):

        if self.source_fair_value_gap_index < 0:
            raise ValueError(
                "Source Fair Value Gap index cannot be negative."
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
            == OrderBlockDirection.BULLISH
        )

    @property
    def is_bearish(self) -> bool:
        return (
            self.direction
            == OrderBlockDirection.BEARISH
        )

    @property
    def height(self) -> float:
        return (
            self.upper_price
            - self.lower_price
        )