"""
Expansion Confirmation Policy

Defines the contract for confirming
ExpansionCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.expansion_candidate import (
    ExpansionCandidate,
)

from .expansion_confirmation_result import (
    ExpansionConfirmationResult,
)


class ExpansionConfirmationPolicy(ABC):

    @abstractmethod
    def confirm(
        self,
        candidate: ExpansionCandidate,
        model: CanonicalMarketModel,
    ) -> ExpansionConfirmationResult:
        pass