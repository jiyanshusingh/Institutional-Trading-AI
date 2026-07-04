"""
ICT Protected Swing Candidate Detector

Theory 1.0

Placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from ..protected_swing_candidate import (
    ProtectedSwingCandidate,
)

from ..protected_swing_candidate_detector import (
    ProtectedSwingCandidateDetector,
)


class ICTProtectedSwingCandidateDetector(
    ProtectedSwingCandidateDetector
):

    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ProtectedSwingCandidate, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        return ()