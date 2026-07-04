"""
Canonical Market Model

Document 6 — Canonical Market Model Specification

The CanonicalMarketModel is the immutable value object representing the
complete canonical semantic interpretation of a single ObservationHistory
under a single declared Theory.

This object contains only established semantic constructs.
It performs no computation.
"""

from dataclasses import dataclass
from typing import Tuple, Any

from domain.market_observation.observation_history import ObservationHistory


@dataclass(frozen=True, slots=True)
class CanonicalMarketModel:
    """
    Immutable aggregate representing the complete semantic interpretation
    of one ObservationHistory.

    This object is produced only by the SemanticConstructionPipeline.
    """

    # ------------------------------------------------------------------
    # Observation Domain
    # ------------------------------------------------------------------

    observation_history: ObservationHistory

    # ------------------------------------------------------------------
    # Semantic Ontology
    # ------------------------------------------------------------------

    swings: Tuple[Any, ...] = ()

    structure_events: Tuple[Any, ...] = ()
    
    protected_swings: Tuple[Any, ...] = ()

    expansions: Tuple[Any, ...] = ()

    origin_regions: Tuple[Any, ...] = ()

    fair_value_gaps: Tuple[Any, ...] = ()

    # ------------------------------------------------------------------
    # Representations
    # ------------------------------------------------------------------

    order_blocks: Tuple[Any, ...] = ()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self):

        if self.observation_history is None:
            raise ValueError(
                "CanonicalMarketModel requires an ObservationHistory."
            )

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def symbol(self) -> str:
        return self.observation_history.metadata.symbol

    @property
    def timeframe(self) -> str:
        return self.observation_history.metadata.timeframe

    @property
    def observation_count(self) -> int:
        return len(self.observation_history)
    
    @property
    def swing_count(self) -> int:
        return len(self.swings)


    @property
    def structure_event_count(self) -> int:
        return len(self.structure_events)
    
    @property
    def protected_swing_count(self) -> int:
        return len(self.protected_swings)
    
    @property
    def expansion_count(self) -> int:
        return len(self.expansions)
    
    @property
    def origin_region_count(self) -> int:
        return len(self.origin_regions)
    
    @property
    def fair_value_gap_count(self) -> int:
        return len(self.fair_value_gaps)
    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    @property
    def summary(self) -> dict:

        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "observations": len(self.observation_history),
            "swings": len(self.swings),
            "structure_events": len(self.structure_events),
            "protected_swings": len(self.protected_swings),
            "expansions": len(self.expansions),
            "origin_regions": len(self.origin_regions),
            "fair_value_gaps": len(self.fair_value_gaps),
            "order_blocks": len(self.order_blocks),
        }