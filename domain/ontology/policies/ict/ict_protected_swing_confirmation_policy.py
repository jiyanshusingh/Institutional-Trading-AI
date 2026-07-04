"""
ICT Protected Swing Confirmation Policy

Theory 1.0

Initial placeholder implementation.

Every candidate is confirmed immediately.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.protected_swing_candidate import (
    ProtectedSwingCandidate,
)

from ..protected_swing_confirmation_policy import (
    ProtectedSwingConfirmationPolicy,
)

from ..protected_swing_confirmation_result import (
    ProtectedSwingConfirmationResult,
)


class ICTProtectedSwingConfirmationPolicy(
    ProtectedSwingConfirmationPolicy
):

    def confirm(
        self,
        candidate: ProtectedSwingCandidate,
        model: CanonicalMarketModel,
    ) -> ProtectedSwingConfirmationResult:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        return ProtectedSwingConfirmationResult(
            confirmed=True,
            confirmation_index=candidate.protecting_event_index,
        )