from dataclasses import dataclass
from typing import Tuple

from .market_observation import MarketObservation
from .observation_metadata import ObservationMetadata


@dataclass(frozen=True, slots=True)
class ObservationHistory:
    """
    Immutable value object representing one observation history.

    This object contains observations only.
    It performs no semantic interpretation.
    """

    observations: Tuple[MarketObservation, ...]
    metadata: ObservationMetadata
    
    def __post_init__(self):

        if len(self.observations) == 0:
            raise ValueError(
                "Observation history cannot be empty."
            )

    def __len__(self) -> int:
        return len(self.observations)

    def __iter__(self):
        return iter(self.observations)

    def __getitem__(self, index: int) -> MarketObservation:
        return self.observations[index]

    @property
    def first(self) -> MarketObservation:
        return self.observations[0]

    @property
    def last(self) -> MarketObservation:
        return self.observations[-1]