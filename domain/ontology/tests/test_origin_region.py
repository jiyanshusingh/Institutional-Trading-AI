from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.origin_region import (
    OriginRegion,
    OriginRegionDirection,
)


def test_create_bullish_origin_region():

    region = OriginRegion(
        source_expansion_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BULLISH,
    )

    assert region.is_bullish
    assert not region.is_bearish


def test_create_bearish_origin_region():

    region = OriginRegion(
        source_expansion_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BEARISH,
    )

    assert region.is_bearish
    assert not region.is_bullish


def test_negative_source_expansion_not_allowed():

    with pytest.raises(ValueError):

        OriginRegion(
            source_expansion_index=-1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=110,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_positive_prices_required():

    with pytest.raises(ValueError):

        OriginRegion(
            source_expansion_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=-110,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_upper_price_must_be_greater_than_lower_price():

    with pytest.raises(ValueError):

        OriginRegion(
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

        OriginRegion(
            source_expansion_index=1,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            upper_price=110,
            lower_price=100,
            direction=OriginRegionDirection.BULLISH,
        )


def test_region_height():

    region = OriginRegion(
        source_expansion_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BULLISH,
    )

    assert region.height == 10


def test_origin_region_is_immutable():

    region = OriginRegion(
        source_expansion_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=OriginRegionDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        region.upper_price = 120