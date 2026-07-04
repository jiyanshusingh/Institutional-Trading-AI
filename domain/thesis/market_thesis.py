from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Tuple
@dataclass(frozen=True, slots=True)
class MarketThesis:

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    thesis_id: str
    created_at: datetime

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    symbol: str
    timeframe: str

    reasoning_model: str
    theory: str
    version: str

    # ------------------------------------------------------------------
    # Scope
    # ------------------------------------------------------------------

    market_regime: str
    session: str

    # ------------------------------------------------------------------
    # Core Thesis (required)
    # ------------------------------------------------------------------

    central_claim: str

    # ------------------------------------------------------------------
    # Optional fields (defaults start here)
    # ------------------------------------------------------------------

    objectives: Tuple[str, ...] = field(default_factory=tuple)

    supporting_evidence: Tuple[str, ...] = field(default_factory=tuple)

    counter_evidence: Tuple[str, ...] = field(default_factory=tuple)

    assumptions: Tuple[str, ...] = field(default_factory=tuple)

    expected_structural_evolution: str = ""

    invalidation: Tuple[str, ...] = field(default_factory=tuple)

    uncertainty: str = "UNKNOWN"
    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def has_counter_evidence(self) -> bool:
        return len(self.counter_evidence) > 0

    def has_assumptions(self) -> bool:
        return len(self.assumptions) > 0

    def is_falsifiable(self) -> bool:
        return len(self.invalidation) > 0

    def evidence_count(self) -> int:
        return len(self.supporting_evidence)

    def counter_evidence_count(self) -> int:
        return len(self.counter_evidence)

    def summary(self) -> str:
        return (
            f"{self.symbol} [{self.timeframe}] - "
            f"{self.central_claim}"
        )

    def __str__(self) -> str:
        return (
            f"MarketThesis("
            f"symbol={self.symbol}, "
            f"timeframe={self.timeframe}, "
            f"claim='{self.central_claim}')"
        )