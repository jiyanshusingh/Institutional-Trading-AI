from models.order_block import OrderBlock
from models.origin_region import OriginRegion

from policies.order_block.order_block_policy import OrderBlockPolicy


class FullCandleOrderBlockPolicy(OrderBlockPolicy):

    def create(
        self,
        origin_region: OriginRegion,
        df
    ) -> OrderBlock:

        candle = df.iloc[origin_region.start_index]

        return OrderBlock(

            origin_region=origin_region,

            high=candle["High"],

            low=candle["Low"]

        )