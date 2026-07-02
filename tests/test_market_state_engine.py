from datetime import datetime

from engines.market_state_engine import MarketStateEngine
from models.structure_event import StructureEvent


# -------------------------------------------------
# Scenario 1
# UNKNOWN -> Bullish BOS -> UPTREND
# -------------------------------------------------

events = [

    StructureEvent(

        event_id=1,

        event_type="BOS",

        direction="BULLISH",

        timestamp=datetime.now(),

        candle_index=10,

        broken_swing_index=5,

        base_swing_index=4,

        price=100.0,

        valid=True,

        metadata={
            "displacement": 2.5
        }

    )

]

engine = MarketStateEngine(events)

history = engine.process()

print("\n==============================")
print("MARKET STATE HISTORY")
print("==============================\n")

for record in history:

    print(record)

print("\nFinal State :", engine.market_state)