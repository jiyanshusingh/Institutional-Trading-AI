class StructureEventEngine:

    def __init__(self, df):

        self.df = df.copy()

        self.events = []

    def generate_events(self):

        event_id = 1

        for i in range(len(self.df)):

            row = self.df.iloc[i]

            # Only VALID BOS create events
            if not row["BOS_Valid"]:
                continue

            direction = (
                "BULLISH"
                if row["Bullish_BOS"]
                else "BEARISH"
            )

            event = {

                "event_id": event_id,

                "event_type": "BOS",

                "direction": direction,

                "timestamp": self.df.index[i],

                "candle_index": i,

                "price": row["BOS_Level"],

                "valid": True,

                "metadata": {

                    "displacement": row["BOS_Displacement"]

                }

            }

            self.events.append(event)

            event_id += 1

        return self.events