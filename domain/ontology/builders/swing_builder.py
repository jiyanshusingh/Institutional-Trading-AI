"""
Swing Builder

Constructs immutable Swing objects from
confirmed Swing candidates.
"""

from domain.market_observation.observation_history import ObservationHistory

from domain.ontology.swing import Swing

from domain.ontology.candidates.swing_candidate_detector import (
    SwingCandidateDetector,
)

from domain.ontology.policies.swing_confirmation_policy import (
    SwingConfirmationPolicy,
)
from domain.ontology.calculations.swing_strength_calculator import (
    SwingStrengthCalculator,
)


class SwingBuilder:

    def __init__(
        self,
        detector: SwingCandidateDetector,
        confirmation_policy: SwingConfirmationPolicy,
    ):

        self._detector = detector
        self._confirmation_policy = confirmation_policy

    def build(
        self,
        observation_history: ObservationHistory,
    ) -> tuple[Swing, ...]:

        candidates = self._detector.detect(
            observation_history
        )

        swings = []

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate,
                observation_history,
            )

            if not result.confirmed:
                continue

            swings.append(

                Swing(

                    index=candidate.index,

                    confirmation_index=result.confirmation_index,

                    timestamp=candidate.timestamp,

                    price=candidate.price,

                    swing_type=candidate.swing_type,
                )

            )

        return tuple(swings)