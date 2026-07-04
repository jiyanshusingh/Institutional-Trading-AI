"""
Trade Candidate

Theory 1.0

Represents an explainable trading opportunity generated from a
MarketInterpretation.

A TradeCandidate is a hypothesis.

It is not an executed trade.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TradeDirection(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass(frozen=True, slots=True)
class TradeCandidate:
    """
    Immutable trading opportunity.
    """

    symbol: str

    direction: TradeDirection

    entry_price: float

    stop_loss: float

    target_price: float

    confidence: float

    expected_reward_risk: float

    generated_timestamp: datetime

    reasoning: tuple[str, ...]

    def __post_init__(self):

        if not self.symbol:
            raise ValueError(
                "Symbol cannot be empty."
            )

        if self.entry_price <= 0:
            raise ValueError(
                "Entry price must be positive."
            )

        if self.stop_loss <= 0:
            raise ValueError(
                "Stop loss must be positive."
            )

        if self.target_price <= 0:
            raise ValueError(
                "Target price must be positive."
            )

        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                "Confidence must be between 0.0 and 1.0."
            )

        if self.expected_reward_risk <= 0:
            raise ValueError(
                "Expected reward-risk must be positive."
            )

        if len(self.reasoning) == 0:
            raise ValueError(
                "Reasoning cannot be empty."
            )

    @property
    def is_long(self) -> bool:
        return self.direction == TradeDirection.LONG

    @property
    def is_short(self) -> bool:
        return self.direction == TradeDirection.SHORT