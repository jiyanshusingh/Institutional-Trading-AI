from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
from domain.thesis.market_thesis import MarketThesis
from domain.reasoning.structural_context import StructuralContext


class DummyCanonicalMarketModel:
    """
    Minimal CanonicalMarketModel stub for reasoning tests.
    """

    symbol = "RELIANCE"
    timeframe = "15m"

    expansions = ()
    structure_events = ()
    protected_swings = ()


def test_metadata():

    model = ICTReasoningModel()

    assert model.model_name == "ICTReasoningModel"
    assert model.theory == "ICT"
    assert model.version == "1.0"


def test_returns_tuple():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    theses = model.construct_market_theses(market)

    assert isinstance(theses, tuple)


def test_returns_single_market_thesis():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    theses = model.construct_market_theses(market)

    assert len(theses) == 1
    assert isinstance(theses[0], MarketThesis)


def test_symbol_propagates():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    thesis = model.construct_market_theses(market)[0]

    assert thesis.symbol == "RELIANCE"


def test_timeframe_propagates():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    thesis = model.construct_market_theses(market)[0]

    assert thesis.timeframe == "15m"


def test_market_thesis_is_falsifiable():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    thesis = model.construct_market_theses(market)[0]

    assert thesis.is_falsifiable()


def test_market_thesis_has_central_claim():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    thesis = model.construct_market_theses(market)[0]

    assert thesis.central_claim != ""


def test_market_thesis_contains_evidence_tuple():

    model = ICTReasoningModel()

    market = DummyCanonicalMarketModel()

    thesis = model.construct_market_theses(market)[0]

    assert isinstance(thesis.supporting_evidence, tuple)
    assert isinstance(thesis.counter_evidence, tuple)
    
def test_generate_expected_structural_evolution_bullish():

    model = ICTReasoningModel()

    context = StructuralContext(
        context="Bullish Expansion",
        dominant_expansion="BULLISH",
        protected_structure="Present",
        latest_structure_event="BOS",
        observations=(),
        confidence_notes=(),
    )

    forecast = model._generate_expected_structural_evolution(
        context
    )

    assert (
        "bullish structural expansion"
        in forecast.lower()
    )
def test_generate_expected_structural_evolution_transition():

    model = ICTReasoningModel()

    context = StructuralContext(
        context="Transition",
        dominant_expansion="BULLISH",
        protected_structure="Present",
        latest_structure_event="CHOCH",
        observations=(),
        confidence_notes=(),
    )

    forecast = model._generate_expected_structural_evolution(
        context
    )

    assert (
        "additional structural confirmation"
        in forecast.lower()
    )
def test_generate_expected_structural_evolution_indeterminate():

    model = ICTReasoningModel()

    context = StructuralContext(
        context="Indeterminate",
        dominant_expansion="None",
        protected_structure="Absent",
        latest_structure_event="None",
        observations=(),
        confidence_notes=(),
    )

    forecast = model._generate_expected_structural_evolution(
        context
    )

    assert (
        "no justified structural evolution"
        in forecast.lower()
    )