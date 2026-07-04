"""
Expansion

Theory 1.0

An Expansion is an immutable semantic construct representing a
completed structural movement.

It begins at a Base Swing and ends at a confirming
Structure Event.

The Expansion performs no computation.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ExpansionDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


@dataclass(frozen=True, slots=True)
class Expansion:
    """
    Immutable Expansion.
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

    @property
    def is_bullish(self) -> bool:
        return (
            self.direction
            == ExpansionDirection.BULLISH
        )

    @property
    def is_bearish(self) -> bool:
        return (
            self.direction
            == ExpansionDirection.BEARISH
        )

    @property
    def price_range(self) -> float:
        return abs(
            self.end_price - self.start_price
        )