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

from domain.ontology.builders.origin_region_builder import (
    OriginRegionBuilder,
)

from domain.ontology.origin_region import (
    OriginRegion,
)

from domain.ontology.candidates.ict.ict_origin_region_candidate_detector import (
    ICTOriginRegionCandidateDetector,
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


def create_builder():

    detector = ICTOriginRegionCandidateDetector()

    policy = ICTOriginRegionConfirmationPolicy()

    return OriginRegionBuilder(
        detector=detector,
        confirmation_policy=policy,
    )


def test_builder_returns_tuple():

    builder = create_builder()

    regions = builder.build(
        create_model(),
    )

    assert isinstance(
        regions,
        tuple,
    )


def test_builder_returns_origin_regions():

    builder = create_builder()

    regions = builder.build(
        create_model(),
    )

    assert all(
        isinstance(region, OriginRegion)
        for region in regions
    )


def test_builder_initially_returns_empty_tuple():

    builder = create_builder()

    regions = builder.build(
        create_model(),
    )

    assert len(regions) == 0


def test_builder_requires_model():

    builder = create_builder()

    with pytest.raises(ValueError):

        builder.build(None)