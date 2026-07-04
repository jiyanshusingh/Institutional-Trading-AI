"""
ICT Fair Value Gap Candidate Detector

Theory 1.0

Initial placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from ..fair_value_gap_candidate import (
    FairValueGapCandidate,
)

from ..fair_value_gap_candidate_detector import (
    FairValueGapCandidateDetector,
)


class ICTFairValueGapCandidateDetector(
    FairValueGapCandidateDetector
):

    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[FairValueGapCandidate, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        #
        # Theory 1.0 placeholder
        #

        return ()