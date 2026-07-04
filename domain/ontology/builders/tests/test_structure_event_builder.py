from datetime import datetime

import pytest

from domain.market_observation.market_observation import MarketObservation
from domain.market_observation.observation_history import ObservationHistory
from domain.market_observation.observation_metadata import ObservationMetadata

from domain.ontology.builders.structure_event_builder import (
    StructureEventBuilder,
)

from domain.ontology.structure_event import (
    StructureEvent,
)

from domain.ontology.candidates.ict.ict_structure_event_candidate_detector import (
    ICTStructureEventCandidateDetector,
)

from domain.ontology.policies.ict.ict_structure_event_confirmation_policy import (
    ICTStructureEventConfirmationPolicy,
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
        symbol="TEST",
        timeframe="15m",
        start_time=observations[0].timestamp,
        end_time=observations[-1].timestamp,
        observation_count=len(observations),
    )

    return ObservationHistory(
        observations=observations,
        metadata=metadata,
    )


def create_builder():

    detector = ICTStructureEventCandidateDetector()

    confirmation_policy = (
        ICTStructureEventConfirmationPolicy()
    )

    return StructureEventBuilder(
        detector=detector,
        confirmation_policy=confirmation_policy,
    )


def test_builder_returns_tuple():

    builder = create_builder()

    events = builder.build(
        create_history(),
    )

    assert isinstance(events, tuple)


def test_builder_initially_returns_empty_tuple():

    builder = create_builder()

    events = builder.build(
        create_history(),
    )

    assert len(events) == 0


def test_builder_returns_structure_events():

    builder = create_builder()

    events = builder.build(
        create_history(),
    )

    assert all(
        isinstance(event, StructureEvent)
        for event in events
    )


def test_builder_requires_history():

    builder = create_builder()

    with pytest.raises(ValueError):

        builder.build(None)