from dataclasses import dataclass


@dataclass(frozen=True)
class FairValueGap:

    upper_price: float

    lower_price: float
    