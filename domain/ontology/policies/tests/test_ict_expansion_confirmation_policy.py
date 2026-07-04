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

from domain.ontology.expansion import (
    ExpansionDirection,
)

from domain.ontology.candidates.expansion_candidate import (
    ExpansionCandidate,
)

from domain.ontology.policies.expansion_confirmation_result import (
    ExpansionConfirmationResult,
)

from domain.ontology.policies.ict.ict_expansion_confirmation_policy import (
    ICTExpansionConfirmationPolicy,
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

    now = datetime.now()

    return ExpansionCandidate(
        base_swing_index=1,
        confirmation_event_index=2,
        start_timestamp=now,
        end_timestamp=now,
        start_price=100,
        end_price=110,
        direction=ExpansionDirection.BULLISH,
    )


def test_confirm_returns_confirmation_result():

    policy = ICTExpansionConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert result.confirmed is True


def test_confirmation_index_matches_candidate():

    candidate = create_candidate()

    policy = ICTExpansionConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_model(),
    )

    assert (
        result.confirmation_index
        == candidate.confirmation_event_index
    )


def test_returns_confirmation_result_object():

    policy = ICTExpansionConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert isinstance(
        result,
        ExpansionConfirmationResult,
    )


def test_requires_model():

    policy = ICTExpansionConfirmationPolicy()

    with pytest.raises(ValueError):

        policy.confirm(
            create_candidate(),
            None,
        )