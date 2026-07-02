from dataclasses import dataclass

from models.order_block import OrderBlock
from models.fair_value_gap import FairValueGap


@dataclass(frozen=True)
class OrderBlockFVGOverlap:

    order_block: OrderBlock

    fair_value_gap: FairValueGap