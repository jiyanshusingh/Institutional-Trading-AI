from dataclasses import dataclass


@dataclass(frozen=True)
class FairValueGap:

    start_index: int

    middle_index: int

    end_index: int

    upper_price: float

    lower_price: float

    direction: str

    policy: str