"""
Expansion Builder

Constructs immutable Expansion objects from
confirmed Expansion candidates.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.expansion import (
    Expansion,
)

from domain.ontology.candidates.expansion_candidate_detector import (
    ExpansionCandidateDetector,
)

from domain.ontology.policies.expansion_confirmation_policy import (
    ExpansionConfirmationPolicy,
)


class ExpansionBuilder:

    def __init__(
        self,
        detector: ExpansionCandidateDetector,
        confirmation_policy: ExpansionConfirmationPolicy,
    ):

        self._detector = detector
        self._confirmation_policy = confirmation_policy

    def build(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[Expansion, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        candidates = self._detector.detect(
            model,
        )

        expansions = []

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate,
                model,
            )

            if not result.confirmed:
                continue

            expansions.append(

                Expansion(

                    base_swing_index=candidate.base_swing_index,

                    confirmation_event_index=(
                        candidate.confirmation_event_index
                    ),

                    start_timestamp=candidate.start_timestamp,

                    end_timestamp=candidate.end_timestamp,

                    start_price=candidate.start_price,

                    end_price=candidate.end_price,

                    direction=candidate.direction,

                )

            )

        return tuple(expansions)