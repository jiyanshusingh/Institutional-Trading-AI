"""
Origin Region Builder

Constructs immutable OriginRegion objects from
confirmed OriginRegion candidates.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.origin_region import (
    OriginRegion,
)

from domain.ontology.candidates.origin_region_candidate_detector import (
    OriginRegionCandidateDetector,
)

from domain.ontology.policies.origin_region_confirmation_policy import (
    OriginRegionConfirmationPolicy,
)


class OriginRegionBuilder:

    def __init__(
        self,
        detector: OriginRegionCandidateDetector,
        confirmation_policy: OriginRegionConfirmationPolicy,
    ):

        self._detector = detector
        self._confirmation_policy = confirmation_policy

    def build(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[OriginRegion, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        candidates = self._detector.detect(
            model,
        )

        origin_regions = []

        for candidate in candidates:

            result = self._confirmation_policy.confirm(
                candidate,
                model,
            )

            if not result.confirmed:
                continue

            origin_regions.append(

                OriginRegion(

                    source_expansion_index=(
                        candidate.source_expansion_index
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

        return tuple(origin_regions)