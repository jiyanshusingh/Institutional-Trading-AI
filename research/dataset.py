"""
==========================================================
Research Dataset
==========================================================

Purpose
-------
Represents a collection of ResearchSample objects.

A ResearchDataset is the canonical dataset used by the
Research Engine.

Responsibilities
----------------
- Store research samples
- Filter samples
- Summarize dataset
- Export to DataFrame
- Export to dictionaries

Independent of:

- Statistics
- Machine Learning
- Trading Logic
- Backtesting

==========================================================
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

import pandas as pd

from .sample import ResearchSample


# ==========================================================
# Research Dataset
# ==========================================================

class ResearchDataset:
    """
    Collection of ResearchSample objects.
    """

    def __init__(
        self,
        samples: Iterable[ResearchSample] | None = None,
    ):

        self._samples: list[ResearchSample] = list(
            samples or []
        )

    # ======================================================
    # Collection API
    # ======================================================

    def add_sample(
        self,
        sample: ResearchSample,
    ) -> None:
        """
        Add a research sample.
        """

        self._samples.append(sample)

    def extend(
        self,
        samples: Iterable[ResearchSample],
    ) -> None:
        """
        Add multiple samples.
        """

        self._samples.extend(samples)

    def clear(
        self,
    ) -> None:
        """
        Remove every sample.
        """

        self._samples.clear()

    # ======================================================
    # Access
    # ======================================================

    def samples(
        self,
    ) -> list[ResearchSample]:
        """
        Return all samples.
        """

        return list(self._samples)

    def first(
        self,
    ) -> ResearchSample | None:

        if not self._samples:
            return None

        return self._samples[0]

    def last(
        self,
    ) -> ResearchSample | None:

        if not self._samples:
            return None

        return self._samples[-1]

    # ======================================================
    # Filters
    # ======================================================

    def filter_by_symbol(
        self,
        symbol: str,
    ) -> "ResearchDataset":

        return ResearchDataset(

            sample

            for sample in self._samples

            if sample.symbol == symbol

        )

    def filter_by_event(
        self,
        event: str,
    ) -> "ResearchDataset":

        return ResearchDataset(

            sample

            for sample in self._samples

            if sample.event == event

        )

    def filter_by_timeframe(
        self,
        timeframe: str,
    ) -> "ResearchDataset":

        return ResearchDataset(

            sample

            for sample in self._samples

            if sample.timeframe == timeframe

        )

    def filter_by_outcome(
        self,
        outcome: str,
    ) -> "ResearchDataset":

        return ResearchDataset(

            sample

            for sample in self._samples

            if sample.outcome == outcome

        )

    # ======================================================
    # Statistics
    # ======================================================

    def unique_symbols(
        self,
    ) -> list[str]:

        return sorted(

            {

                sample.symbol

                for sample in self._samples

            }

        )

    def unique_events(
        self,
    ) -> list[str]:

        return sorted(

            {

                sample.event

                for sample in self._samples

            }

        )

    def unique_timeframes(
        self,
    ) -> list[str]:

        return sorted(

            {

                sample.timeframe

                for sample in self._samples

            }

        )

    def outcome_counts(
        self,
    ) -> dict[str, int]:

        return dict(

            Counter(

                sample.outcome

                for sample in self._samples

            )

        )

    # ======================================================
    # Export
    # ======================================================

    def to_dicts(
        self,
    ) -> list[dict]:

        return [

            sample.to_dict()

            for sample in self._samples

        ]

    def to_dataframe(
        self,
    ) -> pd.DataFrame:

        return pd.DataFrame(

            self.to_dicts()

        )

    # ======================================================
    # Summary
    # ======================================================

    def summary(
        self,
    ) -> dict:

        return {

            "samples": len(self),

            "symbols": len(
                self.unique_symbols()
            ),

            "events": len(
                self.unique_events()
            ),

            "timeframes": len(
                self.unique_timeframes()
            ),

            "outcomes": self.outcome_counts(),

        }

    # ======================================================
    # Magic Methods
    # ======================================================

    def __len__(
        self,
    ) -> int:

        return len(self._samples)

    def __iter__(
        self,
    ):

        return iter(self._samples)

    def __getitem__(
        self,
        index: int,
    ) -> ResearchSample:

        return self._samples[index]

    def __bool__(
        self,
    ) -> bool:

        return bool(self._samples)

    def __repr__(
        self,
    ) -> str:

        return (

            f"ResearchDataset("

            f"samples={len(self)})"

        )


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    from datetime import datetime

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

    sample.set_outcome(
        "bos_continuation",
    )

    dataset = ResearchDataset()

    dataset.add_sample(sample)

    print(dataset)

    print()

    print(dataset.summary())

    print()

    print(dataset.to_dataframe())