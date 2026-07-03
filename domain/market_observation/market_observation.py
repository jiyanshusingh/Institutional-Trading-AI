from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MarketObservation:
    """
    A single immutable market observation.
    """

    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: float | None = None
    def __post_init__(self):

        if self.high < max(self.open, self.close, self.low):
            raise ValueError(
                "High price must be greater than or equal to open, close, and low."
            )

        if self.low > min(self.open, self.close, self.high):
            raise ValueError(
                "Low price must be less than or equal to open, close, and high."
            )

        if self.volume is not None and self.volume < 0:
            raise ValueError(
                "Volume cannot be negative."
            )