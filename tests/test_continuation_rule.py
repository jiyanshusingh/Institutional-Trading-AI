from datetime import datetime

from assessments.market_observations import MarketObservations
from assessments.structural.rules.continuation_rule import ContinuationRule
from models.expansion import Expansion
from models.structure_event import StructureEvent

rule = ContinuationRule()

# -----------------------------
# TEST 1
# Bullish Continuation
# -----------------------------

expansion1 = Expansion(
    id=1,
    segment_id=1,
    direction="Bullish",
    base_swing_index=10,
    broken_swing_index=20,
    bos_event_id=1,
    start_index=10,
    end_index=20
)

obs1 = MarketObservations(
    structure_events=(),
    expansions=(expansion1,)
)

# -----------------------------
# TEST 2
# Bearish Continuation
# -----------------------------

expansion2 = Expansion(
    id=2,
    segment_id=2,
    direction="Bearish",
    base_swing_index=30,
    broken_swing_index=40,
    bos_event_id=2,
    start_index=30,
    end_index=40
)

obs2 = MarketObservations(
    structure_events=(),
    expansions=(expansion2,)
)

# -----------------------------
# TEST 3
# Bullish Expansion + Bearish CHOCH
# -----------------------------

choch = StructureEvent(
    event_id=1,
    event_type="CHOCH",
    direction="Bearish",
    timestamp=datetime.now(),
    candle_index=25,
    broken_swing_index=21,
    base_swing_index=18,
    price=100.0,
    valid=True,
    metadata={}
)

obs3 = MarketObservations(
    structure_events=(choch,),
    expansions=(expansion1,)
)

# -----------------------------
# TEST 4
# No Expansion
# -----------------------------

obs4 = MarketObservations()

# -----------------------------
# Run Tests
# -----------------------------

from datetime import datetime

from assessments.market_observations import MarketObservations
from assessments.structural.rules.continuation_rule import ContinuationRule
from models.expansion import Expansion
from models.structure_event import StructureEvent

rule = ContinuationRule()

# -----------------------------
# TEST 1
# Bullish Continuation
# -----------------------------

expansion1 = Expansion(
    id=1,
    segment_id=1,
    direction="Bullish",
    base_swing_index=10,
    broken_swing_index=20,
    bos_event_id=1,
    start_index=10,
    end_index=20
)

obs1 = MarketObservations(
    structure_events=(),
    expansions=(expansion1,)
)

# -----------------------------
# TEST 2
# Bearish Continuation
# -----------------------------

expansion2 = Expansion(
    id=2,
    segment_id=2,
    direction="Bearish",
    base_swing_index=30,
    broken_swing_index=40,
    bos_event_id=2,
    start_index=30,
    end_index=40
)

obs2 = MarketObservations(
    structure_events=(),
    expansions=(expansion2,)
)

# -----------------------------
# TEST 3
# Bullish Expansion + Bearish CHOCH
# -----------------------------

choch = StructureEvent(
    event_id=1,
    event_type="CHOCH",
    direction="Bearish",
    timestamp=datetime.now(),
    candle_index=25,
    broken_swing_index=21,
    base_swing_index=18,
    price=100.0,
    valid=True,
    metadata={}
)

obs3 = MarketObservations(
    structure_events=(choch,),
    expansions=(expansion1,)
)

# -----------------------------
# TEST 4
# No Expansion
# -----------------------------

obs4 = MarketObservations()

# -----------------------------
# Run Tests
# -----------------------------

print("==============================")
print("TEST 1")
print("==============================")
print(rule.evaluate(obs1))

print("==============================")
print("TEST 2")
print("==============================")
print(rule.evaluate(obs2))

print("==============================")
print("TEST 3")
print("==============================")
print(rule.evaluate(obs3))

print("==============================")
print("TEST 4")
print("==============================")
print(rule.evaluate(obs4))