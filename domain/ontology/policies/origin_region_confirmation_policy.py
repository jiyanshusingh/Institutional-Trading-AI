"""
Origin Region Confirmation Policy

Defines the contract for confirming
OriginRegionCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.origin_region_candidate import (
    OriginRegionCandidate,
)

from .origin_region_confirmation_result import (
    OriginRegionConfirmationResult,
)


class OriginRegionConfirmationPolicy(ABC):

    @abstractmethod
    def confirm(
        self,
        candidate: OriginRegionCandidate,
        model: CanonicalMarketModel,
    ) -> OriginRegionConfirmationResult:
        pass