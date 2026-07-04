"""
Protected Swing Builder

Constructs immutable ProtectedSwing objects from
confirmed ProtectedSwing candidates.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.protected_swing import (
    ProtectedSwing,
)

from domain.ontology.candidates.protected_swing_candidate_detector import (
    ProtectedSwingCandidateDetector,
)

from domain.ontology.policies.protected_swing_confirmation_policy import (
    ProtectedSwingConfirmationPolicy,
)


class ProtectedSwingBuilder:

    def __init__(
        self,
        detector: ProtectedSwingCandidateDetector,
        confirmation_policy: ProtectedSwingConfirmationPolicy,
    ):

        self._detector = detector
        self._confirmation_policy = confirmation_policy

    def build(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ProtectedSwing, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        candidates = self._detector.detect(
            model,
        )

        protected_swings = []

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate,
                model,
            )

            if not result.confirmed:
                continue

            protected_swings.append(

                ProtectedSwing(

                    swing_index=candidate.swing_index,

                    timestamp=candidate.timestamp,

                    price=candidate.price,

                    protected_type=candidate.protected_type,

                    protecting_event_index=(
                        candidate.protecting_event_index
                    ),
                )

            )

        return tuple(protected_swings)