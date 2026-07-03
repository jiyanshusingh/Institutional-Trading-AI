from architecture.selection.candidate import Candidate

from models.origin_region import OriginRegion
from models.order_block import OrderBlock


class OrderBlockBuilder:

    def build(
        self,
        origin_region: OriginRegion,
        candidate: Candidate
    ) -> OrderBlock:

        geometry = candidate.subject

        return OrderBlock(

            origin_region=origin_region,

            high_price=geometry.high_price,

            low_price=geometry.low_price

        )