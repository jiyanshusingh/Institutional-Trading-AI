import pandas as pd

from policies.liquidity.equal_high_policy import EqualHighLiquidityPolicy

policy = EqualHighLiquidityPolicy()

# -----------------------------
# Test Data
# -----------------------------

swings = pd.DataFrame({

    "High": [

        710.00,
        710.05,
        710.08,
        725.00

    ]

})

regions = policy.identify(
    swings,
    tolerance=1.0
)

print("\n==============================")
print("LIQUIDITY REGIONS")
print("==============================")

for region in regions:

    print(region)