from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:

    id: int

    direction: str

    start_event_id: int

    end_event_id: int | None

    start_index: int

    end_index: int | None