"""
==========================================================
Market Event Builder
==========================================================

Purpose
-------
Converts detected market structure events into
standardized MarketEvent objects.

Responsibilities
----------------
- Build MarketEvent objects
- Assign unique IDs
- Preserve event metadata
- Export as list

Does NOT

- Detect BOS
- Detect CHOCH
- Detect Swings
- Perform research
- Perform statistics

==========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from research.market_event import MarketEvent


class MarketEventBuilder:
    """
    Converts detected structural events into MarketEvent
    objects.
    """

    # ======================================================
    # Public API
    # ======================================================

    @staticmethod
    def build(
        events: list[dict[str, Any]],
    ) -> list[MarketEvent]:
        """
        Build MarketEvent objects.

        Parameters
        ----------
        events
            List of detected structure events.

        Returns
        -------
        list[MarketEvent]
        """

        market_events: list[MarketEvent] = []

        for event in events:

            market_events.append(

                MarketEventBuilder.from_dict(
                    event
                )

            )

        return market_events

    # ======================================================
    # Builders
    # ======================================================

    @staticmethod
    def from_dict(
        data: dict[str, Any],
    ) -> MarketEvent:
        """
        Convert one dictionary into a MarketEvent.
        """

        return MarketEvent(

            # ----------------------------------------------
            # Identity
            # ----------------------------------------------

            event_id=data.get(
                "event_id",
                str(uuid4()),
            ),

            event_type=data["event_type"],

            # ----------------------------------------------
            # Context
            # ----------------------------------------------

            symbol=data["symbol"],

            timeframe=data["timeframe"],

            timestamp=data["timestamp"],

            direction=data.get("direction"),

            price=data.get("price"),

            candle_index=data.get(
                "candle_index"
            ),

            # ----------------------------------------------
            # Structure
            # ----------------------------------------------

            base_swing=data.get(
                "base_swing"
            ),

            trigger_swing=data.get(
                "trigger_swing"
            ),

            protected_swing=data.get(
                "protected_swing"
            ),

            segment=data.get(
                "segment"
            ),

            expansion=data.get(
                "expansion"
            ),

            metadata=data.get(
                "metadata",
                {},
            ),

        )

    # ======================================================
    # Export
    # ======================================================

    @staticmethod
    def to_dicts(
        events: list[MarketEvent],
    ) -> list[dict]:
        """
        Convert MarketEvents to dictionaries.
        """

        return [

            event.to_dict()

            for event in events

        ]


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    detected_events = [

        {

            "event_type": "bos",

            "symbol": "RELIANCE",

            "timeframe": "15m",

            "timestamp": datetime.now(),

            "direction": "Bullish",

            "price": 2518.75,

            "candle_index": 1234,

            "base_swing": "SH-001",

            "trigger_swing": "SH-002",

            "protected_swing": "SL-001",

            "segment": "SEG-001",

            "expansion": "EXP-001",

            "metadata": {

                "strength": 0.87,

            },

        }

    ]

    events = MarketEventBuilder.build(
        detected_events
    )

    print(events[0])

    print()

    print(events[0].to_dict())