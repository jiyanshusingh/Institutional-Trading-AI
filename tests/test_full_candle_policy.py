import pandas as pd

df = pd.DataFrame({

    "High": [752.50],

    "Low": [741.25]

})
from models.origin_region import OriginRegion

origin = OriginRegion(

    start_index=0,

    end_index=0

)
from policies.order_block.full_candle_policy import FullCandleOrderBlockPolicy

policy = FullCandleOrderBlockPolicy()

order_block = policy.create(
    origin,
    df
)
print("\n==============================")
print("ORDER BLOCK")
print("==============================\n")

print(order_block)
assert order_block.high == 752.50
assert order_block.low == 741.25
assert order_block.origin_region == origin

print("\n✅ Unit Test Passed")