from application.pipeline.trading_pipeline import TradingPipeline

from domain.reasoning.ict.ict_reasoning_model import (
    ICTReasoningModel,
)

from domain.opportunity.ict_opportunity_generator import (
    ICTOpportunityGenerator,
)

from domain.opportunity.ict_opportunity_assessor import (
    ICTOpportunityAssessor,
)

from domain.opportunity.ict_opportunity_ranker import (
    ICTOpportunityRanker,
)

from domain.portfolio.ict_portfolio_allocator import (
    ICTPortfolioAllocator,
)

from domain.trade.ict_trade_constructor import (
    ICTTradeConstructor,
)

from domain.execution.ict_execution_planner import (
    ICTExecutionPlanner,
)

from application.pipeline.pipeline_result import (
    PipelineResult,
)


class DummyMarket:
    """
    Minimal Canonical Market Model required
    for Version 1 runtime testing.
    """

    symbol = "RELIANCE"

    timeframe = "15m"

    expansions = ()

    structure_events = ()

    protected_swings = ()


def make_pipeline() -> TradingPipeline:

    return TradingPipeline(

        reasoning_model=ICTReasoningModel(),

        opportunity_generator=(
            ICTOpportunityGenerator()
        ),

        opportunity_assessor=(
            ICTOpportunityAssessor()
        ),

        opportunity_ranker=(
            ICTOpportunityRanker()
        ),

        portfolio_allocator=(
            ICTPortfolioAllocator()
        ),

        trade_constructor=(
            ICTTradeConstructor()
        ),

        execution_planner=(
            ICTExecutionPlanner()
        ),
    )


# ==========================================================
# Runtime
# ==========================================================

def test_pipeline_returns_pipeline_result():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert isinstance(
        result,
        PipelineResult,
    )


# ==========================================================
# Market
# ==========================================================

def test_market_propagates():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.market.symbol == "RELIANCE"

    assert result.market.timeframe == "15m"


# ==========================================================
# Reasoning
# ==========================================================

def test_market_thesis_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.thesis_count == 1


# ==========================================================
# Opportunity Intelligence
# ==========================================================

def test_opportunity_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.opportunity_count == 1


def test_assessment_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.assessment_count == 1


def test_ranking_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.ranking_count == 1


# ==========================================================
# Portfolio
# ==========================================================

def test_portfolio_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert (
        result.portfolio_decision
        is not None
    )


# ==========================================================
# Trade
# ==========================================================

def test_trade_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.trade_count == 1


# ==========================================================
# Execution
# ==========================================================

def test_execution_plan_created():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    assert result.execution_plan_count == 1


# ==========================================================
# Pipeline Integrity
# ==========================================================

def test_pipeline_summary():

    pipeline = make_pipeline()

    result = pipeline.run(
        DummyMarket()
    )

    summary = result.summary

    assert summary["symbol"] == "RELIANCE"

    assert summary["theses"] == 1

    assert summary["opportunities"] == 1

    assert summary["assessments"] == 1

    assert summary["rankings"] == 1

    assert summary["trades"] == 1

    assert summary["execution_plans"] == 1