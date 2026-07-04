import pytest
from datetime import datetime

from domain.ontology.candidates.protected_swing_candidate import (
    ProtectedSwingCandidate,
)

from domain.ontology.protected_swing import (
    ProtectedSwingType,
)


def test_create_high_candidate():

    candidate = ProtectedSwingCandidate(
        swing_index=10,
        timestamp=datetime.now(),
        price=105,
        protected_type=ProtectedSwingType.HIGH,
        protecting_event_index=15,
    )

    assert candidate.protected_type == ProtectedSwingType.HIGH


def test_create_low_candidate():

    candidate = ProtectedSwingCandidate(
        swing_index=20,
        timestamp=datetime.now(),
        price=95,
        protected_type=ProtectedSwingType.LOW,
        protecting_event_index=25,
    )

    assert candidate.protected_type == ProtectedSwingType.LOW


def test_negative_swing_index():

    with pytest.raises(ValueError):

        ProtectedSwingCandidate(
            swing_index=-1,
            timestamp=datetime.now(),
            price=100,
            protected_type=ProtectedSwingType.HIGH,
            protecting_event_index=1,
        )


def test_negative_event_index():

    with pytest.raises(ValueError):

        ProtectedSwingCandidate(
            swing_index=1,
            timestamp=datetime.now(),
            price=100,
            protected_type=ProtectedSwingType.HIGH,
            protecting_event_index=-1,
        )


def test_negative_price():

    with pytest.raises(ValueError):

        ProtectedSwingCandidate(
            swing_index=1,
            timestamp=datetime.now(),
            price=-100,
            protected_type=ProtectedSwingType.HIGH,
            protecting_event_index=1,
        )


def test_candidate_is_immutable():

    candidate = ProtectedSwingCandidate(
        swing_index=1,
        timestamp=datetime.now(),
        price=100,
        protected_type=ProtectedSwingType.HIGH,
        protecting_event_index=2,
    )

    with pytest.raises(Exception):
        candidate.price = 200