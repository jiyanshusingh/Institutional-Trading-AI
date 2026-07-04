from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.candidates.fair_value_gap_candidate import (
    FairValueGapCandidate,
)

from domain.ontology.fair_value_gap import (
    FairValueGapDirection,
)


def test_create_bullish_candidate():

    candidate = FairValueGapCandidate(
        source_origin_region_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BULLISH,
    )

    assert (
        candidate.direction
        == FairValueGapDirection.BULLISH
    )


def test_create_bearish_candidate():

    candidate = FairValueGapCandidate(
        source_origin_region_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BEARISH,
    )

    assert (
        candidate.direction
        == FairValueGapDirection.BEARISH
    )


def test_negative_source_origin_region_not_allowed():

    with pytest.raises(ValueError):

        FairValueGapCandidate(
            source_origin_region_index=-1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=110,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_positive_prices_required():

    with pytest.raises(ValueError):

        FairValueGapCandidate(
            source_origin_region_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=-110,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_upper_price_must_be_greater_than_lower_price():

    with pytest.raises(ValueError):

        FairValueGapCandidate(
            source_origin_region_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=95,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_end_timestamp_after_start_timestamp():

    now = datetime.now()

    with pytest.raises(ValueError):

        FairValueGapCandidate(
            source_origin_region_index=1,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            upper_price=110,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_candidate_is_immutable():

    candidate = FairValueGapCandidate(
        source_origin_region_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        candidate.upper_price = 120