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

from domain.ontology.fair_value_gap import (
    FairValueGapDirection,
)

from domain.ontology.candidates.fair_value_gap_candidate import (
    FairValueGapCandidate,
)

from domain.ontology.policies.fair_value_gap_confirmation_result import (
    FairValueGapConfirmationResult,
)

from domain.ontology.policies.ict.ict_fair_value_gap_confirmation_policy import (
    ICTFairValueGapConfirmationPolicy,
)


def create_model():

    observation = MarketObservation(
        timestamp=datetime(2026, 1, 1, 9, 15),
        open=100,
        high=105,
        low=99,
        close=103,
        volume=100,
    )

    history = ObservationHistory(
        observations=(observation,),
        metadata=ObservationMetadata(
            symbol="TEST",
            timeframe="15m",
            start_time=observation.timestamp,
            end_time=observation.timestamp,
            observation_count=1,
        ),
    )

    return CanonicalMarketModel(
        observation_history=history,
    )


def create_candidate():

    now = datetime.now()

    return FairValueGapCandidate(
        source_origin_region_index=1,
        start_timestamp=now,
        end_timestamp=now,
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BULLISH,
    )


def test_confirm_returns_confirmation_result():

    policy = ICTFairValueGapConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert result.confirmed


def test_confirmation_index_matches_candidate():

    candidate = create_candidate()

    policy = ICTFairValueGapConfirmationPolicy()

    result = policy.confirm(
        candidate,
        create_model(),
    )

    assert (
        result.confirmation_index
        == candidate.source_origin_region_index
    )


def test_returns_confirmation_result_object():

    policy = ICTFairValueGapConfirmationPolicy()

    result = policy.confirm(
        create_candidate(),
        create_model(),
    )

    assert isinstance(
        result,
        FairValueGapConfirmationResult,
    )


def test_requires_model():

    policy = ICTFairValueGapConfirmationPolicy()

    with pytest.raises(ValueError):

        policy.confirm(
            create_candidate(),
            None,
        )