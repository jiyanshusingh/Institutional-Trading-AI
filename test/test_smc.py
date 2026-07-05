from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from engines.smc_engine import SMCEngine

engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

# Market Structure
ms = MarketStructure(df)
ms.detect_swings()
df = ms.classify_structure()

# SMC
smc = SMCEngine(df)
df = smc.detect_bos()

print(
    df[
        [
            "Close",
            "Swing_High",
            "Swing_Low",
            "Bullish_BOS",
            "Bearish_BOS",
        ]
    ].tail(40)
)