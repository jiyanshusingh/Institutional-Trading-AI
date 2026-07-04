"""
Structure Event Candidate

Theory 1.0

Represents a potential StructureEvent discovered by the
candidate detector before confirmation.

A StructureEventCandidate contains only objective structural
facts. It carries no validity state and performs no
semantic interpretation.
"""

from dataclasses import dataclass
from datetime import datetime

from domain.ontology.structure_event import (
    StructureEventType,
    StructureDirection,
)


@dataclass(frozen=True, slots=True)
class StructureEventCandidate:
    """
    Immutable candidate for a StructureEvent.
    """

    event_type: StructureEventType

    direction: StructureDirection

    timestamp: datetime

    candle_index: int

    broken_swing_index: int

    base_swing_index: int

    price: float

    displacement: float

    def __post_init__(self):

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