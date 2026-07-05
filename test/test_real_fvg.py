from engines.data_engine import DataEngine
from policies.fair_value_gap.ict_three_candle_policy import (
    ICTThreeCandleFVGPolicy
)

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
# Detect FVGs
# -----------------------------------

policy = ICTThreeCandleFVGPolicy()

fvgs = policy.detect(df)

# -----------------------------------
# Print
# -----------------------------------

print("\n==============================")
print("FAIR VALUE GAPS")
print("==============================")

for i, fvg in enumerate(fvgs, start=1):

    print(f"""
FVG #{i}

Upper Price : {fvg.upper_price}
Lower Price : {fvg.lower_price}

------------------------------
""")