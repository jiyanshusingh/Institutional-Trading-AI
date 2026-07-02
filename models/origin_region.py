from dataclasses import dataclass


@dataclass(frozen=True)
class OriginRegion:

    start_index: int

    end_index: int