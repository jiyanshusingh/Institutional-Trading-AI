from engines.data_engine import DataEngine
from engines.market_structure import MarketStructure
from policies.liquidity.equal_high_policy import EqualHighLiquidityPolicy

# Load data
engine = DataEngine()

df = engine.get_data(
    "MARICO.NS",
    period="1y",
    interval="1d"
)

# Detect swings
ms = MarketStructure(df)

df = ms.detect_swings()

# Keep only confirmed swing highs
swing_highs = df[df["Swing_High"]]
print(swing_highs[["High"]])
print(f"\nTotal Swing Highs: {len(swing_highs)}")

# Detect liquidity
policy = EqualHighLiquidityPolicy()

regions = policy.identify(
    swing_highs,
    tolerance=0.5     # <-- Replace placeholder with an actual value
)

print("\n==============================")
print("LIQUIDITY REGIONS")
print("==============================")

for i, region in enumerate(regions, start=1):

    print(f"""
Region #{i}

Upper Price : {region.upper_price}
Lower Price : {region.lower_price}

------------------------------
""")