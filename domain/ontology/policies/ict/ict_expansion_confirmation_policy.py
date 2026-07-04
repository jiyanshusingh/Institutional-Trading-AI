"""
ICT Expansion Confirmation Policy

Theory 1.0

Initial placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.expansion_candidate import (
    ExpansionCandidate,
)

from ..expansion_confirmation_policy import (
    ExpansionConfirmationPolicy,
)

from ..expansion_confirmation_result import (
    ExpansionConfirmationResult,
)


class ICTExpansionConfirmationPolicy(
    ExpansionConfirmationPolicy
):

    def confirm(
        self,
        candidate: ExpansionCandidate,
        model: CanonicalMarketModel,
    ) -> ExpansionConfirmationResult:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        return ExpansionConfirmationResult(
            confirmed=True,
            confirmation_index=(
                candidate.confirmation_event_index
            ),
        )