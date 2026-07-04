"""
ICT Structure Event Candidate Detector

Theory 1.0

Current implementation is a placeholder.

Structure Event detection will be migrated
from the legacy engine incrementally.
"""

from domain.market_observation.observation_history import ObservationHistory

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from ..structure_event_candidate_detector import (
    StructureEventCandidateDetector,
)


class ICTStructureEventCandidateDetector(
    StructureEventCandidateDetector
):

    def detect(
        self,
        observation_history: ObservationHistory,
    ) -> tuple[StructureEventCandidate, ...]:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        return ()