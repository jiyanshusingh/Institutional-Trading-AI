from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.validation_engine import ValidationEngine
import pandas as pd

engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

ms = MarketStructure(df)

df = ms.detect_swings()
df = ms.classify_structure()
df = ms.detect_trend_candidate()
df = ms.detect_protected_swings()
df = ms.detect_bos()
df = ms.detect_choch()
df = ms.detect_market_state()

validator = ValidationEngine(df)

validator = ValidationEngine(df)

result = validator.validate_choch()

print(
    df[
        (df["Bullish_CHOCH"]) |
        (df["Bearish_CHOCH"])
    ][[
        "Close",
        "Structure",
        "Trend_Candidate",
        "Protected_High",
        "Protected_Low",
        "Bullish_CHOCH",
        "Bearish_CHOCH",
        "Market_State"
    ]]
)
from engines.order_block_engine import OrderBlockEngine
from engines.structure_event_engine import StructureEventEngine

event_engine = StructureEventEngine(df)
bos_events = event_engine.generate_events()

ob_engine = OrderBlockEngine(df, bos_events)

df = ob_engine.initialize()

print("\n========== ORDER BLOCK PROJECTION ==========\n")

ob_engine.detect_order_blocks()

df = ob_engine.project_order_blocks()

print(

    df[
        [
            "Bullish_OB",
            "Bearish_OB",
            "OB_High",
            "OB_Low",
            "OB_Type",
            "OB_Source_BOS",
            "OB_Valid"
        ]
    ][
        (df["Bullish_OB"]) |
        (df["Bearish_OB"])
    ]

)