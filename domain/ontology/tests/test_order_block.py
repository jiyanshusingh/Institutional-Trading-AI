from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from domain.ontology.order_block import (
    OrderBlock,
    OrderBlockDirection,
)


def test_create_bullish_order_block():

    block = OrderBlock(
        source_fair_value_gap_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=OrderBlockDirection.BULLISH,
    )

    assert block.is_bullish
    assert not block.is_bearish


def test_create_bearish_order_block():

    block = OrderBlock(
        source_fair_value_gap_index=2,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now() + timedelta(minutes=15),
        upper_price=110,
        lower_price=100,
        direction=OrderBlockDirection.BEARISH,
    )

    assert block.is_bearish
    assert not block.is_bullish


def test_negative_source_fair_value_gap_not_allowed():

    with pytest.raises(ValueError):

        OrderBlock(
            source_fair_value_gap_index=-1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=110,
            lower_price=100,
            direction=OrderBlockDirection.BULLISH,
        )


def test_positive_prices_required():

    with pytest.raises(ValueError):

        OrderBlock(
            source_fair_value_gap_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=-110,
            lower_price=100,
            direction=OrderBlockDirection.BULLISH,
        )


def test_upper_price_must_be_greater_than_lower_price():

    with pytest.raises(ValueError):

        OrderBlock(
            source_fair_value_gap_index=1,
            start_timestamp=datetime.now(),
            end_timestamp=datetime.now(),
            upper_price=95,
            lower_price=100,
            direction=OrderBlockDirection.BULLISH,
        )


def test_end_timestamp_after_start_timestamp():

    now = datetime.now()

    with pytest.raises(ValueError):

        OrderBlock(
            source_fair_value_gap_index=1,
            start_timestamp=now,
            end_timestamp=now - timedelta(minutes=15),
            upper_price=110,
            lower_price=100,
            direction=OrderBlockDirection.BULLISH,
        )


def test_order_block_height():

    block = OrderBlock(
        source_fair_value_gap_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=OrderBlockDirection.BULLISH,
    )

    assert block.height == 10


def test_order_block_is_immutable():

    block = OrderBlock(
        source_fair_value_gap_index=1,
        start_timestamp=datetime.now(),
        end_timestamp=datetime.now(),
        upper_price=110,
        lower_price=100,
        direction=OrderBlockDirection.BULLISH,
    )

    with pytest.raises(FrozenInstanceError):
        block.upper_price = 120