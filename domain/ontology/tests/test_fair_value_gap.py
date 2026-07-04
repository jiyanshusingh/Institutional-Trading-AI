from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.fair_value_gap import (
    FairValueGap,
    FairValueGapDirection,
)


def test_create_bullish_fair_value_gap():

    gap = FairValueGap(
        source_origin_region_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BULLISH,
    )

    assert gap.is_bullish
    assert not gap.is_bearish


def test_create_bearish_fair_value_gap():

    gap = FairValueGap(
        source_origin_region_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BEARISH,
    )

    assert gap.is_bearish
    assert not gap.is_bullish


def test_negative_source_origin_region_not_allowed():

    with pytest.raises(ValueError):

        FairValueGap(
            source_origin_region_index=-1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=110,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_positive_prices_required():

    with pytest.raises(ValueError):

        FairValueGap(
            source_origin_region_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=-110,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_upper_price_must_be_greater_than_lower_price():

    with pytest.raises(ValueError):

        FairValueGap(
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

        FairValueGap(
            source_origin_region_index=1,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            upper_price=110,
            lower_price=100,
            direction=FairValueGapDirection.BULLISH,
        )


def test_gap_height():

    gap = FairValueGap(
        source_origin_region_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BULLISH,
    )

    assert gap.height == 10


def test_gap_is_immutable():

    gap = FairValueGap(
        source_origin_region_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=FairValueGapDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        gap.upper_price = 120