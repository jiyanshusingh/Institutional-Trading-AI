from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.structure_event_engine import StructureEventEngine
from engines.segment_engine import SegmentEngine


# -----------------------------------
# Load Data
# -----------------------------------

engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

# -----------------------------------
# Market Structure
# -----------------------------------

ms = MarketStructure(df)

df = ms.detect_swings()
df = ms.classify_structure()
df = ms.detect_trend_candidate()
df = ms.detect_protected_swings()
df = ms.detect_bos()
df = ms.detect_choch()

# -----------------------------------
# Structure Events
# -----------------------------------

event_engine = StructureEventEngine(df)

events = event_engine.generate_events()

# -----------------------------------
# Segment Engine
# -----------------------------------

segment_engine = SegmentEngine(events)

segments = segment_engine.build()

# -----------------------------------
# Print Events
# -----------------------------------

print("\n==============================")
print("STRUCTURE EVENTS")
print("==============================")

for event in events:

    print(
        f"{event.event_id:2d} | "
        f"{event.event_type:5s} | "
        f"{event.direction:8s} | "
        f"Candle={event.candle_index}"
    )

# -----------------------------------
# Print Segments
# -----------------------------------

print("\n==============================")
print("SEGMENTS")
print("==============================")

for segment in segments:

    print(segment)

# -----------------------------------
# Active Segment
# -----------------------------------

print("\n==============================")
print("ACTIVE SEGMENT")
print("==============================")

print(segment_engine.active_segment)