from models.segment import Segment
from models.structure_event import StructureEvent


class SegmentEngine:

    def __init__(self, events: list[StructureEvent]):

        self.events = events

        self.segments = []

        self.active_segment = None

        self.next_segment_id = 1

    def build(self):

        for event in self.events:

            self.process_event(event)

        return self.segments

    def process_event(self, event: StructureEvent):

        # ------------------------------------
        # BOS
        # ------------------------------------

        if event.event_type == "BOS":

            self.handle_bos(event)

        # ------------------------------------
        # CHOCH
        # ------------------------------------

        elif event.event_type == "CHOCH":

            self.handle_choch(event)
    # ------------------------------------
    # BOS
    # ------------------------------------

    def handle_bos(self, event: StructureEvent):

        # ------------------------------------
        # No Active Segment
        # ------------------------------------
        if self.active_segment is None:

            segment = Segment(

                id=self.next_segment_id,

                direction=event.direction,

                start_event_id=event.event_id,

                end_event_id=None,

                start_index=event.candle_index,

                end_index=None

            )

            self.segments.append(segment)

            self.active_segment = segment

            self.next_segment_id += 1

        # ------------------------------------
        # Continuation BOS
        # ------------------------------------
        elif self.active_segment.direction == event.direction:

            return

        # ------------------------------------
        # Opposite BOS
        # Should Never Happen
        # ------------------------------------
        else:

            raise RuntimeError(
                "Received opposite BOS while a Segment is still active."
            )
            # ------------------------------------
            # CHOCH
            # ------------------------------------

    def handle_choch(self, event: StructureEvent):

        # ------------------------------------
        # No Active Segment
        # ------------------------------------
        if self.active_segment is None:

            return

        # ------------------------------------
        # Same Direction
        # Ignore
        # ------------------------------------
        if event.direction == self.active_segment.direction:

            return

        # ------------------------------------
        # Close Active Segment
        # ------------------------------------
        closed_segment = Segment(

            id=self.active_segment.id,

            direction=self.active_segment.direction,

            start_event_id=self.active_segment.start_event_id,

            end_event_id=event.event_id,

            start_index=self.active_segment.start_index,

            end_index=event.candle_index

        )

        segment_index = len(self.segments) - 1

        self.segments[segment_index] = closed_segment

        self.active_segment = None