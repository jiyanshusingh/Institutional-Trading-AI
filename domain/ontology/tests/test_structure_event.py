import pytest
from datetime import datetime

from domain.ontology.structure_event import (
    StructureEvent,
    StructureEventType,
    StructureDirection,
)


def test_create_bullish_bos():

    event = StructureEvent(
        event_id=1,
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=20,
        broken_swing_index=15,
        base_swing_index=10,
        price=105.5,
        displacement=2.4,
    )

    assert event.event_type == StructureEventType.BOS
    assert event.direction == StructureDirection.BULLISH
    assert event.price == 105.5


def test_create_bearish_choch():

    event = StructureEvent(
        event_id=2,
        event_type=StructureEventType.CHOCH,
        direction=StructureDirection.BEARISH,
        timestamp=datetime.now(),
        candle_index=30,
        broken_swing_index=25,
        base_swing_index=18,
        price=98.2,
        displacement=3.1,
    )

    assert event.event_type == StructureEventType.CHOCH
    assert event.direction == StructureDirection.BEARISH


def test_event_id_must_be_positive():

    with pytest.raises(ValueError):

        StructureEvent(
            event_id=0,
            event_type=StructureEventType.BOS,
            direction=StructureDirection.BULLISH,
            timestamp=datetime.now(),
            candle_index=1,
            broken_swing_index=0,
            base_swing_index=0,
            price=100,
            displacement=1,
        )


def test_negative_candle_index_not_allowed():

    with pytest.raises(ValueError):

        StructureEvent(
            event_id=1,
            event_type=StructureEventType.BOS,
            direction=StructureDirection.BULLISH,
            timestamp=datetime.now(),
            candle_index=-1,
            broken_swing_index=0,
            base_swing_index=0,
            price=100,
            displacement=1,
        )


def test_negative_price_not_allowed():

    with pytest.raises(ValueError):

        StructureEvent(
            event_id=1,
            event_type=StructureEventType.BOS,
            direction=StructureDirection.BULLISH,
            timestamp=datetime.now(),
            candle_index=1,
            broken_swing_index=0,
            base_swing_index=0,
            price=-10,
            displacement=1,
        )


def test_negative_displacement_not_allowed():

    with pytest.raises(ValueError):

        StructureEvent(
            event_id=1,
            event_type=StructureEventType.BOS,
            direction=StructureDirection.BULLISH,
            timestamp=datetime.now(),
            candle_index=1,
            broken_swing_index=0,
            base_swing_index=0,
            price=100,
            displacement=-1,
        )


def test_structure_event_is_immutable():

    event = StructureEvent(
        event_id=1,
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=20,
        broken_swing_index=15,
        base_swing_index=10,
        price=105,
        displacement=2.5,
    )

    with pytest.raises(Exception):
        event.price = 200