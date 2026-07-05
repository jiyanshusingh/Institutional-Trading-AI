from datetime import datetime

from assessments.market_configuration import MarketConfiguration
from models.expansion import Expansion
from models.structure_event import StructureEvent


def create_bos(
    event_id=1,
    direction="BEARISH",
    candle_index=100
):

    return StructureEvent(
        event_id=event_id,
        event_type="BOS",
        direction=direction,
        timestamp=datetime.now(),
        candle_index=candle_index,
        broken_swing_index=10,
        base_swing_index=5,
        price=100.0,
        valid=True,
        metadata={}
    )


def create_choch(
    event_id=2,
    direction="BULLISH",
    candle_index=120
):

    return StructureEvent(
        event_id=event_id,
        event_type="CHOCH",
        direction=direction,
        timestamp=datetime.now(),
        candle_index=candle_index,
        broken_swing_index=20,
        base_swing_index=15,
        price=120.0,
        valid=True,
        metadata={}
    )


def create_expansion(
    direction="BEARISH"
):

    return Expansion(
        id=1,
        segment_id=1,
        direction=direction,
        base_swing_index=5,
        broken_swing_index=10,
        bos_event_id=1,
        start_index=5,
        end_index=100
    )


# ----------------------------------------------------
# Test 1
# Latest BOS
# ----------------------------------------------------

def test_latest_bos():

    bos = create_bos()

    configuration = MarketConfiguration(
        structure_events=(bos,)
    )

    assert configuration.latest_bos() == bos


# ----------------------------------------------------
# Test 2
# Latest CHOCH
# ----------------------------------------------------

def test_latest_choch():

    bos = create_bos()

    choch = create_choch()

    configuration = MarketConfiguration(
        structure_events=(bos, choch)
    )

    assert configuration.latest_choch() == choch


# ----------------------------------------------------
# Test 3
# Governing Expansion Exists
# ----------------------------------------------------

def test_governing_expansion_exists():

    expansion = create_expansion()

    bos = create_bos()

    configuration = MarketConfiguration(
        structure_events=(bos,),
        expansions=(expansion,)
    )

    assert configuration.governing_expansion() == expansion


# ----------------------------------------------------
# Test 4
# Governing Expansion Invalidated
# ----------------------------------------------------

def test_governing_expansion_invalidated():

    expansion = create_expansion(direction="BEARISH")

    bos = create_bos(direction="BEARISH")

    choch = create_choch(
        direction="BULLISH",
        candle_index=120
    )

    configuration = MarketConfiguration(
        structure_events=(bos, choch),
        expansions=(expansion,)
    )

    assert configuration.governing_expansion() is None


# ----------------------------------------------------
# Test 5
# No Expansion
# ----------------------------------------------------

def test_no_expansion():

    configuration = MarketConfiguration()

    assert configuration.governing_expansion() is None