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

from __future__ import annotations

from domain.market_observation.observation_history import (
    ObservationHistory,
)

from domain.ontology.swing import Swing

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
    """
    ICT Structure Event Confirmation Policy.

    Version 2 currently accepts every candidate.

    The actual ICT confirmation rules
    (close beyond swing, displacement, etc.)
    will be implemented later.
    """

    def confirm(
        self,
        candidate: StructureEventCandidate,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> StructureEventConfirmationResult:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        if swings is None:
            raise ValueError(
                "Confirmed swings are required."
            )

        #
        # Version 2
        # Real ICT confirmation logic
        # will be implemented later.
        #

        return StructureEventConfirmationResult(
            confirmed=True,
            confirmation_index=candidate.candle_index,
        )