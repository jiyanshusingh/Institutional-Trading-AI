from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ObservationMetadata:
    """
    Metadata describing an ObservationHistory.
    """

    symbol: str
    timeframe: str

    start_time: datetime
    end_time: datetime

    observation_count: int

    source: str | None = None
    schema_version: str = "1.0"
    
    def __post_init__(self):

        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if not self.timeframe.strip():
            raise ValueError("Timeframe cannot be empty.")

        if self.observation_count <= 0:
            raise ValueError(
                "Observation count must be positive."
            )

        if self.end_time < self.start_time:
            raise ValueError(
                "End time cannot precede start time."
            )
    