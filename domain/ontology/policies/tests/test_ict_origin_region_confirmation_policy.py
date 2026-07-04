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

from domain.ontology.origin_region import (
    OriginRegionDirection,
)

from domain.ontology.candidates.origin_region_candidate import (
    OriginRegionCandidate,
)

from domain.ontology.policies.origin_region_confirmation_result import (
    OriginRegionConfirmationResult,
)

from domain.ontology.policies.ict.ict_origin_region_confirmation_policy import (
    ICTOriginRegionConfirmationPolicy,
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

    return OriginRegionCandidate(
        source_expansion_index=1,
        start_timestamp=now,
        end_timestamp=now,
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BULLISH,
    )


def test_confirm_returns_confirmation_result():

    policy = ICTOriginRegionConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert result.confirmed is True


def test_confirmation_index_matches_candidate():

    candidate = create_candidate()

    policy = ICTOriginRegionConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_model(),
    )

    assert (
        result.confirmation_index
        == candidate.source_expansion_index
    )


def test_returns_confirmation_result_object():

    policy = ICTOriginRegionConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert isinstance(
        result,
        OriginRegionConfirmationResult,
    )


def test_requires_model():

    policy = ICTOriginRegionConfirmationPolicy()

    with pytest.raises(ValueError):

        policy.confirm(
            create_candidate(),
            None,
        )