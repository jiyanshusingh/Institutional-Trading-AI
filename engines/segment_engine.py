import pandas as pd


class SegmentEngine:

    def __init__(self, df, bos_events):

        self.df = df.copy()
        self.bos_events = bos_events

        self.segments = []

    # --------------------------------------------------
    # Create Segment
    # --------------------------------------------------

    def create_segment(self, bos_event):

        segment = {

            "segment_id": len(self.segments) + 1,

            "source_bos": bos_event["event_id"],

            "direction": bos_event["direction"],

            "start_index": None,

            "end_index": bos_event["candle_index"],

            "state": "ACTIVE",

            "valid": True

        }

        return segment

    # --------------------------------------------------
    # Validate Segment
    # --------------------------------------------------

    def validate_segment(self, segment):

        if segment is None:
            return False

        # Rule 1
        # Valid Direction

        if segment["direction"] not in ["BULLISH", "BEARISH"]:
            return False

        # Rule 2
        # Source BOS must exist

        if segment["source_bos"] is None:
            return False

        # Rule 3
        # End Index must exist

        if segment["end_index"] is None:
            return False

        # Rule 4
        # State must be ACTIVE

        if segment["state"] != "ACTIVE":
            return False

        return True

    # --------------------------------------------------
    # Store Segment
    # --------------------------------------------------

    def store_segment(self, segment):

        if segment is None:
            return

        self.segments.append(segment)

    # --------------------------------------------------
    # Generate Segments
    # --------------------------------------------------

    def generate_segments(self):

        for bos_event in self.bos_events:

            segment = self.create_segment(bos_event)

            if self.validate_segment(segment):

                self.store_segment(segment)

        return self.segments