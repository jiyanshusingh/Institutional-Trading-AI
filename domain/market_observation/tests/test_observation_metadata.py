import pytest
from datetime import datetime

from domain.market_observation.observation_metadata import ObservationMetadata


def test_create_valid_metadata():

    metadata = ObservationMetadata(
        symbol="MARICO.NS",
        timeframe="15m",
        start_time=datetime(2026, 1, 1),
        end_time=datetime(2026, 1, 2),
        observation_count=100,
    )

    assert metadata.symbol == "MARICO.NS"
    assert metadata.timeframe == "15m"
    assert metadata.observation_count == 100


def test_observation_count_must_be_positive():

    with pytest.raises(ValueError):

        ObservationMetadata(
            symbol="ABC",
            timeframe="1h",
            start_time=datetime.now(),
            end_time=datetime.now(),
            observation_count=0,
        )


def test_end_time_cannot_precede_start_time():

    with pytest.raises(ValueError):

        ObservationMetadata(
            symbol="ABC",
            timeframe="1h",
            start_time=datetime(2026, 1, 2),
            end_time=datetime(2026, 1, 1),
            observation_count=10,
        )


def test_symbol_cannot_be_empty():

    with pytest.raises(ValueError):

        ObservationMetadata(
            symbol="",
            timeframe="15m",
            start_time=datetime.now(),
            end_time=datetime.now(),
            observation_count=5,
        )


def test_timeframe_cannot_be_empty():

    with pytest.raises(ValueError):

        ObservationMetadata(
            symbol="ABC",
            timeframe="",
            start_time=datetime.now(),
            end_time=datetime.now(),
            observation_count=5,
        )