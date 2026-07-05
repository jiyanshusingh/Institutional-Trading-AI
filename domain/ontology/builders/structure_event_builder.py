"""
Structure Event Builder

Constructs immutable StructureEvent objects from
confirmed StructureEvent candidates.
"""

from __future__ import annotations

from domain.market_observation.observation_history import (
    ObservationHistory,
)

from domain.ontology.swing import Swing

from domain.ontology.structure_event import (
    StructureEvent,
)

from domain.ontology.candidates.structure_event_candidate_detector import (
    StructureEventCandidateDetector,
)

from domain.ontology.policies.structure_event_confirmation_policy import (
    StructureEventConfirmationPolicy,
)


class StructureEventBuilder:
    """
    Builds immutable StructureEvent objects.

    This builder coordinates:

        ObservationHistory
                +
        Confirmed Swings
                ↓
        Candidate Detection
                ↓
        Confirmation
                ↓
        StructureEvent Construction
    """

    def __init__(
        self,
        detector: StructureEventCandidateDetector,
        confirmation_policy: StructureEventConfirmationPolicy,
    ):

        self._detector = detector
        self._confirmation_policy = confirmation_policy

    def build(
        self,
        observation_history: ObservationHistory,
        swings: tuple[Swing, ...],
    ) -> tuple[StructureEvent, ...]:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        if swings is None:
            raise ValueError(
                "Confirmed swings are required."
            )

        # ---------------------------------------------
        # Detect Candidates
        # ---------------------------------------------

        candidates = self._detector.detect(
            observation_history=observation_history,
            swings=swings,
        )

        # ---------------------------------------------
        # Confirm Candidates
        # ---------------------------------------------

        events: list[StructureEvent] = []

        event_id = 1

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate=candidate,
                observation_history=observation_history,
                swings=swings,
            )

            if not result.confirmed:
                continue

            events.append(

                StructureEvent(

                    event_id=event_id,

                    event_type=candidate.event_type,

                    direction=candidate.direction,

                    timestamp=candidate.timestamp,

                    candle_index=candidate.candle_index,

                    broken_swing_index=candidate.broken_swing_index,

                    base_swing_index=candidate.base_swing_index,

                    price=candidate.price,

                    displacement=candidate.displacement,

                )

            )

            event_id += 1

        return tuple(events)