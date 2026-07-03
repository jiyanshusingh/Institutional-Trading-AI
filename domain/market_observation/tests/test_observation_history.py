import pytest
from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_metadata import ObservationMetadata
from domain.market_observation.observation_history import ObservationHistory


def create_observations():

    return (
        MarketObservation(
            datetime(2026, 1, 1, 9, 15),
            100,
            105,
            99,
            103,
            100,
        ),
        MarketObservation(
            datetime(2026, 1, 1, 9, 30),
            103,
            106,
            102,
            105,
            110,
        ),
    )


def create_metadata():

    return ObservationMetadata(
        symbol="MARICO.NS",
        timeframe="15m",
        start_time=datetime(2026, 1, 1, 9, 15),
        end_time=datetime(2026, 1, 1, 9, 30),
        observation_count=2,
    )


def test_create_valid_observation_history():

    history = ObservationHistory(
        observations=create_observations(),
        metadata=create_metadata(),
    )

    assert len(history) == 2


def test_first_property():

    history = ObservationHistory(
        observations=create_observations(),
        metadata=create_metadata(),
    )

    assert history.first.open == 100


def test_last_property():

    history = ObservationHistory(
        observations=create_observations(),
        metadata=create_metadata(),
    )

    assert history.last.close == 105


def test_indexing():

    history = ObservationHistory(
        observations=create_observations(),
        metadata=create_metadata(),
    )

    assert history[0].open == 100


def test_iteration():

    history = ObservationHistory(
        observations=create_observations(),
        metadata=create_metadata(),
    )

    count = 0

    for _ in history:
        count += 1

    assert count == 2


def test_empty_history_not_allowed():

    with pytest.raises(ValueError):

        ObservationHistory(
            observations=(),
            metadata=create_metadata(),
        )