from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.order_block_engine import OrderBlockEngine

engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

ms = MarketStructure(df)

df = ms.detect_swings()
df = ms.classify_structure()
df = ms.detect_bos()
df = ms.detect_choch()

ob = OrderBlockEngine(df)

df = ob.detect_order_blocks()

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