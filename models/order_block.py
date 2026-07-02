from dataclasses import dataclass

from models.origin_region import OriginRegion


@dataclass(frozen=True)
class OrderBlock:

    origin_region: OriginRegion

    high: float

    low: float