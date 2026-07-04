from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
from domain.reasoning.structural_context import StructuralContext


def make_context(name):

    return StructuralContext(
        context=name,
        dominant_expansion="BULLISH",
        protected_structure="Present",
        latest_structure_event="BOS",
        observations=(),
        confidence_notes=(),
    )


def test_bullish_forecast():

    model = ICTReasoningModel()

    forecast = model._generate_expected_structural_evolution(
        make_context("Bullish Expansion")
    )

    assert "bullish structural expansion" in forecast.lower()


def test_bearish_forecast():

    model = ICTReasoningModel()

    forecast = model._generate_expected_structural_evolution(
        make_context("Bearish Expansion")
    )

    assert "bearish structural expansion" in forecast.lower()


def test_transition_forecast():

    model = ICTReasoningModel()

    forecast = model._generate_expected_structural_evolution(
        make_context("Transition")
    )

    assert "additional structural confirmation" in forecast.lower()


def test_indeterminate_forecast():

    model = ICTReasoningModel()

    forecast = model._generate_expected_structural_evolution(
        make_context("Indeterminate")
    )

    assert "no justified structural evolution" in forecast.lower()