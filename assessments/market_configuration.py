from dataclasses import dataclass


@dataclass(frozen=True)
class MarketConfiguration:

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
            key=lambda expansion: expansion.end_index
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
            latest.end_index
        )

        for event in events:

            # Ignore invalid events
            if not event.valid:
                continue

            # Ignore BOS
            if event.event_type != "CHOCH":
                continue

            # Opposite CHOCH invalidates Expansion
            if (
                latest.direction == "BULLISH"
                and event.direction == "BEARISH"
            ):
                return None

            if (
                latest.direction == "BEARISH"
                and event.direction == "BULLISH"
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
            and event.event_type == event_type
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
        pass  # later

    def latest_segment(self):
        pass # later

    # -----------------------------------
    # Region Queries
    # -----------------------------------

    def latest_order_block(self):
        pass# later

    def active_order_blocks(self):
        pass# later

    def latest_fvg(self):
        pass# later

    def open_fvgs(self):
        pass# later