"""
==========================================================
Market Event
==========================================================

Purpose
-------
Defines one detected market event.

A MarketEvent represents one historical occurrence of a
structural market event.

Examples

- One BOS
- One CHOCH
- One Liquidity Sweep
- One Expansion
- One Pullback

It is independent of

- pandas
- Statistics
- Machine Learning
- Trading Logic

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ==========================================================
# Market Event
# ==========================================================

@dataclass(slots=True)
class MarketEvent:
    """
    One detected market event.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    event_id: str

    event_type: str

    # ------------------------------------------------------
    # Market Context
    # ------------------------------------------------------

    symbol: str

    timeframe: str

    timestamp: datetime

    # ------------------------------------------------------
    # Event Context
    # ------------------------------------------------------

    direction: str | None = None

    price: float | None = None

    candle_index: int | None = None

    # ------------------------------------------------------
    # Structure References
    # ------------------------------------------------------

    base_swing: str | None = None

    trigger_swing: str | None = None

    protected_swing: str | None = None

    segment: str | None = None

    expansion: str | None = None

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ======================================================
    # Metadata API
    # ======================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    # ======================================================
    # Export
    # ======================================================

    def to_dict(self) -> dict[str, Any]:

        data = {

            "event_id": self.event_id,

            "event_type": self.event_type,

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "timestamp": self.timestamp,

            "direction": self.direction,

            "price": self.price,

            "candle_index": self.candle_index,

            "base_swing": self.base_swing,

            "trigger_swing": self.trigger_swing,

            "protected_swing": self.protected_swing,

            "segment": self.segment,

            "expansion": self.expansion,

        }

        data.update(self.metadata)

        return data

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:

        return (

            f"MarketEvent("

            f"id={self.event_id}, "

            f"type={self.event_type}, "

            f"symbol={self.symbol}, "

            f"timeframe={self.timeframe}"

            f")"

        )


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    event = MarketEvent(

        event_id="EVT-000001",

        event_type="bos",

        symbol="RELIANCE",

        timeframe="15m",

        timestamp=datetime.now(),

        direction="Bullish",

        price=2521.45,

        candle_index=1845,

        base_swing="SH-0012",

        trigger_swing="SH-0013",

        protected_swing="SL-0010",

        segment="SEG-0021",

        expansion="EXP-0008",

    )

    event.add_metadata(

        "volume_spike",

        True,

    )

    print(event)

    print()

    print(event.to_dict())