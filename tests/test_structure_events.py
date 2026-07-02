from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.structure_event_engine import StructureEventEngine


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
print("\n==============================")
print("CHOCH EVENTS")
print("==============================")

debug_columns = [
    "Bullish_CHOCH",
    "Bearish_CHOCH",
    "CHOCH_Type",
    "CHOCH_Level",
    "CHOCH_Broken_Swing_Index",
    "CHOCH_Valid"
]

print(
    df.loc[
        df["Bullish_CHOCH"] | df["Bearish_CHOCH"],
        debug_columns
    ]
)

df = ms.detect_market_state()
print("\nAFTER MARKET STATE")
print(
    df.loc[
        df["Bullish_CHOCH"] | df["Bearish_CHOCH"],
        debug_columns
    ]
)
print("\nCHOCH_Base_Swing_Index exists:",
      "CHOCH_Base_Swing_Index" in df.columns)
# -----------------------------------
# Generate Events
# -----------------------------------

event_engine = StructureEventEngine(df)

events = event_engine.generate_events()

# -----------------------------------
# Print Events
# -----------------------------------

print("\n==============================")
print("STRUCTURE EVENTS")
print("==============================\n")

for event in events:

    print(f"Event ID            : {event['event_id']}")
    print(f"Event Type          : {event['event_type']}")
    print(f"Direction           : {event['direction']}")
    print(f"Candle Index        : {event['candle_index']}")
    print(f"Broken Swing Index  : {event['broken_swing_index']}")
    print(f"Base Swing Index    : {event['base_swing_index']}")
    print(f"Price               : {event['price']}")
    print(f"Valid               : {event['valid']}")
    print("------------------------------")