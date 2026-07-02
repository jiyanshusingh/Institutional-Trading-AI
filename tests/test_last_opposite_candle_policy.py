import pandas as pd

from models.expansion import Expansion
from policies.origin_region.last_opposite_candle_policy import (
    LastOppositeCandlePolicy
)


# ---------------------------------------
# Synthetic OHLC
# ---------------------------------------

df = pd.DataFrame({

    "Open":  [100, 100, 99],

    "Close": [100, 99, 105]

})

# ---------------------------------------
# Expansion
# ---------------------------------------

expansion = Expansion(

    id=1,

    segment_id=1,

    direction="BULLISH",

    base_swing_index=0,

    broken_swing_index=0,

    bos_event_id=1,

    start_index=0,

    end_index=2

)

# ---------------------------------------
# Policy
# ---------------------------------------

policy = LastOppositeCandlePolicy()

origin = policy.identify(

    expansion,

    df

)

# ---------------------------------------
# Result
# ---------------------------------------

print("\n==============================")
print("ORIGIN REGION")
print("==============================")

print(origin)