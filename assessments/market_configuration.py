from dataclasses import dataclass
import pandas as pd
from domain.ontology.structure_event import StructureDirection

@dataclass(frozen=True)
class MarketConfiguration:
    df: pd.DataFrame
    structure_events: tuple = ()

    segments: tuple = ()

    expansions: tuple = ()

    origin_regions: tuple = ()

    order_blocks: tuple = ()

    fair_value_gaps: tuple = ()

    liquidity_regions: tuple = ()

    relationships: tuple = ()

    # -----------------------------------
    # Expansion Queries
    # -----------------------------------
    def latest_expansion(self):
        if not self.expansions:
            return None

        return max(
            self.expansions,
            key=lambda expansion: expansion.confirmation_event_index
        )

    def latest_structure_event(self):
        if not self.structure_events:
            return None

        return max(
            self.structure_events,
            key=lambda event: event.candle_index
        )

    def structure_events_after(self, candle_index):

        return tuple(

            event

            for event in self.structure_events

            if event.candle_index > candle_index

        )
    def governing_expansion(self):

        latest = self.latest_expansion()

        if latest is None:
            return None

        events = self.structure_events_after(
            latest.confirmation_event_index
        )

        for event in events:

            if not event.valid:
                continue

            if event.event_type.value != "CHOCH":
                continue

            if (
                latest.direction == StructureDirection.BULLISH
                and event.direction == StructureDirection.BEARISH
            ):
                return None

            if (
                latest.direction == StructureDirection.BEARISH
                and event.direction == StructureDirection.BULLISH
            ):
                return None

        return latest
    # -----------------------------------
    # Structure Event Queries
    # -----------------------------------
    def _latest_event(self, event_type):

        events = tuple(
            event
            for event in self.structure_events
            if event.valid
            and event.event_type.value == event_type
        )

        if not events:
            return None

        return max(events, key=lambda e: e.candle_index)

    def latest_bos(self):
        return self._latest_event("BOS")


    def latest_choch(self):
        return self._latest_event("CHOCH")
    # -----------------------------------
    # Segment Queries
    # -----------------------------------

    def active_segment(self):
        return None

    def latest_segment(self):
        return None

    # -----------------------------------
    # Region Queries
    # -----------------------------------

    def latest_order_block(self):
        return None

    def active_order_blocks(self):
        return None

    def latest_fair_value_gap(self):
        if not self.fair_value_gaps:
            return None
        return self.fair_value_gaps[-1]

    def open_fvgs(self):
        return None