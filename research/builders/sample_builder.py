"""
==========================================================
Sample Builder
==========================================================

Purpose
-------
Constructs ResearchSample objects from MarketEvent objects.

Responsibilities
----------------
- Convert MarketEvent → ResearchSample
- Attach deterministic feature values
- Preserve market context

Does NOT

- Compute features
- Detect events
- Assign outcomes
- Perform research

==========================================================
"""

from __future__ import annotations

from typing import Any

from research.market_event import MarketEvent
from research.sample import ResearchSample


# ==========================================================
# Sample Builder
# ==========================================================

class SampleBuilder:
    """
    Builds ResearchSample objects.
    """

    # ======================================================
    # Public API
    # ======================================================

    @staticmethod
    def build(
        event: MarketEvent,
        features: dict[str, float] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ResearchSample:
        """
        Build a ResearchSample from a MarketEvent.
        """

        sample = ResearchSample(

            sample_id=SampleBuilder._sample_id(
                event.event_id
            ),

            symbol=event.symbol,

            timeframe=event.timeframe,

            timestamp=event.timestamp,

            event=event.event_type,

        )

        # ----------------------------------------------
        # Copy Features
        # ----------------------------------------------

        if features:

            for name, value in features.items():

                sample.add_feature(
                    name=name,
                    value=value,
                )

        # ----------------------------------------------
        # Copy Event Metadata
        # ----------------------------------------------

        sample.add_metadata(
            "event_id",
            event.event_id,
        )

        sample.add_metadata(
            "direction",
            event.direction,
        )

        sample.add_metadata(
            "price",
            event.price,
        )

        sample.add_metadata(
            "candle_index",
            event.candle_index,
        )

        sample.add_metadata(
            "base_swing",
            event.base_swing,
        )

        sample.add_metadata(
            "trigger_swing",
            event.trigger_swing,
        )

        sample.add_metadata(
            "protected_swing",
            event.protected_swing,
        )

        sample.add_metadata(
            "segment",
            event.segment,
        )

        sample.add_metadata(
            "expansion",
            event.expansion,
        )

        # ----------------------------------------------
        # Additional Metadata
        # ----------------------------------------------

        if metadata:

            for key, value in metadata.items():

                sample.add_metadata(
                    key,
                    value,
                )

        return sample

    # ======================================================
    # Helper
    # ======================================================

    @staticmethod
    def _sample_id(
        event_id: str,
    ) -> str:
        """
        Generate a deterministic sample ID.
        """

        return f"SMP-{event_id}"