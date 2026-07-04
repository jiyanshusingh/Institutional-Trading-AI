"""
Protected Swing Confirmation Policy

Defines the contract for confirming
ProtectedSwingCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.protected_swing_candidate import (
    ProtectedSwingCandidate,
)

from .protected_swing_confirmation_result import (
    ProtectedSwingConfirmationResult,
)


class ProtectedSwingConfirmationPolicy(ABC):

    @abstractmethod
    def confirm(
        self,
        candidate: ProtectedSwingCandidate,
        model: CanonicalMarketModel,
    ) -> ProtectedSwingConfirmationResult:
        pass