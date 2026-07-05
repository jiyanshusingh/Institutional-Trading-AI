from datetime import datetime

from models.structure_event import StructureEvent
from models.segment import Segment
from engines.expansion_engine import ExpansionEngine


# --------------------------------------
# Segment
# --------------------------------------

segments = [

    Segment(

        id=1,

        direction="BULLISH",

        start_event_id=1,

        end_event_id=None,

        start_index=10,

        end_index=None

    )

]

# --------------------------------------
# Events
# --------------------------------------

events = [

    StructureEvent(

        event_id=1,

        event_type="BOS",

        direction="BULLISH",

        timestamp=datetime.now(),

        candle_index=10,

        broken_swing_index=5,

        base_swing_index=4,

        price=100,

        valid=True,

        metadata={}

    )

]

# --------------------------------------
# Expansion Engine
# --------------------------------------

engine = ExpansionEngine(

    segments,

    events

)

expansions = engine.build()

# --------------------------------------
# Print
# --------------------------------------

print("\n==============================")
print("EXPANSIONS")
print("==============================\n")

for expansion in expansions:

    print(expansion)