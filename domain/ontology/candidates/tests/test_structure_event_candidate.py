import pytest
from datetime import datetime

from domain.ontology.candidates.structure_event_candidate import (
    StructureEventCandidate,
)

from domain.ontology.structure_event import (
    StructureEventType,
    StructureDirection,
)


def test_create_bullish_bos_candidate():

    candidate = StructureEventCandidate(
        event_type=StructureEventType.BOS,
        direction=StructureDirection.BULLISH,
        timestamp=datetime.now(),
        candle_index=20,
        broken_swing_index=15,
        base_swing_index=10,
        price=105.5,
        displacement=2.4,
    )

    assert candidate.event_type == StructureEventType.BOS
    assert candidate.direction == StructureDirection.BULLISH
    assert candidate.price == 105.5


def test_create_bearish_choch_candidate():

    candidate = StructureEventCandidate(
        event_type=StructureEventType.CHOCH,
        direction=StructureDirection.BEARISH,
        timestamp=datetime.now(),
        candle_index=30,
        broken_swing_index=25,
        base_swing_index=18,
        price=98.2,
        displacement=3.1,
    )

    assert candidate.event_type == StructureEventType.CHOCH
    assert candidate.direction == StructureDirection.BEARISH


def test_negative_candle_index_not_allowed():

    with pytest.raises(ValueError):

        StructureEventCandidate(
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

        StructureEventCandidate(
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

        StructureEventCandidate(
            event_type=StructureEventType.BOS,
            direction=StructureDirection.BULLISH,
            timestamp=datetime.now(),
            candle_index=1,
            broken_swing_index=0,
            base_swing_index=0,
            price=100,
            displacement=-1,
        )


def test_candidate_is_immutable():

    candidate = StructureEventCandidate(
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
        candidate.price = 200