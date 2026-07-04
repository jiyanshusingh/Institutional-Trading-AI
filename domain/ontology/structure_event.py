"""
Structure Event

Theory 1.0

A StructureEvent represents a confirmed structural event
produced by the Semantic Construction Pipeline.

Examples

- BOS
- CHOCH

A StructureEvent is immutable.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StructureEventType(Enum):
    """Types of structural events."""

    BOS = "BOS"
    CHOCH = "CHOCH"


class StructureDirection(Enum):
    """Direction of the structural event."""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


@dataclass(frozen=True, slots=True)
class StructureEvent:
    """
    Immutable semantic representation of a confirmed
    structural event.
    """

    event_id: int

    event_type: StructureEventType

    direction: StructureDirection

    timestamp: datetime

    candle_index: int

    broken_swing_index: int

    base_swing_index: int

    price: float

    displacement: float

    valid: bool = True

    def __post_init__(self):

        if self.event_id <= 0:
            raise ValueError(
                "Event ID must be positive."
            )

        if self.candle_index < 0:
            raise ValueError(
                "Candle index cannot be negative."
            )

        if self.broken_swing_index < 0:
            raise ValueError(
                "Broken swing index cannot be negative."
            )

        if self.base_swing_index < 0:
            raise ValueError(
                "Base swing index cannot be negative."
            )

        if self.price <= 0:
            raise ValueError(
                "Price must be positive."
            )

        if self.displacement < 0:
            raise ValueError(
                "Displacement cannot be negative."
            )