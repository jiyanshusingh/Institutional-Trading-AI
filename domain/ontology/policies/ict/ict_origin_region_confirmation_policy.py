"""
ICT Origin Region Confirmation Policy

Theory 1.0

Initial placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.origin_region_candidate import (
    OriginRegionCandidate,
)

from ..origin_region_confirmation_policy import (
    OriginRegionConfirmationPolicy,
)

from ..origin_region_confirmation_result import (
    OriginRegionConfirmationResult,
)


class ICTOriginRegionConfirmationPolicy(
    OriginRegionConfirmationPolicy
):

    def confirm(
        self,
        candidate: OriginRegionCandidate,
        model: CanonicalMarketModel,
    ) -> OriginRegionConfirmationResult:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        return OriginRegionConfirmationResult(
            confirmed=True,
            confirmation_index=(
                candidate.source_expansion_index
            ),
        )