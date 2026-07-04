"""
Fair Value Gap Confirmation Policy

Defines the contract for confirming
FairValueGapCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.fair_value_gap_candidate import (
    FairValueGapCandidate,
)

from .fair_value_gap_confirmation_result import (
    FairValueGapConfirmationResult,
)


class FairValueGapConfirmationPolicy(ABC):

    @abstractmethod
    def confirm(
        self,
        candidate: FairValueGapCandidate,
        model: CanonicalMarketModel,
    ) -> FairValueGapConfirmationResult:
        pass