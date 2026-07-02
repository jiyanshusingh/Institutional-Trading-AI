from models.structure_event import StructureEvent
UNKNOWN = "UNKNOWN"
UPTREND = "UPTREND"
DOWNTREND = "DOWNTREND"
TRANSITION = "TRANSITION"


class MarketStateEngine:

    def __init__(self, events: list[StructureEvent]):

        self.events = events

        self.market_state = "UNKNOWN"

        self.history = []

    def process(self):

        for event in self.events:

            self.process_event(event)

        return self.history

    def process_event(self, event: StructureEvent):

        if self.market_state == UNKNOWN:

            self.handle_unknown(event)

        elif self.market_state == UPTREND:

            self.handle_uptrend(event)

        elif self.market_state == DOWNTREND:

            self.handle_downtrend(event)

        elif self.market_state == TRANSITION:

            self.handle_transition(event)
            
    def handle_unknown(self, event: StructureEvent):

        # --------------------------------------
        # Bullish BOS starts an Uptrend
        # --------------------------------------

        if (
            event.event_type == "BOS"
            and event.direction == "BULLISH"
        ):

            previous_state = self.market_state

            self.market_state = UPTREND

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bullish BOS"

            })

        # --------------------------------------
        # Bearish BOS starts a Downtrend
        # --------------------------------------

        elif (
            event.event_type == "BOS"
            and event.direction == "BEARISH"
        ):

            previous_state = self.market_state

            self.market_state = DOWNTREND

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bearish BOS"

            })
            
    def handle_uptrend(self, event: StructureEvent):

        # --------------------------------------
        # Bullish BOS
        # Stay in UPTREND
        # --------------------------------------

        if (
            event.event_type == "BOS"
            and event.direction == "BULLISH"
        ):

            previous_state = self.market_state

            self.market_state = UPTREND

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bullish BOS"

            })

        # --------------------------------------
        # Bearish CHOCH
        # Transition begins
        # --------------------------------------

        elif (
            event.event_type == "CHOCH"
            and event.direction == "BEARISH"
        ):

            previous_state = self.market_state

            self.market_state = TRANSITION

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bearish CHOCH"

            })
            
    def handle_downtrend(self, event: StructureEvent):

        # --------------------------------------
        # Bearish BOS
        # Stay in DOWNTREND
        # --------------------------------------

        if (
            event.event_type == "BOS"
            and event.direction == "BEARISH"
        ):

            previous_state = self.market_state

            self.market_state = DOWNTREND

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bearish BOS"

            })

        # --------------------------------------
        # Bullish CHOCH
        # Transition begins
        # --------------------------------------

        elif (
            event.event_type == "CHOCH"
            and event.direction == "BULLISH"
        ):

            previous_state = self.market_state

            self.market_state = TRANSITION

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bullish CHOCH"

            })


    # -------------------------------------------------
    # TRANSITION
    # -------------------------------------------------

    def handle_transition(self, event: StructureEvent):

        # --------------------------------------
        # Bullish BOS
        # Confirm Bullish Trend
        # --------------------------------------

        if (
            event.event_type == "BOS"
            and event.direction == "BULLISH"
        ):

            previous_state = self.market_state

            self.market_state = UPTREND

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bullish BOS"

            })

        # --------------------------------------
        # Bearish BOS
        # Confirm Bearish Trend
        # --------------------------------------

        elif (
            event.event_type == "BOS"
            and event.direction == "BEARISH"
        ):

            previous_state = self.market_state

            self.market_state = DOWNTREND

            self.history.append({

                "event_id": event.event_id,

                "event_type": event.event_type,

                "timestamp": event.timestamp,

                "previous_state": previous_state,

                "new_state": self.market_state,

                "reason": "Bearish BOS"

            })