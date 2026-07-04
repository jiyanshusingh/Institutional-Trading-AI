"""
Protected Swing Candidate

Theory 1.0

Represents a potential ProtectedSwing before
confirmation.

A candidate is discovered from existing semantic
constructs but is not yet authoritative.
"""

from dataclasses import dataclass
from datetime import datetime

from domain.ontology.protected_swing import (
    ProtectedSwingType,
)


@dataclass(frozen=True, slots=True)
class ProtectedSwingCandidate:

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