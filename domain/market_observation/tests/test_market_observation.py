import pytest
from datetime import datetime

from domain.market_observation.market_observation import MarketObservation


def test_create_valid_market_observation():

    observation = MarketObservation(
        timestamp=datetime(2026, 1, 1, 9, 15),
        open=100,
        high=105,
        low=99,
        close=103,
        volume=1000,
    )

    assert observation.open == 100
    assert observation.high == 105
    assert observation.low == 99
    assert observation.close == 103
    assert observation.volume == 1000


def test_high_must_be_greater_than_or_equal_to_all_prices():

    with pytest.raises(ValueError):

        MarketObservation(
            timestamp=datetime.now(),
            open=100,
            high=99,
            low=95,
            close=98,
            volume=100,
        )


def test_low_must_be_less_than_or_equal_to_all_prices():

    with pytest.raises(ValueError):

        MarketObservation(
            timestamp=datetime.now(),
            open=100,
            high=105,
            low=101,
            close=103,
            volume=100,
        )


def test_negative_volume_not_allowed():

    with pytest.raises(ValueError):

        MarketObservation(
            timestamp=datetime.now(),
            open=100,
            high=105,
            low=99,
            close=103,
            volume=-1,
        )


def test_market_observation_is_immutable():

    observation = MarketObservation(
        timestamp=datetime.now(),
        open=100,
        high=105,
        low=99,
        close=103,
        volume=100,
    )

    with pytest.raises(Exception):
        observation.open = 200