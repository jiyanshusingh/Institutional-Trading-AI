"""
ICT Origin Region Candidate Detector

Theory 1.0

Detects origin regions: the price region from which
a confirmed expansion originated.

For an expansion, the origin region encompasses the
consolidation zone around the base swing area.
"""

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)
from domain.ontology.origin_region import OriginRegionDirection
from domain.ontology.candidates.origin_region_candidate import (
    OriginRegionCandidate,
)
from domain.ontology.candidates.origin_region_candidate_detector import (
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
            raise ValueError("CanonicalMarketModel is required.")

        if not model.expansions:
            return ()

        candidates = []
        obs = model.observation_history.observations

        for expansion in model.expansions:
            base_idx = expansion.base_swing_index

            upper = expansion.start_price
            lower = expansion.start_price

            lookback_start = max(0, base_idx - 5)

            for swing in model.swings:
                if lookback_start <= swing.index <= base_idx:
                    upper = max(upper, swing.price)
                    lower = min(lower, swing.price)

            for i in range(lookback_start, min(base_idx + 1, len(obs))):
                candle = obs[i]
                upper = max(upper, candle.high)
                lower = min(lower, candle.low)

            direction = (
                OriginRegionDirection.BULLISH
                if expansion.is_bullish
                else OriginRegionDirection.BEARISH
            )

            candidates.append(
                OriginRegionCandidate(
                    source_expansion_index=expansion.confirmation_event_index,
                    start_timestamp=obs[lookback_start].timestamp,
                    end_timestamp=obs[base_idx].timestamp,
                    upper_price=upper,
                    lower_price=lower,
                    direction=direction,
                )
            )

        return tuple(candidates)