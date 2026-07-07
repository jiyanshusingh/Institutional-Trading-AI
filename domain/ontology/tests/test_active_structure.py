from datetime import datetime

import pytest

from domain.ontology.active_structure import (
    ActiveStructure,
)
from domain.ontology.swing import Swing
from domain.ontology.swing_type import SwingType


def create_high(index=0):

    return Swing(
        index=index,
        confirmation_index=index + 1,
        timestamp=datetime.now(),
        price=100 + index,
        swing_type=SwingType.HIGH,
    )


def create_low(index=0):

    return Swing(
        index=index,
        confirmation_index=index + 1,
        timestamp=datetime.now(),
        price=100 + index,
        swing_type=SwingType.LOW,
    )


def test_accepts_empty_active_swings():

    structure = ActiveStructure(
        active_swings=(),
    )

    assert len(structure) == 0


def test_stores_active_swings():

    high = create_high(0)
    low = create_low(1)

    structure = ActiveStructure(
        active_swings=(
            high,
            low,
        ),
    )

    assert structure.active_swings == (
        high,
        low,
    )


def test_active_highs_returns_only_highs():

    high1 = create_high(0)
    low = create_low(1)
    high2 = create_high(2)

    structure = ActiveStructure(
        active_swings=(
            high1,
            low,
            high2,
        ),
    )

    assert structure.active_highs == (
        high1,
        high2,
    )


def test_active_lows_returns_only_lows():

    high = create_high(0)
    low1 = create_low(1)
    low2 = create_low(2)

    structure = ActiveStructure(
        active_swings=(
            high,
            low1,
            low2,
        ),
    )

    assert structure.active_lows == (
        low1,
        low2,
    )


def test_length_matches_active_swings():

    structure = ActiveStructure(
        active_swings=(
            create_high(0),
            create_low(1),
            create_high(2),
        ),
    )

    assert len(structure) == 3


def test_iteration_returns_active_swings():

    swings = (
        create_high(0),
        create_low(1),
        create_high(2),
    )

    structure = ActiveStructure(
        active_swings=swings,
    )

    assert tuple(structure) == swings


def test_none_active_swings_raises_value_error():

    with pytest.raises(ValueError):

        ActiveStructure(
            active_swings=None,
        )


def test_non_swing_objects_raise_type_error():

    with pytest.raises(TypeError):

        ActiveStructure(
            active_swings=(
                1,
                2,
                3,
            ),
        )