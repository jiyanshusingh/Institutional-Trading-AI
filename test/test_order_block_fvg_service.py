from models.origin_region import OriginRegion
from models.order_block import OrderBlock
from models.fair_value_gap import FairValueGap

from services.confluence.order_block_fvg_service import (
    OrderBlockFVGService
)

service = OrderBlockFVGService()

dummy_origin = OriginRegion(
    start_index=0,
    end_index=0
)

# -----------------------------------
# Case 1 : Full Overlap
# -----------------------------------

order_blocks = [
    OrderBlock(
        origin_region=dummy_origin,
        high=710,
        low=700
    )
]

fair_value_gaps = [
    FairValueGap(
        upper_price=708,
        lower_price=705
    )
]

overlaps = service.find_overlaps(
    order_blocks,
    fair_value_gaps
)

assert len(overlaps) == 1


# -----------------------------------
# Case 2 : No Overlap
# -----------------------------------

fair_value_gaps = [
    FairValueGap(
        upper_price=715,
        lower_price=711
    )
]

overlaps = service.find_overlaps(
    order_blocks,
    fair_value_gaps
)

assert len(overlaps) == 0


# -----------------------------------
# Case 3 : Boundary Touch
# -----------------------------------

fair_value_gaps = [
    FairValueGap(
        upper_price=715,
        lower_price=710
    )
]

overlaps = service.find_overlaps(
    order_blocks,
    fair_value_gaps
)

assert len(overlaps) == 1


# -----------------------------------
# Case 4 : FVG Contains Order Block
# -----------------------------------

order_blocks = [
    OrderBlock(
        origin_region=dummy_origin,
        high=708,
        low=705
    )
]

fair_value_gaps = [
    FairValueGap(
        upper_price=710,
        lower_price=700
    )
]

overlaps = service.find_overlaps(
    order_blocks,
    fair_value_gaps
)

assert len(overlaps) == 1


print("\n✅ OrderBlockFVGService tests passed.")