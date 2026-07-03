import pandas as pd

from .market_observation import MarketObservation
from .observation_history import ObservationHistory
from .observation_metadata import ObservationMetadata


class ObservationHistoryBuilder:

    @staticmethod
    def from_dataframe(
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
        source: str | None = None,
    ) -> ObservationHistory:

        observations = tuple(
            MarketObservation(
                timestamp=row["Datetime"],
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]) if "Volume" in row else None,
            )
            for _, row in df.iterrows()
        )

        metadata = ObservationMetadata(
            symbol=symbol,
            timeframe=timeframe,
            start_time=observations[0].timestamp,
            end_time=observations[-1].timestamp,
            observation_count=len(observations),
            source=source,
        )

        return ObservationHistory(
            observations=observations,
            metadata=metadata,
        )