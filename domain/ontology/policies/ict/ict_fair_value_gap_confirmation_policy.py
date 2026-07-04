"""
ICT Fair Value Gap Confirmation Policy

Theory 1.0

Initial placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.fair_value_gap_candidate import (
    FairValueGapCandidate,
)

from ..fair_value_gap_confirmation_policy import (
    FairValueGapConfirmationPolicy,
)

from ..fair_value_gap_confirmation_result import (
    FairValueGapConfirmationResult,
)


class ICTFairValueGapConfirmationPolicy(
    FairValueGapConfirmationPolicy
):

    def confirm(
        self,
        candidate: FairValueGapCandidate,
        model: CanonicalMarketModel,
    ) -> FairValueGapConfirmationResult:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        return FairValueGapConfirmationResult(
            confirmed=True,
            confirmation_index=(
                candidate.source_origin_region_index
            ),
        )