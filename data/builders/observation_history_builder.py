from __future__ import annotations

import pandas as pd

from domain.market_observation.market_observation import (
    MarketObservation,
)
from domain.market_observation.observation_history import (
    ObservationHistory,
)
from domain.market_observation.observation_metadata import (
    ObservationMetadata,
)

class ObservationHistoryBuilder:
    """
    Builds an ObservationHistory from a normalized
    OHLCV pandas DataFrame.

    Expected columns

    timestamp
    open
    high
    low
    close
    volume
    """

    REQUIRED_COLUMNS = (
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    )

    def build(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
        source: str = "CSV",
    ) -> ObservationHistory:

        self._validate_dataframe(df)

        observations = tuple(
            self._build_observation(row)
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

    # ==========================================================
    # Internal Helpers
    # ==========================================================

    def _build_observation(
        self,
        row,
    ) -> MarketObservation:

        volume = (
            None
            if pd.isna(row["volume"])
            else float(row["volume"])
        )

        return MarketObservation(
            timestamp=pd.Timestamp(
                row["timestamp"]
            ).to_pydatetime(),

            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),

            volume=volume,
        )

    def _validate_dataframe(
        self,
        df: pd.DataFrame,
    ) -> None:

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(missing)
            )

        if df.empty:
            raise ValueError(
                "DataFrame cannot be empty."
            )

        if not df["timestamp"].is_monotonic_increasing:
            df.sort_values(
                "timestamp",
                inplace=True,
            )
            df.reset_index(
                drop=True,
                inplace=True,
            )