"""
ICT Expansion Candidate Detector

Theory 1.0

Detects expansions: structural movements that begin at
a base swing and end at a confirming structure event.

Bullish Expansion: base swing low → bullish BOS/CHOCH
Bearish Expansion: base swing high → bearish BOS/CHOCH
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)
from domain.ontology.expansion import ExpansionDirection
from domain.ontology.swing_type import SwingType
from domain.ontology.structure_event import StructureDirection
from domain.ontology.candidates.expansion_candidate import (
    ExpansionCandidate,
)
from domain.ontology.candidates.expansion_candidate_detector import (
    ExpansionCandidateDetector,
)


class ICTExpansionCandidateDetector(
    ExpansionCandidateDetector
):

    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ExpansionCandidate, ...]:

        if model is None:
            raise ValueError("CanonicalMarketModel is required.")

        if not model.structure_events or not model.swings:
            return ()

        swing_map = {s.index: s for s in model.swings}
        candidates = []

        for event in model.structure_events:
            if not event.valid:
                continue

            base_swing = swing_map.get(event.base_swing_index)
            if base_swing is None:
                continue

            if event.direction == StructureDirection.BULLISH:
                direction = ExpansionDirection.BULLISH
            elif event.direction == StructureDirection.BEARISH:
                direction = ExpansionDirection.BEARISH
            else:
                continue

            candidates.append(
                ExpansionCandidate(
                    base_swing_index=base_swing.index,
                    confirmation_event_index=event.event_id,
                    start_timestamp=base_swing.timestamp,
                    end_timestamp=event.timestamp,
                    start_price=base_swing.price,
                    end_price=event.price,
                    direction=direction,
                )
            )

        return tuple(candidates)