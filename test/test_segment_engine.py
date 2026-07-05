from datetime import datetime

from models.structure_event import StructureEvent
from engines.segment_engine import SegmentEngine


# --------------------------------------
# Scenario 1
# UNKNOWN
# ↓
# Bullish BOS
# ↓
# First Bullish Segment
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
    ),

    StructureEvent(
        event_id=2,
        event_type="CHOCH",
        direction="BEARISH",
        timestamp=datetime.now(),
        candle_index=20,
        broken_swing_index=8,
        base_swing_index=5,
        price=95,
        valid=True,
        metadata={}
    ),

    StructureEvent(
        event_id=3,
        event_type="BOS",
        direction="BEARISH",
        timestamp=datetime.now(),
        candle_index=30,
        broken_swing_index=15,
        base_swing_index=12,
        price=90,
        valid=True,
        metadata={}
    )

]
engine = SegmentEngine(events)

segments = engine.build()

print("\n==============================")
print("SEGMENTS")
print("==============================\n")

for segment in segments:

    print(segment)

print("\nActive Segment")
print(engine.active_segment)