"""
Origin Region Candidate Detector

Defines the contract for discovering
OriginRegionCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from .origin_region_candidate import (
    OriginRegionCandidate,
)


class OriginRegionCandidateDetector(ABC):

    @abstractmethod
    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[OriginRegionCandidate, ...]:
        """
        Detect Origin Region candidates.
        """
        pass