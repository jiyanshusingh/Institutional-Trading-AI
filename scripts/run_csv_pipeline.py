from application.runtime.csv_runtime import (
    CSVRuntime,
)

from application.pipeline.trading_pipeline import (
    TradingPipeline,
)

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


def build_pipeline() -> TradingPipeline:

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


def main():

    runtime = CSVRuntime(
        trading_pipeline=build_pipeline(),
    )

    result = runtime.run(

        csv_path="historical_data/normalized/ACUTAAS_1m.csv",

        symbol="ACUTAAS",

        timeframe="15m",
    )

    print()

    print("=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    print(result.summary)

    print()

    print("=" * 60)
    print("CANONICAL MARKET MODEL")
    print("=" * 60)

    print(result.market.summary)

    print()

    print("=" * 60)
    print("MARKET THESES")
    print("=" * 60)

    for thesis in result.market_theses:

        print(thesis)

    print()

    print("=" * 60)
    print("OPPORTUNITIES")
    print("=" * 60)

    for opportunity in result.opportunities:

        print(opportunity)

    print()

    print("=" * 60)
    print("ASSESSMENTS")
    print("=" * 60)

    for assessment in result.opportunity_assessments:

        print(assessment)

    print()

    print("=" * 60)
    print("RANKINGS")
    print("=" * 60)

    for ranking in result.opportunity_rankings:

        print(ranking)

    print()

    print("=" * 60)
    print("PORTFOLIO")
    print("=" * 60)

    print(result.portfolio_decision)

    print()

    print("=" * 60)
    print("TRADES")
    print("=" * 60)

    for trade in result.trade_candidates:

        print(trade)

    print()

    print("=" * 60)
    print("EXECUTION PLANS")
    print("=" * 60)

    for plan in result.execution_plans:

        print(plan)

    print()

    print("=" * 60)
    print("PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()