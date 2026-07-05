"""
ICT Structure Event Candidate Detector

Theory 1.0

Detects candidate BOS and CHOCH events from
confirmed swings.

Commit 1

- Validate inputs
- Iterate confirmed swings
- No BOS detection yet
"""

from __future__ import annotations

from domain.market_observation.observation_history import (
    ObservationHistory,
)

from domain.ontology.swing import Swing
from domain.ontology.swing import SwingType

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from ..structure_event_candidate_detector import (
    StructureEventCandidateDetector,
)


class ICTStructureEventCandidateDetector(
    StructureEventCandidateDetector
):
    """
    Version 1
    Commit 1

    Traverses confirmed swings.

    No BOS candidates are produced yet.
    """

    def detect(
        self,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> tuple[StructureEventCandidate, ...]:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        if swings is None:
            raise ValueError(
                "Confirmed swings are required."
            )

        if len(swings) == 0:
            return ()

        candidates: list[StructureEventCandidate] = []

        #
        # Commit 1
        #
        # Traverse swings only.
        #
        for swing in swings:

            #
            # Bullish BOS will use HIGH swings.
            #
            if swing.swing_type == SwingType.HIGH:
                continue

            #
            # Bearish BOS will use LOW swings.
            #
            if swing.swing_type == SwingType.LOW:
                continue

        return tuple(candidates)