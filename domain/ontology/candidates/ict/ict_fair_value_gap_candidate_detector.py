"""
ICT Fair Value Gap Candidate Detector

Theory 1.0

Detects Fair Value Gaps: three-candle imbalances where
the high of the first candle < low of the third (bullish)
or the low of the first > high of the third (bearish).

FVGs are detected within the context of origin regions.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)
from domain.ontology.fair_value_gap import FairValueGapDirection
from domain.ontology.candidates.fair_value_gap_candidate import (
    FairValueGapCandidate,
)
from domain.ontology.candidates.fair_value_gap_candidate_detector import (
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
            raise ValueError("CanonicalMarketModel is required.")

        if not model.origin_regions:
            return ()

        obs = model.observation_history.observations
        if len(obs) < 3:
            return ()

        candidates = []

        for i in range(len(obs) - 2):
            c1 = obs[i]
            c2 = obs[i + 1]
            c3 = obs[i + 2]

            if c1.high < c3.low:
                direction = FairValueGapDirection.BULLISH
            elif c1.low > c3.high:
                direction = FairValueGapDirection.BEARISH
            else:
                continue

            origin_idx = self._find_containing_origin_region(
                i, model.origin_regions
            )

            if direction == FairValueGapDirection.BULLISH:
                upper = c3.low
                lower = c1.high
            else:
                upper = c1.low
                lower = c3.high

            candidates.append(
                FairValueGapCandidate(
                    source_origin_region_index=origin_idx,
                    start_timestamp=c2.timestamp,
                    end_timestamp=c2.timestamp,
                    upper_price=upper,
                    lower_price=lower,
                    direction=direction,
                )
            )

        seen = set()
        unique = []
        for c in candidates:
            key = (c.upper_price, c.lower_price, c.direction.value)
            if key not in seen:
                seen.add(key)
                unique.append(c)

        return tuple(unique)

    def _find_containing_origin_region(
        self,
        candle_index: int,
        origin_regions,
    ) -> int:
        return 0 if origin_regions else -1