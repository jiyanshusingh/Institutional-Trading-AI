"""
Fair Value Gap Builder

Constructs immutable FairValueGap objects from
confirmed FairValueGap candidates.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.fair_value_gap import (
    FairValueGap,
)

from domain.ontology.candidates.fair_value_gap_candidate_detector import (
    FairValueGapCandidateDetector,
)

from domain.ontology.policies.fair_value_gap_confirmation_policy import (
    FairValueGapConfirmationPolicy,
)


class FairValueGapBuilder:

    def __init__(
        self,
        detector: FairValueGapCandidateDetector,
        confirmation_policy: FairValueGapConfirmationPolicy,
    ):

        self._detector = detector
        self._confirmation_policy = confirmation_policy

    def build(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[FairValueGap, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        candidates = self._detector.detect(
            model,
        )

        fair_value_gaps = []

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate,
                model,
            )

            if not result.confirmed:
                continue

            fair_value_gaps.append(

                FairValueGap(

                    source_origin_region_index=(
                        candidate.source_origin_region_index
                    ),

                    start_timestamp=(
                        candidate.start_timestamp
                    ),

                    end_timestamp=(
                        candidate.end_timestamp
                    ),

                    upper_price=(
                        candidate.upper_price
                    ),

                    lower_price=(
                        candidate.lower_price
                    ),

                    direction=(
                        candidate.direction
                    ),

                )

            )

        return tuple(fair_value_gaps)