from engines.origin_region_builder import OriginRegionBuilder

from policies.origin_region.base_origin_region_policy import (
    OriginRegionPolicy
)

from policies.origin_region.ict.ict_origin_candidate_generator import (
    ICTOriginCandidateGenerator
)

from policies.origin_region.ict.ict_origin_selection_policy import (
    ICTOriginSelectionPolicy
)


class ICTOriginRegionPolicy(
    OriginRegionPolicy
):

    def __init__(self):

        self.generator = ICTOriginCandidateGenerator()

        self.selector = ICTOriginSelectionPolicy()

        self.builder = OriginRegionBuilder()

    def locate(
        self,
        expansion,
        configuration
    ):

        candidates = self.generator.generate(
            expansion,
            configuration
        )

        selected = self.selector.select(
            candidates
        )

        if selected is None:
            return None

        return self.builder.build(
            selected,
            expansion,
            configuration
        )

    def _search_window(
        self,
        expansion,
        configuration
    ):
        pass

    def _candidate_candles(
        self,
        window,
        configuration
    ):
        pass

    def _select_origin_candle(
        self,
        candidates
    ):
        pass

    def _build_origin_region(
        self,
        candle,
        expansion
    ):
        pass