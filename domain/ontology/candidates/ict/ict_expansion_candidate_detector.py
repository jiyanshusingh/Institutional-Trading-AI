"""
ICT Expansion Candidate Detector

Theory 1.0

Initial placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from ..expansion_candidate import (
    ExpansionCandidate,
)

from ..expansion_candidate_detector import (
    ExpansionCandidateDetector,
)


class ICTExpansionCandidateDetector(
    ExpansionCandidateDetector
):

    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[ExpansionCandidate, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        #
        # Theory 1.0 placeholder
        #

        return ()