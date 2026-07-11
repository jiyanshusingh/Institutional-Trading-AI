"""
ICT Protected Swing Candidate Detector

Theory 1.0

Detects protected swings: when a structure event
(BOS/CHOCH) breaks a swing high or low, that swing
becomes protected — it represents the last structural
point before the break.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)
from domain.ontology.swing_type import SwingType
from domain.ontology.protected_swing import ProtectedSwingType
from domain.ontology.candidates.protected_swing_candidate import (
    ProtectedSwingCandidate,
)
from domain.ontology.candidates.protected_swing_candidate_detector import (
    ProtectedSwingCandidateDetector,
)


class ICTProtectedSwingCandidateDetector(
    ProtectedSwingCandidateDetector
):

    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ProtectedSwingCandidate, ...]:

        if model is None:
            raise ValueError("CanonicalMarketModel is required.")

        if not model.structure_events or not model.swings:
            return ()

        swing_map = {s.index: s for s in model.swings}
        candidates = []

        for event in model.structure_events:
            if not event.valid:
                continue

            broken_swing = swing_map.get(event.broken_swing_index)
            if broken_swing is None:
                continue

            protected_type = (
                ProtectedSwingType.HIGH
                if broken_swing.swing_type == SwingType.HIGH
                else ProtectedSwingType.LOW
            )

            candidates.append(
                ProtectedSwingCandidate(
                    swing_index=broken_swing.index,
                    timestamp=broken_swing.timestamp,
                    price=broken_swing.price,
                    protected_type=protected_type,
                    protecting_event_index=event.event_id,
                )
            )

        return tuple(candidates)