"""
Protected Swing

Theory 1.0

A ProtectedSwing is an immutable semantic construct representing
the currently protected structural swing established by a confirmed
StructureEvent.

A ProtectedSwing is derived from existing semantic constructs.
It performs no computation.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ProtectedSwingType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"


@dataclass(frozen=True, slots=True)
class ProtectedSwing:
    """
    Immutable Protected Swing.
    """

    swing_index: int

    timestamp: datetime

    price: float

    protected_type: ProtectedSwingType

    protecting_event_index: int

    def __post_init__(self):

        if self.swing_index < 0:
            raise ValueError(
                "Swing index cannot be negative."
            )

        if self.protecting_event_index < 0:
            raise ValueError(
                "Protecting event index cannot be negative."
            )

        if self.price <= 0:
            raise ValueError(
                "Price must be positive."
            )

    @property
    def is_high(self) -> bool:
        return (
            self.protected_type
            == ProtectedSwingType.HIGH
        )

    @property
    def is_low(self) -> bool:
        return (
            self.protected_type
            == ProtectedSwingType.LOW
        )