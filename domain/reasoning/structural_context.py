from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True, slots=True)
class StructuralContext:
    """
    Immutable description of the current structural organization
    of the market.

    This is an intermediate reasoning artifact.

    It does NOT predict the future.
    It does NOT generate trades.
    It simply answers:

        "What structural situation currently exists?"
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    context: str

    # ------------------------------------------------------------------
    # Structural State
    # ------------------------------------------------------------------

    dominant_expansion: str

    protected_structure: str

    latest_structure_event: str

    # ------------------------------------------------------------------
    # Reasoning Notes
    # ------------------------------------------------------------------

    observations: Tuple[str, ...] = field(default_factory=tuple)

    confidence_notes: Tuple[str, ...] = field(default_factory=tuple)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def is_bullish(self) -> bool:
        return "bullish" in self.context.lower()

    def is_bearish(self) -> bool:
        return "bearish" in self.context.lower()

    def is_transition(self) -> bool:
        return self.context.lower() == "transition"

    def observation_count(self) -> int:
        return len(self.observations)

    def summary(self) -> str:
        return (
            f"{self.context} | "
            f"Expansion: {self.dominant_expansion}"
        )

    def __str__(self) -> str:
        return (
            f"StructuralContext("
            f"context='{self.context}', "
            f"expansion='{self.dominant_expansion}')"
        )