"""
==========================================================
Event Types
==========================================================

Purpose
-------
Defines every canonical market structure event used by the
Research Engine.

This module DOES NOT detect events.

It only defines:

- Event identifiers
- Categories
- Descriptions
- Event metadata

Detection is performed by the Market Structure Engine.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ==========================================================
# Event Category
# ==========================================================

class EventCategory(Enum):

    MARKET_STRUCTURE = "Market Structure"

    LIQUIDITY = "Liquidity"

    TREND = "Trend"

    SEGMENT = "Segment"

    EXPANSION = "Expansion"

    PULLBACK = "Pullback"

    SWING = "Swing"

    EXECUTION = "Execution"


# ==========================================================
# Event Metadata
# ==========================================================

@dataclass(frozen=True)
class Event:

    id: str

    name: str

    category: EventCategory

    description: str

    deterministic: bool


# ==========================================================
# Event Registry
# ==========================================================

EVENTS = {

    # ------------------------------------------------------
    # Swing Events
    # ------------------------------------------------------

    "swing_high": Event(

        id="EVT-001",

        name="Swing High",

        category=EventCategory.SWING,

        description="Confirmed swing high.",

        deterministic=True,

    ),

    "swing_low": Event(

        id="EVT-002",

        name="Swing Low",

        category=EventCategory.SWING,

        description="Confirmed swing low.",

        deterministic=True,

    ),

    "protected_high": Event(

        id="EVT-003",

        name="Protected High",

        category=EventCategory.SWING,

        description="Protected swing high.",

        deterministic=True,

    ),

    "protected_low": Event(

        id="EVT-004",

        name="Protected Low",

        category=EventCategory.SWING,

        description="Protected swing low.",

        deterministic=True,

    ),

    # ------------------------------------------------------
    # Market Structure
    # ------------------------------------------------------

    "bos": Event(

        id="EVT-005",

        name="Break of Structure",

        category=EventCategory.MARKET_STRUCTURE,

        description="Confirmed Break of Structure.",

        deterministic=True,

    ),

    "choch": Event(

        id="EVT-006",

        name="Change of Character",

        category=EventCategory.MARKET_STRUCTURE,

        description="Confirmed Change of Character.",

        deterministic=True,

    ),

    # ------------------------------------------------------
    # Liquidity
    # ------------------------------------------------------

    "liquidity_sweep": Event(

        id="EVT-007",

        name="Liquidity Sweep",

        category=EventCategory.LIQUIDITY,

        description="Liquidity sweep confirmed.",

        deterministic=True,

    ),

    "equal_highs": Event(

        id="EVT-008",

        name="Equal Highs",

        category=EventCategory.LIQUIDITY,

        description="Equal highs identified.",

        deterministic=True,

    ),

    "equal_lows": Event(

        id="EVT-009",

        name="Equal Lows",

        category=EventCategory.LIQUIDITY,

        description="Equal lows identified.",

        deterministic=True,

    ),

    # ------------------------------------------------------
    # Segment
    # ------------------------------------------------------

    "segment_start": Event(

        id="EVT-010",

        name="Segment Start",

        category=EventCategory.SEGMENT,

        description="Beginning of a structural segment.",

        deterministic=True,

    ),

    "segment_end": Event(

        id="EVT-011",

        name="Segment End",

        category=EventCategory.SEGMENT,

        description="End of a structural segment.",

        deterministic=True,

    ),

    # ------------------------------------------------------
    # Expansion
    # ------------------------------------------------------

    "expansion_start": Event(

        id="EVT-012",

        name="Expansion Start",

        category=EventCategory.EXPANSION,

        description="Beginning of an expansion.",

        deterministic=True,

    ),

    "expansion_end": Event(

        id="EVT-013",

        name="Expansion End",

        category=EventCategory.EXPANSION,

        description="End of an expansion.",

        deterministic=True,

    ),

    # ------------------------------------------------------
    # Pullback
    # ------------------------------------------------------

    "pullback_start": Event(

        id="EVT-014",

        name="Pullback Start",

        category=EventCategory.PULLBACK,

        description="Beginning of a pullback.",

        deterministic=True,

    ),

    "pullback_end": Event(

        id="EVT-015",

        name="Pullback End",

        category=EventCategory.PULLBACK,

        description="End of a pullback.",

        deterministic=True,

    ),

}


# ==========================================================
# Helper Functions
# ==========================================================

def get_event(
    event_name: str,
) -> Event:
    """
    Return metadata for an event.
    """

    return EVENTS[event_name]


def list_events():
    """
    Return all registered event names.
    """

    return sorted(EVENTS.keys())


def events_by_category(
    category: EventCategory,
):
    """
    Return all events belonging to a category.
    """

    return {

        name: event

        for name, event in EVENTS.items()

        if event.category == category

    }


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("EVENT TYPES")
    print("=" * 60)

    print()

    print(f"Total Events : {len(EVENTS)}")

    print()

    for event in list_events():

        print(event)