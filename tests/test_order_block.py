from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.order_block_engine import OrderBlockEngine
from engines.structure_event_engine import StructureEventEngine

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

event_engine = StructureEventEngine(df)
bos_events = event_engine.generate_events()

ob = OrderBlockEngine(df, bos_events)

df = ob.initialize()

order_blocks = ob.detect_order_blocks()

df = ob.project_order_blocks()

print(
    df[
        [
            "Open",
            "Close",
            "Bullish_BOS",
            "Bearish_BOS",
            "Bullish_OB",
            "Bearish_OB"
        ]
    ].tail(80)
)