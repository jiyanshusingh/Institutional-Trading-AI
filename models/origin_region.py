from dataclasses import dataclass
@dataclass(frozen=True)
class OriginRegion:

    id: int

    expansion_id: int

    policy: str

    start_index: int

    end_index: int

    low_price: float

    high_price: float