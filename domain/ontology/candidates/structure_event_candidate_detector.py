
"""
Structure Event Candidate Detector

Defines the contract for discovering
StructureEventCandidate objects from an
ObservationHistory.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.market_observation.observation_history import (
    ObservationHistory,
)

from domain.ontology.swing import Swing

from .structure_event_candidate import (
    StructureEventCandidate,
)


class StructureEventCandidateDetector(ABC):
    """
    Detects candidate Structure Events from an
    ObservationHistory and the already-confirmed swings.

    The detector only proposes candidates.

    Confirmation is performed by the
    StructureEventConfirmationPolicy.
    """

    @abstractmethod
    def detect(
        self,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> tuple[StructureEventCandidate, ...]:
        """
        Detect Structure Event candidates.

        Parameters
        ----------
        observation_history
            Raw immutable market observations.

        swings
            Confirmed swings produced by SwingBuilder.

        Returns
        -------
        tuple[StructureEventCandidate, ...]
            Candidate BOS / CHOCH events.
        """
        ...