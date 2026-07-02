from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StructureEvent:

    event_id: int

    event_type: str

    direction: str

    timestamp: datetime

    candle_index: int

    broken_swing_index: int

    base_swing_index: int

    price: float

    valid: bool

    metadata: dict