from datetime import datetime

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.semantic_construction.semantic_construction_pipeline import (
    SemanticConstructionPipeline,
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


def test_pipeline_returns_canonical_market_model():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert isinstance(
        model,
        CanonicalMarketModel,
    )


def test_pipeline_preserves_observation_history():

    history = create_history()

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(history)

    assert model.observation_history == history


def test_pipeline_preserves_symbol():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert model.symbol == "MARICO.NS"


def test_pipeline_preserves_timeframe():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert model.timeframe == "15m"


def test_pipeline_initially_contains_no_semantic_constructs():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert len(model.swings) == 0
    assert len(model.structure_events) == 0
    assert len(model.expansions) == 0
    assert len(model.origin_regions) == 0
    assert len(model.fair_value_gaps) == 0
    assert len(model.order_blocks) == 0