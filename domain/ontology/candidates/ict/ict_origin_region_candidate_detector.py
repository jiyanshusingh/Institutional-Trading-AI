"""
ICT Origin Region Candidate Detector

Theory 1.0

Initial placeholder implementation.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from ..origin_region_candidate import (
    OriginRegionCandidate,
)

from ..origin_region_candidate_detector import (
    OriginRegionCandidateDetector,
)


class ICTOriginRegionCandidateDetector(
    OriginRegionCandidateDetector
):

    def detect(
        self,
        model: CanonicalMarketModel,
    ) -> tuple[OriginRegionCandidate, ...]:

        if model is None:
            raise ValueError(
                "CanonicalMarketModel is required."
            )

        #
        # Theory 1.0 placeholder
        #

        return ()