from architecture.selection.candidate import Candidate
from assessments.market_configuration import MarketConfiguration
from models.origin_region import OriginRegion


class OriginRegionBuilder:

    def __init__(self):

        self.next_origin_region_id = 1

    def build(
        self,
        candidate: Candidate,
        expansion,
        configuration: MarketConfiguration
    ) -> OriginRegion:

        candle_index = candidate.subject

        candle = configuration.df.iloc[candle_index]

        origin_region = OriginRegion(

            id=self.next_origin_region_id,

            expansion_id=expansion.id,

            policy="ICT",

            start_index=candle_index,

            end_index=candle_index,

            low_price=candle["Low"],

            high_price=candle["High"]

        )

        self.next_origin_region_id += 1

        return origin_region