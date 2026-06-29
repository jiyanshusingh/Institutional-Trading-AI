from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure

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

print(
    df[
        [
            "Close",
            "High",
            "Low",
            "Swing_High",
            "Swing_Low",
            "Structure",
            "Bullish_BOS",
            "Bearish_BOS",
            "Bullish_CHOCH",
            "Bearish_CHOCH"
        ]
    ].tail(60)
)