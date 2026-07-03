from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)


def create_history():

    observations = (
        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 15),
            open=100,
            high=105,
            low=99,
            close=103,
            volume=100,
        ),
        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 30),
            open=103,
            high=106,
            low=102,
            close=105,
            volume=120,
        ),
    )

    metadata = ObservationMetadata(
        symbol="MARICO.NS",
        timeframe="15m",
        start_time=observations[0].timestamp,
        end_time=observations[-1].timestamp,
        observation_count=len(observations),
    )

    return ObservationHistory(
        observations=observations,
        metadata=metadata,
    )


def test_create_empty_canonical_market_model():

    history = create_history()

    model = CanonicalMarketModel(
        observation_history=history,
    )

    assert model.observation_history == history


def test_symbol_property():

    model = CanonicalMarketModel(
        observation_history=create_history(),
    )

    assert model.symbol == "MARICO.NS"


def test_timeframe_property():

    model = CanonicalMarketModel(
        observation_history=create_history(),
    )

    assert model.timeframe == "15m"


def test_observation_count():

    model = CanonicalMarketModel(
        observation_history=create_history(),
    )

    assert model.observation_count == 2


def test_default_semantic_constructs_are_empty():

    model = CanonicalMarketModel(
        observation_history=create_history(),
    )

    assert model.swings == ()
    assert model.structure_events == ()
    assert model.expansions == ()
    assert model.origin_regions == ()
    assert model.fair_value_gaps == ()
    assert model.order_blocks == ()


def test_summary():

    model = CanonicalMarketModel(
        observation_history=create_history(),
    )

    summary = model.summary

    assert summary["symbol"] == "MARICO.NS"
    assert summary["timeframe"] == "15m"
    assert summary["observations"] == 2
    assert summary["swings"] == 0
    assert summary["structure_events"] == 0
    assert summary["expansions"] == 0
    assert summary["origin_regions"] == 0
    assert summary["fair_value_gaps"] == 0
    assert summary["order_blocks"] == 0


def test_requires_observation_history():

    import pytest

    with pytest.raises(ValueError):

        CanonicalMarketModel(
            observation_history=None,
        )


def test_model_is_immutable():

    import pytest

    model = CanonicalMarketModel(
        observation_history=create_history(),
    )

    with pytest.raises(Exception):
        model.swings = ()