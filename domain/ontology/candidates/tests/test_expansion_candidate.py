from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.candidates.expansion_candidate import (
    ExpansionCandidate,
)

from domain.ontology.expansion import (
    ExpansionDirection,
)


def test_create_bullish_candidate():

    candidate = ExpansionCandidate(
        base_swing_index=5,
        confirmation_event_index=8,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        start_price=100,
        end_price=110,
        direction=ExpansionDirection.BULLISH,
    )

    assert candidate.direction == ExpansionDirection.BULLISH


def test_create_bearish_candidate():

    candidate = ExpansionCandidate(
        base_swing_index=10,
        confirmation_event_index=15,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        start_price=110,
        end_price=95,
        direction=ExpansionDirection.BEARISH,
    )

    assert candidate.direction == ExpansionDirection.BEARISH


def test_negative_base_swing_index():

    with pytest.raises(ValueError):

        ExpansionCandidate(
            base_swing_index=-1,
            confirmation_event_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            start_price=100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_negative_confirmation_event_index():

    with pytest.raises(ValueError):

        ExpansionCandidate(
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

        ExpansionCandidate(
            base_swing_index=1,
            confirmation_event_index=2,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            start_price=-100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_end_timestamp_after_start_timestamp():

    now = datetime.now()

    with pytest.raises(ValueError):

        ExpansionCandidate(
            base_swing_index=1,
            confirmation_event_index=2,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            start_price=100,
            end_price=105,
            direction=ExpansionDirection.BULLISH,
        )


def test_candidate_is_immutable():

    candidate = ExpansionCandidate(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        start_price=100,
        end_price=105,
        direction=ExpansionDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        candidate.start_price = 120