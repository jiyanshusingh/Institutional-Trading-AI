class StructureEventEngine:

    def __init__(self, df):

        self.df = df.copy()
        self.events = []
    # -------------------------------------------------
    # Event Factory
    # -------------------------------------------------
    def create_event(
        self,
        event_id,
        event_type,
        direction,
        timestamp,
        candle_index,
        broken_swing_index,
        base_swing_index,
        price,
        valid,
        metadata
    ):

        return {

            "event_id": event_id,

            "event_type": event_type,

            "direction": direction,

            "timestamp": timestamp,

            "candle_index": candle_index,

            "broken_swing_index": broken_swing_index,

            "base_swing_index": base_swing_index,

            "price": price,

            "valid": valid,

            "metadata": metadata

        }
    # -------------------------------------------------
    # Dispatcher
    # -------------------------------------------------
    def generate_events(self):

        self.generate_bos_events()
        self.generate_choch_events()

        return self.events

    # -------------------------------------------------
    # BOS Events
    # -------------------------------------------------
    def generate_bos_events(self):

        event_id = len(self.events) + 1

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

            # ----------------------------------------
            # Base Swing
            # ----------------------------------------

            if direction == "BULLISH":
                base_swing_index = row["Protected_Low_Index"]
            else:
                base_swing_index = row["Protected_High_Index"]

            event = self.create_event(

                event_id=event_id,

                event_type="BOS",

                direction=direction,

                timestamp=self.df.index[i],

                candle_index=i,

                broken_swing_index=row["BOS_Broken_Swing_Index"],

                base_swing_index=base_swing_index,

                price=row["BOS_Level"],

                valid=True,

                metadata={

                    "displacement": row["BOS_Displacement"]

                }

            )

            self.events.append(event)

            event_id += 1
            
    # -------------------------------------------------
    # CHOCH Events
    # -------------------------------------------------
    def generate_choch_events(self):

        event_id = len(self.events) + 1

        for i in range(len(self.df)):

            row = self.df.iloc[i]
            if row["CHOCH_Valid"]:

                print("Index :", i)
                print("Type  :", row["CHOCH_Type"])
                print("Level :", row["CHOCH_Level"])
                print("Broken:", row["CHOCH_Broken_Swing_Index"])
                print("Base  :", row["CHOCH_Base_Swing_Index"])
            # Only VALID CHOCH create events
            if not row["CHOCH_Valid"]:
                continue

            direction = (
                "BULLISH"
                if row["Bullish_CHOCH"]
                else "BEARISH"
            )

            if direction == "BULLISH":
                base_swing_index = row["CHOCH_Base_Swing_Index"]

            else:
                base_swing_index = row["CHOCH_Base_Swing_Index"]

            event = self.create_event(

                event_id=event_id,

                event_type="CHOCH",

                direction=direction,

                timestamp=self.df.index[i],

                candle_index=i,

                broken_swing_index=row["CHOCH_Broken_Swing_Index"],

                base_swing_index=base_swing_index,

                price=row["CHOCH_Level"],

                valid=True,

                metadata={

                    "displacement": row["CHOCH_Displacement"]

                }

            )

            self.events.append(event)
            print(event)
            print("Total Events:", len(self.events))


            event_id += 1