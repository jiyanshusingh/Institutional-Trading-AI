"""
==========================================================
Research Sample
==========================================================

Purpose
-------
Defines the canonical research observation used throughout
the Research Engine.

A ResearchSample represents ONE market event together with

- Context
- Deterministic Features
- Future Outcome

It is independent of:

- pandas
- Machine Learning
- Statistics
- Backtesting

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ==========================================================
# Research Sample
# ==========================================================

@dataclass(slots=True)
class ResearchSample:
    """
    Canonical research observation.

    One sample corresponds to one structural market event.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    sample_id: str

    # ------------------------------------------------------
    # Market Context
    # ------------------------------------------------------

    symbol: str

    timeframe: str

    timestamp: datetime

    # ------------------------------------------------------
    # Event
    # ------------------------------------------------------

    event: str

    # ------------------------------------------------------
    # Outcome
    # ------------------------------------------------------

    outcome: str | None = None

    # ------------------------------------------------------
    # Feature Values
    # ------------------------------------------------------

    features: dict[str, float] = field(
        default_factory=dict
    )

    # ------------------------------------------------------
    # Additional Metadata
    # ------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ======================================================
    # Feature API
    # ======================================================

    def add_feature(
        self,
        name: str,
        value: float,
    ) -> None:
        """
        Add or update a feature.
        """

        self.features[name] = value

    def get_feature(
        self,
        name: str,
    ) -> float:
        """
        Return feature value.
        """

        return self.features[name]

    def has_feature(
        self,
        name: str,
    ) -> bool:
        """
        Check whether feature exists.
        """

        return name in self.features

    # ======================================================
    # Metadata API
    # ======================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store additional metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    # ======================================================
    # Outcome API
    # ======================================================

    def set_outcome(
        self,
        outcome: str,
    ) -> None:
        """
        Assign research outcome.
        """

        self.outcome = outcome

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert sample to flat dictionary.
        Suitable for DataFrame construction.
        """

        data = {

            "sample_id": self.sample_id,

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "timestamp": self.timestamp,

            "event": self.event,

            "outcome": self.outcome,

        }

        data.update(self.features)

        return data


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    sample = ResearchSample(

        sample_id="SMP-000001",

        symbol="RELIANCE",

        timeframe="15m",

        timestamp=datetime.now(),

        event="bos",

    )

    sample.add_feature(
        "atr_14",
        1.82,
    )

    sample.add_feature(
        "relative_volume_20",
        2.34,
    )

    sample.set_outcome(
        "bos_continuation",
    )

    print(sample)

    print()

    print(sample.to_dict())