from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
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
#df = ms.detect_bos()
#df = ms.detect_choch()
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
print(
    df[
        [
            "Close",
            "Structure",
            "Trend_Candidate",
            "Protected_Low",
            "Protected_High"
        ]
    ].to_csv("protected_swings_validation.csv")
)