import pytest

from domain.reasoning.structural_context import StructuralContext


def build_context():

    return StructuralContext(
        context="Bullish Expansion",

        dominant_expansion="Bullish",

        protected_structure="Bullish Protected Swing",

        latest_structure_event="Bullish BOS",

        observations=(
            "Expansion Active",
            "Protected Swing Intact",
        ),

        confidence_notes=(
            "No opposing CHOCH detected.",
        ),
    )


def test_creation():

    context = build_context()

    assert context.context == "Bullish Expansion"


def test_is_bullish():

    context = build_context()

    assert context.is_bullish()


def test_is_not_bearish():

    context = build_context()

    assert not context.is_bearish()


def test_observation_count():

    context = build_context()

    assert context.observation_count() == 2


def test_summary():

    context = build_context()

    assert "Bullish Expansion" in context.summary()


def test_is_frozen():

    context = build_context()

    with pytest.raises(AttributeError):
        context.context = "Bearish Expansion"