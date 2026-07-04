from dataclasses import dataclass
from datetime import datetime

from .swing_type import SwingType


@dataclass(frozen=True, slots=True)
class Swing:

    index: int

    confirmation_index: int

    timestamp: datetime

    price: float

    swing_type: SwingType

    def __post_init__(self):

        if self.index < 0:
            raise ValueError(
                "Index cannot be negative."
            )

        if self.confirmation_index < self.index:
            raise ValueError(
                "Confirmation index cannot precede swing index."
            )

        if self.price <= 0:
            raise ValueError(
                "Price must be positive."
            )

    @property
    def is_high(self):

        return self.swing_type == SwingType.HIGH

    @property
    def is_low(self):

        return self.swing_type == SwingType.LOW