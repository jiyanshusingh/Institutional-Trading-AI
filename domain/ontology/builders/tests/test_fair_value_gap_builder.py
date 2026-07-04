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

from domain.ontology.builders.fair_value_gap_builder import (
    FairValueGapBuilder,
)

from domain.ontology.fair_value_gap import (
    FairValueGap,
)

from domain.ontology.candidates.ict.ict_fair_value_gap_candidate_detector import (
    ICTFairValueGapCandidateDetector,
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


def create_builder():

    detector = ICTFairValueGapCandidateDetector()

    policy = ICTFairValueGapConfirmationPolicy()

    return FairValueGapBuilder(
        detector=detector,
        confirmation_policy=policy,
    )


def test_builder_returns_tuple():

    builder = create_builder()

    gaps = builder.build(
        create_model(),
    )

    assert isinstance(
        gaps,
        tuple,
    )


def test_builder_returns_fair_value_gap_objects():

    builder = create_builder()

    gaps = builder.build(
        create_model(),
    )

    assert all(
        isinstance(gap, FairValueGap)
        for gap in gaps
    )


def test_builder_initially_returns_empty_tuple():

    builder = create_builder()

    gaps = builder.build(
        create_model(),
    )

    assert len(gaps) == 0


def test_builder_requires_model():

    builder = create_builder()

    with pytest.raises(ValueError):

        builder.build(None)