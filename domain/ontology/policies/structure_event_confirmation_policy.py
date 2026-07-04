"""
Structure Event Confirmation Policy

Defines the contract for confirming
StructureEventCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.market_observation.observation_history import ObservationHistory

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from .structure_event_confirmation_result import (
    StructureEventConfirmationResult,
)


class StructureEventConfirmationPolicy(ABC):

    @abstractmethod
    def confirm(
        self,
        candidate: StructureEventCandidate,
        observation_history: ObservationHistory,
    ) -> StructureEventConfirmationResult:
        pass