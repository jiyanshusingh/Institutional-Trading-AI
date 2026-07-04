"""
Expansion Candidate Detector

Defines the contract for discovering
ExpansionCandidate objects.
"""

from abc import ABC, abstractmethod

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from .expansion_candidate import (
    ExpansionCandidate,
)


class ExpansionCandidateDetector(ABC):

    @abstractmethod
    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ExpansionCandidate, ...]:
        """
        Detect expansion candidates.
        """
        pass