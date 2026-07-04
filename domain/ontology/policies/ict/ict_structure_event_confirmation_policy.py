"""
ICT Structure Event Confirmation Policy

Theory 1.0

Current implementation confirms every
candidate immediately.

Later versions will include:

- BOS validation
- CHOCH validation
- Protected Swing validation
- Theory-specific rules
"""

from domain.market_observation.observation_history import ObservationHistory

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from ..structure_event_confirmation_policy import (
    StructureEventConfirmationPolicy,
)

from ..structure_event_confirmation_result import (
    StructureEventConfirmationResult,
)


class ICTStructureEventConfirmationPolicy(
    StructureEventConfirmationPolicy
):

    def confirm(
        self,
        candidate: StructureEventCandidate,
        observation_history: ObservationHistory,
    ) -> StructureEventConfirmationResult:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        return StructureEventConfirmationResult(
            confirmed=True,
            confirmation_index=candidate.candle_index,
        )