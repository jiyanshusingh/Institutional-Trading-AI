from datetime import datetime

import pytest

from domain.market_observation.market_observation import (
    MarketObservation,
)
from domain.market_observation.observation_history import (
    ObservationHistory,
)
from domain.market_observation.observation_metadata import (
    ObservationMetadata,
)

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)

from domain.ontology.candidates.ict.ict_expansion_candidate_detector import (
    ICTExpansionCandidateDetector,
)


def create_model():

    observations = (
        MarketObservation(
            timestamp=datetime(2026, 1, 1, 9, 15),
            open=100,
            high=105,
            low=99,
            close=103,
            volume=100,
        ),
    )

    metadata = ObservationMetadata(
        symbol="TEST",
        timeframe="15m",
        start_time=observations[0].timestamp,
        end_time=observations[0].timestamp,
        observation_count=1,
    )

    history = ObservationHistory(
        observations=observations,
        metadata=metadata,
    )

    return CanonicalMarketModel(
        observation_history=history,
    )


def test_returns_tuple():

    detector = ICTExpansionCandidateDetector()

    candidates = detector.detect(
        create_model(),
    )

    assert isinstance(
        candidates,
        tuple,
    )


def test_initially_returns_empty_tuple():

    detector = ICTExpansionCandidateDetector()

    candidates = detector.detect(
        create_model(),
    )

    assert len(candidates) == 0


def test_requires_model():

    detector = ICTExpansionCandidateDetector()

    with pytest.raises(ValueError):

        detector.detect(None)