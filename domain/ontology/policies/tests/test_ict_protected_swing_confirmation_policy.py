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

from domain.ontology.protected_swing import (
    ProtectedSwingType,
)

from domain.ontology.candidates.protected_swing_candidate import (
    ProtectedSwingCandidate,
)

from domain.ontology.policies.ict.ict_protected_swing_confirmation_policy import (
    ICTProtectedSwingConfirmationPolicy,
)

from domain.ontology.policies.protected_swing_confirmation_result import (
    ProtectedSwingConfirmationResult,
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


def create_candidate():

    return ProtectedSwingCandidate(
        swing_index=0,
        timestamp=datetime.now(),
        price=100,
        protected_type=ProtectedSwingType.HIGH,
        protecting_event_index=0,
    )


def test_confirm_returns_confirmation_result():

    policy = ICTProtectedSwingConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert result.confirmed is True


def test_confirmation_index_matches_candidate():

    candidate = create_candidate()

    policy = ICTProtectedSwingConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_model(),
    )

    assert (
        result.confirmation_index
        == candidate.protecting_event_index
    )


def test_returns_confirmation_result_object():

    policy = ICTProtectedSwingConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert isinstance(
        result,
        ProtectedSwingConfirmationResult,
    )


def test_requires_model():

    policy = ICTProtectedSwingConfirmationPolicy()

    with pytest.raises(ValueError):

        policy.confirm(
            create_candidate(),
            None,
        )