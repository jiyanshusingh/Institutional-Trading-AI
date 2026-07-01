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
result = validator.validate_swings()

print("\n========== Swing Validation ==========")
print("Passed :", result["passed"])

if result["errors"]:
    print("\nErrors:")
    for error in result["errors"]:
        print("-", error)
else:
    print("No errors found.")
