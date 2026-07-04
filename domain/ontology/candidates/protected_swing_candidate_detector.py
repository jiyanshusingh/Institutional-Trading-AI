"""
Protected Swing Candidate Detector

Defines the contract for discovering
ProtectedSwingCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from .protected_swing_candidate import (
    ProtectedSwingCandidate,
)


class ProtectedSwingCandidateDetector(ABC):

    @abstractmethod
    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ProtectedSwingCandidate, ...]:
        pass