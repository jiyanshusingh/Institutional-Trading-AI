"""
==========================================================
Dataset Builder
==========================================================

Purpose
-------
Construct a ResearchDataset from MarketEvents.

Responsibilities
----------------
- Orchestrate the research pipeline
- Build ResearchSample objects
- Label ResearchSample objects
- Return ResearchDataset

Does NOT
---------
- Compute Features
- Detect Events
- Perform Statistics
- Run Research

==========================================================
"""

from __future__ import annotations

import pandas as pd

from research.dataset import ResearchDataset
from research.market_event import MarketEvent
from research.outcome_definitions import OutcomeDefinition

from research.builders.sample_builder import SampleBuilder
from research.builders.outcome_builder import OutcomeBuilder


class DatasetBuilder:
    """
    Orchestrates construction of a ResearchDataset.
    """

    def __init__(
        self,
        outcome_definition: OutcomeDefinition,
    ):

        self.outcome_definition = outcome_definition

    # ======================================================
    # Build Dataset
    # ======================================================

    def build(
        self,
        events: list[MarketEvent],
        feature_store: dict[str, dict[str, float]],
        future_data: dict[str, pd.DataFrame],
    ) -> ResearchDataset:
        """
        Build a complete ResearchDataset.

        Parameters
        ----------
        events
            Market events.

        feature_store
            Maps event_id -> feature dictionary.

        future_data
            Maps event_id -> future OHLCV DataFrame.

        Returns
        -------
        ResearchDataset
        """

        dataset = ResearchDataset()

        for event in events:

            sample = self._build_sample(

                event=event,

                features=feature_store.get(
                    event.event_id,
                    {},
                ),

                future_df=future_data.get(
                    event.event_id,
                    pd.DataFrame(),
                ),
            )

            dataset.add_sample(sample)

        return dataset

    # ======================================================
    # Internal
    # ======================================================

    def _build_sample(
        self,
        event: MarketEvent,
        features: dict[str, float],
        future_df: pd.DataFrame,
    ):
        """
        Build and label one sample.
        """

        sample = SampleBuilder.build(

            event=event,

            features=features,

        )

        sample = OutcomeBuilder.build(

            sample=sample,

            future_df=future_df,

            definition=self.outcome_definition,

        )

        return sample

    # ======================================================
    # Convenience
    # ======================================================

    def build_one(
        self,
        event: MarketEvent,
        features: dict[str, float],
        future_df: pd.DataFrame,
    ):
        """
        Build a single ResearchSample.
        """

        return self._build_sample(

            event=event,

            features=features,

            future_df=future_df,

        )