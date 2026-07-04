import pytest
from datetime import datetime

from domain.ontology.swing import Swing
from domain.ontology.swing_type import SwingType


def test_create_swing_high():

    swing = Swing(
        index=10,
        confirmation_index=13,
        timestamp=datetime.now(),
        price=105.5,
        swing_type=SwingType.HIGH,
    )

    assert swing.index == 10
    assert swing.confirmation_index == 13
    assert swing.price == 105.5
    assert swing.swing_type == SwingType.HIGH
    assert swing.is_high
    assert not swing.is_low


def test_create_swing_low():

    swing = Swing(
        index=20,
        confirmation_index=24,
        timestamp=datetime.now(),
        price=95.2,
        swing_type=SwingType.LOW,
    )

    assert swing.swing_type == SwingType.LOW
    assert swing.is_low
    assert not swing.is_high


def test_negative_index_not_allowed():

    with pytest.raises(ValueError):

        Swing(
            index=-1,
            confirmation_index=5,
            timestamp=datetime.now(),
            price=100,
            swing_type=SwingType.HIGH,
        )


def test_negative_price_not_allowed():

    with pytest.raises(ValueError):

        Swing(
            index=1,
            confirmation_index=5,
            timestamp=datetime.now(),
            price=-100,
            swing_type=SwingType.HIGH,
        )


def test_confirmation_cannot_precede_index():

    with pytest.raises(ValueError):

        Swing(
            index=10,
            confirmation_index=8,
            timestamp=datetime.now(),
            price=100,
            swing_type=SwingType.HIGH,
        )


def test_swing_is_immutable():

    swing = Swing(
        index=1,
        confirmation_index=4,
        timestamp=datetime.now(),
        price=100,
        swing_type=SwingType.HIGH,
    )

    with pytest.raises(Exception):
        swing.price = 200


def test_is_high_property():

    swing = Swing(
        index=5,
        confirmation_index=8,
        timestamp=datetime.now(),
        price=120,
        swing_type=SwingType.HIGH,
    )

    assert swing.is_high is True
    assert swing.is_low is False


def test_is_low_property():

    swing = Swing(
        index=5,
        confirmation_index=8,
        timestamp=datetime.now(),
        price=90,
        swing_type=SwingType.LOW,
    )

    assert swing.is_low is True
    assert swing.is_high is False