from datetime import UTC, datetime

from domain.reasoning.contracts.reasoning_model import ReasoningModel
from domain.thesis.market_thesis import MarketThesis


class DummyReasoningModel(ReasoningModel):

    @property
    def model_name(self) -> str:
        return "Dummy"

    @property
    def theory(self) -> str:
        return "Test Theory"

    @property
    def version(self) -> str:
        return "1.0"

    def construct_market_theses(
        self,
        market,
        objectives=None,
        constraints=None,
    ):
        return (
            MarketThesis(
                thesis_id="TH-001",
                created_at=datetime.now(UTC),

                symbol="TEST",
                timeframe="15m",

                reasoning_model=self.model_name,
                theory=self.theory,
                version=self.version,

                market_regime="Trending",
                session="Regular",

                central_claim="Dummy market explanation.",

                supporting_evidence=("Expansion",),

                counter_evidence=(),

                assumptions=(),

                expected_structural_evolution="Continuation",

                invalidation=("Bearish CHOCH",),

                uncertainty="LOW",
            ),
        )


def test_reasoning_model_metadata():

    model = DummyReasoningModel()

    assert model.model_name == "Dummy"
    assert model.theory == "Test Theory"
    assert model.version == "1.0"


def test_reasoning_model_returns_market_theses():

    model = DummyReasoningModel()

    theses = model.construct_market_theses(market=None)

    assert isinstance(theses, tuple)
    assert len(theses) == 1
    assert isinstance(theses[0], MarketThesis)


def test_market_thesis_contains_expected_claim():

    model = DummyReasoningModel()

    thesis = model.construct_market_theses(None)[0]

    assert thesis.central_claim == "Dummy market explanation."


def test_market_thesis_is_falsifiable():

    model = DummyReasoningModel()

    thesis = model.construct_market_theses(None)[0]

    assert thesis.is_falsifiable()