from dataclasses import dataclass


@dataclass(frozen=True)
class OrderBlockGeometry:

    high_price: float

    low_price: float