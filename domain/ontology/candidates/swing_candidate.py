"""
Swing Candidate

Represents a potential Swing prior to confirmation.

A SwingCandidate is NOT part of the ontology.
It is an intermediate construction artifact.
"""

from dataclasses import dataclass
from datetime import datetime

from domain.ontology.swing_type import SwingType


@dataclass(frozen=True, slots=True)
class SwingCandidate:

    index: int

    timestamp: datetime

    price: float

    swing_type: SwingType

    def __post_init__(self):

        if self.index < 0:
            raise ValueError("Index cannot be negative.")

        if self.price <= 0:
            raise ValueError("Price must be positive.")