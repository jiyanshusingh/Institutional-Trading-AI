from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.structure_event_engine import StructureEventEngine
from engines.segment_engine import SegmentEngine

# ---------------------------------------------
# Load Data
# ---------------------------------------------

engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

# ---------------------------------------------
# Market Structure Pipeline
# ---------------------------------------------

ms = MarketStructure(df)

df = ms.detect_swings()
df = ms.classify_structure()
df = ms.detect_trend_candidate()
df = ms.detect_protected_swings()
df = ms.detect_bos()
df = ms.detect_choch()
df = ms.detect_market_state()

# ---------------------------------------------
# Structure Events
# ---------------------------------------------

event_engine = StructureEventEngine(df)

bos_events = event_engine.generate_events()

# ---------------------------------------------
# Segment Engine
# ---------------------------------------------

segment_engine = SegmentEngine(df, bos_events)

segments = segment_engine.generate_segments()

# ---------------------------------------------
# Results
# ---------------------------------------------

print("\n==============================")
print("SEGMENT ENGINE TEST")
print("==============================\n")

print(f"BOS Events : {len(bos_events)}")
print(f"Segments   : {len(segments)}")

print("\n------------------------------\n")

for segment in segments:

    print(f"Segment ID : {segment['segment_id']}")
    print(f"Source BOS : {segment['source_bos']}")
    print(f"Direction  : {segment['direction']}")
    print(f"Start      : {segment['start_index']}")
    print(f"End        : {segment['end_index']}")
    print(f"State      : {segment['state']}")
    print(f"Valid      : {segment['valid']}")
    print("\n------------------------------\n")