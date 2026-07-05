import pandas as pd

from policies.fair_value_gap.ict_three_candle_policy import (
    ICTThreeCandleFVGPolicy
)

policy = ICTThreeCandleFVGPolicy()

# -----------------------------
# Bullish Test
# -----------------------------

bullish_df = pd.DataFrame({

    "High": [100, 103, 110],

    "Low": [95, 98, 105]

})

bullish_fvgs = policy.detect(bullish_df)

print("\n==============================")
print("BULLISH FVG")
print("==============================")

for fvg in bullish_fvgs:
    print(fvg)

# -----------------------------
# Bearish Test
# -----------------------------

bearish_df = pd.DataFrame({

    "High": [110, 108, 100],

    "Low": [105, 102, 95]

})

bearish_fvgs = policy.detect(bearish_df)

print("\n==============================")
print("BEARISH FVG")
print("==============================")

for fvg in bearish_fvgs:
    print(fvg)