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

from domain.ontology.candidates.ict.ict_protected_swing_candidate_detector import (
    ICTProtectedSwingCandidateDetector,
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

    history = ObservationHistory(
        observations=observations,
        metadata=metadata,
    )

    return CanonicalMarketModel(
        observation_history=history,
    )


def test_returns_tuple():

    detector = ICTProtectedSwingCandidateDetector()

    candidates = detector.detect(
        create_model(),
    )

    assert isinstance(
        candidates,
        tuple,
    )


def test_initially_returns_empty_tuple():

    detector = ICTProtectedSwingCandidateDetector()

    candidates = detector.detect(
        create_model(),
    )

    assert len(candidates) == 0


def test_requires_model():

    detector = ICTProtectedSwingCandidateDetector()

    with pytest.raises(ValueError):

        detector.detect(None)