from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.candidates.origin_region_candidate import (
    OriginRegionCandidate,
)

from domain.ontology.origin_region import (
    OriginRegionDirection,
)


def test_create_bullish_candidate():

    candidate = OriginRegionCandidate(
        source_expansion_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BULLISH,
    )

    assert (
        candidate.direction
        == OriginRegionDirection.BULLISH
    )


def test_create_bearish_candidate():

    candidate = OriginRegionCandidate(
        source_expansion_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BEARISH,
    )

    assert (
        candidate.direction
        == OriginRegionDirection.BEARISH
    )


def test_negative_source_expansion_not_allowed():

    with pytest.raises(ValueError):

        OriginRegionCandidate(
            source_expansion_index=-1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=110,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_positive_prices_required():

    with pytest.raises(ValueError):

        OriginRegionCandidate(
            source_expansion_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=-110,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_upper_price_must_be_greater_than_lower_price():

    with pytest.raises(ValueError):

        OriginRegionCandidate(
            source_expansion_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=95,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_end_timestamp_after_start_timestamp():

    now = datetime.now()

    with pytest.raises(ValueError):

        OriginRegionCandidate(
            source_expansion_index=1,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            upper_price=110,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_candidate_is_immutable():

    candidate = OriginRegionCandidate(
        source_expansion_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        candidate.upper_price = 120