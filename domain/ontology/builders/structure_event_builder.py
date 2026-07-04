"""
Structure Event Builder

Constructs immutable StructureEvent objects from
confirmed StructureEvent candidates.
"""

from domain.market_observation.observation_history import (
    ObservationHistory,
)

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
    ) -> tuple[StructureEvent, ...]:

        if observation_history is None:
            raise ValueError(
                "ObservationHistory is required."
            )

        candidates = self._detector.detect(
            observation_history
        )

        events = []

        event_id = 1

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate,
                observation_history,
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