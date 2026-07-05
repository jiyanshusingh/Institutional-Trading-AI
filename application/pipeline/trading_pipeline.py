from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from application.pipeline.pipeline_result import PipelineResult


class TradingPipeline:
    """
    Version 1 Trading Pipeline.

    Orchestrates the complete trading intelligence
    workflow.

    It contains no trading logic.

    It simply coordinates the domain components.
    """

    def __init__(
        self,
        reasoning_model,
        opportunity_generator,
        opportunity_assessor,
        opportunity_ranker,
        portfolio_allocator,
        trade_constructor,
        execution_planner,
    ):

        self.reasoning_model = reasoning_model

        self.opportunity_generator = (
            opportunity_generator
        )

        self.opportunity_assessor = (
            opportunity_assessor
        )

        self.opportunity_ranker = (
            opportunity_ranker
        )

        self.portfolio_allocator = (
            portfolio_allocator
        )

        self.trade_constructor = (
            trade_constructor
        )

        self.execution_planner = (
            execution_planner
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def run(
        self,
        market,
        objectives=None,
        constraints=None,
    ) -> PipelineResult:

        # ------------------------------------------------------
        # Reasoning
        # ------------------------------------------------------

        market_theses = (
            self.reasoning_model.construct_market_theses(
                market=market,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Opportunity Generation
        # ------------------------------------------------------

        opportunities = (
            self.opportunity_generator.generate(
                market_theses,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Opportunity Assessment
        # ------------------------------------------------------

        assessments = (
            self.opportunity_assessor.assess(
                opportunities,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Opportunity Ranking
        # ------------------------------------------------------

        rankings = (
            self.opportunity_ranker.rank(
                assessments,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Portfolio Allocation
        # ------------------------------------------------------

        portfolio_decision = (
            self.portfolio_allocator.allocate(
                rankings,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Trade Construction
        # ------------------------------------------------------

        trade_candidates = (
            self.trade_constructor.construct(
                portfolio_decision,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Execution Planning
        # ------------------------------------------------------

        execution_plans = (
            self.execution_planner.plan(
                trade_candidates,
                objectives=objectives,
                constraints=constraints,
            )
        )

        # ------------------------------------------------------
        # Aggregate Result
        # ------------------------------------------------------

        return PipelineResult(
            pipeline_id=str(uuid4()),
            created_at=datetime.now(UTC),

            market=market,

            market_theses=market_theses,

            opportunities=opportunities,

            opportunity_assessments=assessments,

            opportunity_rankings=rankings,

            portfolio_decision=portfolio_decision,

            trade_candidates=trade_candidates,

            execution_plans=execution_plans,
        )