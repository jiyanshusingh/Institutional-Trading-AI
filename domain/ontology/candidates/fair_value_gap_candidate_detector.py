"""
Fair Value Gap Candidate Detector

Defines the contract for discovering
FairValueGapCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from .fair_value_gap_candidate import (
    FairValueGapCandidate,
)


class FairValueGapCandidateDetector(ABC):

    @abstractmethod
    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[FairValueGapCandidate, ...]:
        """
        Detect Fair Value Gap candidates.
        """
        pass