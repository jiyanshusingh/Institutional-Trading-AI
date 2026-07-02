from dataclasses import dataclass


@dataclass(frozen=True)
class Expansion:

    id: int

    segment_id: int

    direction: str

    base_swing_index: int

    bos_event_id: int