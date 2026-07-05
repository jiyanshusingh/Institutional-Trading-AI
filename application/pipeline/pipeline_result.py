"""
Pipeline Result

Version 1.0

A PipelineResult represents the complete output of the
Institutional Trading AI runtime pipeline.

It is an immutable snapshot of every stage of reasoning.

It performs no computation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)
from domain.thesis.market_thesis import MarketThesis
from domain.opportunity.opportunity import Opportunity
from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)
from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)
from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)
from domain.trade.trade_candidate import TradeCandidate
from domain.execution.execution_plan import ExecutionPlan


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """
    Immutable aggregate representing one complete execution
    of the trading intelligence pipeline.
    """

    # ----------------------------------------------------------
    # Metadata
    # ----------------------------------------------------------

    pipeline_id: str

    created_at: datetime

    # ----------------------------------------------------------
    # Input
    # ----------------------------------------------------------

    market: CanonicalMarketModel

    # ----------------------------------------------------------
    # Reasoning
    # ----------------------------------------------------------

    market_theses: tuple[MarketThesis, ...]

    # ----------------------------------------------------------
    # Opportunity Intelligence
    # ----------------------------------------------------------

    opportunities: tuple[Opportunity, ...]

    opportunity_assessments: tuple[
        OpportunityAssessment,
        ...
    ]

    opportunity_rankings: tuple[
        OpportunityRanking,
        ...
    ]

    # ----------------------------------------------------------
    # Portfolio Intelligence
    # ----------------------------------------------------------

    portfolio_decision: PortfolioDecision

    # ----------------------------------------------------------
    # Trade Construction
    # ----------------------------------------------------------

    trade_candidates: tuple[
        TradeCandidate,
        ...
    ]

    # ----------------------------------------------------------
    # Execution Planning
    # ----------------------------------------------------------

    execution_plans: tuple[
        ExecutionPlan,
        ...
    ]

    # ==========================================================
    # Validation
    # ==========================================================

    def __post_init__(self):

        if not self.pipeline_id:
            raise ValueError(
                "Pipeline ID cannot be empty."
            )

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def thesis_count(self) -> int:
        return len(self.market_theses)

    @property
    def opportunity_count(self) -> int:
        return len(self.opportunities)

    @property
    def assessment_count(self) -> int:
        return len(self.opportunity_assessments)

    @property
    def ranking_count(self) -> int:
        return len(self.opportunity_rankings)

    @property
    def trade_count(self) -> int:
        return len(self.trade_candidates)

    @property
    def execution_plan_count(self) -> int:
        return len(self.execution_plans)

    @property
    def summary(self) -> dict:

        return {
            "symbol": self.market.symbol,
            "timeframe": self.market.timeframe,
            "theses": self.thesis_count,
            "opportunities": self.opportunity_count,
            "assessments": self.assessment_count,
            "rankings": self.ranking_count,
            "trades": self.trade_count,
            "execution_plans": self.execution_plan_count,
        }

    def __str__(self) -> str:

        return (
            f"PipelineResult("
            f"symbol={self.market.symbol}, "
            f"timeframe={self.market.timeframe}, "
            f"opportunities={self.opportunity_count}, "
            f"trades={self.trade_count})"
        )