from engines.data_engine import DataEngine
from engines.market_structure import MarketStructureEngine

engine = DataEngine()

df = engine.get_data("MARICO.NS")

df = MarketStructureEngine(df).analyze()

print(
    df[
        [
            "HH",
            "HL",
            "LH",
            "LL",
            "Trend",
            "Bullish_BOS",
            "Bearish_BOS",
            "Bullish_CHOCH",
            "Bearish_CHOCH"
        ]
    ].tail(40)
)