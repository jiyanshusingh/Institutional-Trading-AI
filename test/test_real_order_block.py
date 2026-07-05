from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.structure_event_engine import StructureEventEngine
from engines.segment_engine import SegmentEngine
from engines.expansion_engine import ExpansionEngine

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
expansion_engine = ExpansionEngine(
    segments,
    events
)
expansions = expansion_engine.build()
from policies.origin_region.last_opposite_candle_policy import (
    LastOppositeCandlePolicy
)
from policies.order_block.full_candle_policy import (
    FullCandleOrderBlockPolicy
)

origin_policy = LastOppositeCandlePolicy()

order_block_policy = FullCandleOrderBlockPolicy()

print("==============================")
print("ORDER BLOCK VALIDATION")
print("==============================")

for expansion in expansions:

    origin = origin_policy.identify(
        expansion,
        df
    )
    if origin is None:

        print("Origin Region : None")
        print("-" * 50)

        continue

    order_block = order_block_policy.create(
        origin,
        df
    )
    expansion_df = df.iloc[
        expansion.start_index:
        expansion.end_index + 1
    ][["Open", "Close"]].copy()

    expansion_df["Type"] = expansion_df.apply(

        lambda row:

            "Bullish"

            if row["Close"] > row["Open"]

            else "Bearish"

            if row["Close"] < row["Open"]

            else "Doji",

        axis=1

    )

    print(expansion_df)
    print(f"""
Expansion ID        : {expansion.id}
Segment ID          : {expansion.segment_id}
Direction           : {expansion.direction}
Base Swing Index    : {expansion.base_swing_index}
Broken Swing Index  : {expansion.broken_swing_index}
Start Index         : {expansion.start_index}
End Index           : {expansion.end_index}
BOS Event ID        : {expansion.bos_event_id}
""")

    print(
        f"Origin Region     : "
        f"{origin.start_index} -> {origin.end_index}"
    )

    print(f"Order Block High  : {order_block.high}")

    print(f"Order Block Low   : {order_block.low}")

    print("-" * 50)
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
print("\n==============================")
print("EXPANSIONS")
print("==============================\n")