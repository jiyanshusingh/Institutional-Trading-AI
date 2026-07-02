from dataclasses import dataclass


@dataclass(frozen=True)
class MarketConfiguration:

    structure_events: tuple = ()

    expansions: tuple = ()

    origin_regions: tuple = ()

    order_blocks: tuple = ()

    fair_value_gaps: tuple = ()

    liquidity_regions: tuple = ()

    relationships: tuple = ()
    
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