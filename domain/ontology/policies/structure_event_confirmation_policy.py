"""
Structure Event Confirmation Policy

Defines the contract for confirming
StructureEventCandidate objects.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.market_observation.observation_history import (
    ObservationHistory,
)

from domain.ontology.swing import Swing

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from .structure_event_confirmation_result import (
    StructureEventConfirmationResult,
)


class StructureEventConfirmationPolicy(ABC):
    """
    Confirms candidate Structure Events.

    The confirmation policy validates whether a
    candidate satisfies the ICT Structure Event
    confirmation rules.
    """

    @abstractmethod
    def confirm(
        self,
        candidate: StructureEventCandidate,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> StructureEventConfirmationResult:
        """
        Confirm a candidate Structure Event.

        Parameters
        ----------
        candidate
            Candidate produced by the detector.

        observation_history
            Immutable market observations.

        swings
            Confirmed swings produced by SwingBuilder.

        Returns
        -------
        StructureEventConfirmationResult
        """
        ...