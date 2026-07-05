import pytest
from datetime import datetime

from domain.market_observation.market_observation import (
    MarketObservation,
)
from domain.market_observation.observation_history import (
    ObservationHistory,
)
from domain.market_observation.observation_metadata import (
    ObservationMetadata,
)

from domain.ontology.candidates.ict.ict_structure_event_candidate_detector import (
    ICTStructureEventCandidateDetector,
)

from domain.ontology.swing import Swing


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


def create_swings() -> tuple[Swing, ...]:
    """
    Placeholder detector currently ignores swings.

    An empty tuple is sufficient until the
    BOS/CHOCH implementation is added.
    """
    return ()


def test_returns_tuple():

    detector = ICTStructureEventCandidateDetector()

    candidates = detector.detect(
        observation_history=create_history(),
        swings=create_swings(),
    )

    assert isinstance(candidates, tuple)


def test_initially_returns_empty_tuple():

    detector = ICTStructureEventCandidateDetector()

    candidates = detector.detect(
        observation_history=create_history(),
        swings=create_swings(),
    )

    assert len(candidates) == 0


def test_requires_history():

    detector = ICTStructureEventCandidateDetector()

    with pytest.raises(ValueError):

        detector.detect(
            observation_history=None,
            swings=create_swings(),
        )


def test_requires_swings():

    detector = ICTStructureEventCandidateDetector()

    with pytest.raises(ValueError):

        detector.detect(
            observation_history=create_history(),
            swings=None,
        )