from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.expansion import (
    Expansion,
    ExpansionDirection,
)


def test_create_bullish_expansion():

    expansion = Expansion(
        base_swing_index=5,
        confirmation_event_index=8,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        start_price=100,
        end_price=110,
        direction=ExpansionDirection.BULLISH,
    )

    assert expansion.is_bullish
    assert not expansion.is_bearish


def test_create_bearish_expansion():

    expansion = Expansion(
        base_swing_index=10,
        confirmation_event_index=15,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        start_price=110,
        end_price=95,
        direction=ExpansionDirection.BEARISH,
    )

    assert expansion.is_bearish
    assert not expansion.is_bullish


def test_negative_base_swing_not_allowed():

    with pytest.raises(ValueError):

        Expansion(
            base_swing_index=-1,
            confirmation_event_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            start_price=100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_negative_confirmation_event_not_allowed():

    with pytest.raises(ValueError):

        Expansion(
            base_swing_index=1,
            confirmation_event_index=-1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            start_price=100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_positive_prices_required():

    with pytest.raises(ValueError):

        Expansion(
            base_swing_index=1,
            confirmation_event_index=2,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            start_price=-100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_end_time_after_start_time():

    now = datetime.now()

    with pytest.raises(ValueError):

        Expansion(
            base_swing_index=1,
            confirmation_event_index=2,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            start_price=100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_price_range():

    expansion = Expansion(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        start_price=100,
        end_price=112,
        direction=ExpansionDirection.BULLISH,
    )

    assert expansion.price_range == 12


def test_expansion_is_immutable():

    expansion = Expansion(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        start_price=100,
        end_price=105,
        direction=ExpansionDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        expansion.start_price = 120