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


def test_pipeline_constructs_swings():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert isinstance(model.swings, tuple)
    
def test_pipeline_swing_count_matches_collection():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert model.swing_count == len(model.swings)

def test_pipeline_returns_only_swings_initially():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    # Stage 1 of the pipeline only constructs Swings.
    # Later semantic constructs will be added in future sprints.

    assert hasattr(model, "swings")

def test_pipeline_constructs_structure_events():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert isinstance(
        model.structure_events,
        tuple,
    )

def test_pipeline_structure_event_count():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert (
        model.structure_event_count
        == len(model.structure_events)
    )

def test_pipeline_constructs_expansions():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert isinstance(
        model.expansions,
        tuple,
    )

def test_pipeline_expansion_count_matches_collection():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert (
        model.expansion_count
        == len(model.expansions)
    )
    
def test_pipeline_initially_returns_no_expansions():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )
def test_pipeline_constructs_origin_regions():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert isinstance(
        model.origin_regions,
        tuple,
    )
def test_pipeline_origin_region_count_matches_collection():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert (
        model.origin_region_count
        == len(model.origin_regions)
    )
def test_pipeline_initially_returns_no_origin_regions():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert len(model.origin_regions) == 0

    assert len(model.expansions) == 0

def test_pipeline_constructs_fair_value_gaps():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert isinstance(
        model.fair_value_gaps,
        tuple,
    )
def test_pipeline_fair_value_gap_count_matches_collection():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert (
        model.fair_value_gap_count
        == len(model.fair_value_gaps)
    )
def test_pipeline_initially_returns_no_fair_value_gaps():

    pipeline = SemanticConstructionPipeline()

    model = pipeline.build(
        create_history(),
    )

    assert len(model.fair_value_gaps) == 0