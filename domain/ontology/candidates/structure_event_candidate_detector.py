
"""
Structure Event Candidate Detector

Defines the contract for discovering
StructureEventCandidate objects from an
ObservationHistory.
"""

from abc import ABC, abstractmethod

from domain.market_observation.observation_history import ObservationHistory

from .structure_event_candidate import (
    StructureEventCandidate,
)


class StructureEventCandidateDetector(ABC):

    @abstractmethod
    def detect(
        self,
        observation_history: ObservationHistory,
    ) -> tuple[StructureEventCandidate, ...]:
        """
        Detect structure event candidates.

        Returns
        -------
        tuple[StructureEventCandidate, ...]
        """
        pass