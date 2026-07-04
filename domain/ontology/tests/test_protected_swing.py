import pytest
from datetime import datetime

from domain.ontology.protected_swing import (
    ProtectedSwing,
    ProtectedSwingType,
)


def test_create_protected_high():

    swing = ProtectedSwing(
        swing_index=10,
        timestamp=datetime.now(),
        price=105.5,
        protected_type=ProtectedSwingType.HIGH,
        protecting_event_index=12,
    )

    assert swing.is_high
    assert not swing.is_low


def test_create_protected_low():

    swing = ProtectedSwing(
        swing_index=20,
        timestamp=datetime.now(),
        price=95.2,
        protected_type=ProtectedSwingType.LOW,
        protecting_event_index=25,
    )

    assert swing.is_low
    assert not swing.is_high


def test_negative_index_not_allowed():

    with pytest.raises(ValueError):

        ProtectedSwing(
            swing_index=-1,
            timestamp=datetime.now(),
            price=100,
            protected_type=ProtectedSwingType.HIGH,
            protecting_event_index=5,
        )


def test_negative_price_not_allowed():

    with pytest.raises(ValueError):

        ProtectedSwing(
            swing_index=1,
            timestamp=datetime.now(),
            price=-100,
            protected_type=ProtectedSwingType.HIGH,
            protecting_event_index=5,
        )


def test_negative_protecting_event_not_allowed():

    with pytest.raises(ValueError):

        ProtectedSwing(
            swing_index=1,
            timestamp=datetime.now(),
            price=100,
            protected_type=ProtectedSwingType.HIGH,
            protecting_event_index=-1,
        )


def test_is_high_property():

    swing = ProtectedSwing(
        swing_index=1,
        timestamp=datetime.now(),
        price=100,
        protected_type=ProtectedSwingType.HIGH,
        protecting_event_index=2,
    )

    assert swing.is_high is True


def test_is_low_property():

    swing = ProtectedSwing(
        swing_index=1,
        timestamp=datetime.now(),
        price=100,
        protected_type=ProtectedSwingType.LOW,
        protecting_event_index=2,
    )

    assert swing.is_low is True


def test_protected_swing_is_immutable():

    swing = ProtectedSwing(
        swing_index=1,
        timestamp=datetime.now(),
        price=100,
        protected_type=ProtectedSwingType.HIGH,
        protecting_event_index=2,
    )

    with pytest.raises(Exception):
        swing.price = 200