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

from domain.ontology.builders.protected_swing_builder import (
    ProtectedSwingBuilder,
)

from domain.ontology.protected_swing import (
    ProtectedSwing,
)

from domain.ontology.candidates.ict.ict_protected_swing_candidate_detector import (
    ICTProtectedSwingCandidateDetector,
)

from domain.ontology.policies.ict.ict_protected_swing_confirmation_policy import (
    ICTProtectedSwingConfirmationPolicy,
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


def create_builder():

    detector = ICTProtectedSwingCandidateDetector()

    confirmation_policy = (
        ICTProtectedSwingConfirmationPolicy()
    )

    return ProtectedSwingBuilder(
        detector=detector,
        confirmation_policy=confirmation_policy,
    )


def test_builder_returns_tuple():

    builder = create_builder()

    protected_swings = builder.build(
        create_model(),
    )

    assert isinstance(
        protected_swings,
        tuple,
    )


def test_builder_returns_protected_swings():

    builder = create_builder()

    protected_swings = builder.build(
        create_model(),
    )

    assert all(
        isinstance(
            protected_swing,
            ProtectedSwing,
        )
        for protected_swing in protected_swings
    )


def test_builder_initially_returns_empty_tuple():

    builder = create_builder()

    protected_swings = builder.build(
        create_model(),
    )

    assert len(protected_swings) == 0


def test_builder_requires_model():

    builder = create_builder()

    with pytest.raises(ValueError):

        builder.build(None)