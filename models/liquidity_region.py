from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidityRegion:

    upper_price: float

    lower_price: float