from models.expansion import Expansion
from models.structure_event import StructureEvent
from models.segment import Segment


class ExpansionEngine:

    def __init__(
        self,
        segments: list[Segment],
        events: list[StructureEvent]
    ):

        self.segments = segments
        self.events = events

        self.expansions = []

        self.next_expansion_id = 1
        # ------------------------------------
    # Expansion Factory
    # ------------------------------------

    def create_expansion(

            self,

            segment_id,

            event

        ):

            return Expansion(

                id=self.next_expansion_id,

                segment_id=segment_id,

                direction=event.direction,

                base_swing_index=event.base_swing_index,

                broken_swing_index=event.broken_swing_index,

                bos_event_id=event.event_id,

                start_index=event.base_swing_index,

                end_index=event.candle_index

            )
        # ------------------------------------
    # Segment Lookup
    # ------------------------------------

    def build_segment_lookup(self):

        lookup = {}

        for segment in self.segments:

            start = segment.start_event_id

            if segment.end_event_id is None:

                end = float("inf")

            else:

                end = segment.end_event_id

            for event in self.events:

                if start <= event.event_id <= end:

                    lookup[event.event_id] = segment.id

        return lookup

    def build(self):

            segment_lookup = self.build_segment_lookup()

            for event in self.events:

                if event.event_type != "BOS":

                    continue

                segment_id = segment_lookup.get(event.event_id)

                if segment_id is None:

                    continue

                expansion = self.create_expansion(

                    segment_id,

                    event

                )

                self.expansions.append(expansion)

                self.next_expansion_id += 1

            return self.expansions