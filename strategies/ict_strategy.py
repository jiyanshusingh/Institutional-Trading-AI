"""
ICT Strategy — wraps the existing ICT trading pipeline
under the ExecutableStrategy interface.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("ict_strategy")


def _build_pipeline(stop_loss_multiplier=3.0, take_profit_multiplier=4.0, atr_period=14):
    from application.pipeline.trading_pipeline import TradingPipeline
    from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
    from domain.opportunity.ict_opportunity_generator import ICTOpportunityGenerator
    from domain.opportunity.ict_opportunity_assessor import ICTOpportunityAssessor
    from domain.opportunity.ict_opportunity_ranker import ICTOpportunityRanker
    from domain.portfolio.ict_portfolio_allocator import ICTPortfolioAllocator
    from domain.trade.ict_trade_constructor import ICTTradeConstructor
    from domain.execution.ict_execution_planner import ICTExecutionPlanner

    return TradingPipeline(
        reasoning_model=ICTReasoningModel(),
        opportunity_generator=ICTOpportunityGenerator(),
        opportunity_assessor=ICTOpportunityAssessor(),
        opportunity_ranker=ICTOpportunityRanker(),
        portfolio_allocator=ICTPortfolioAllocator(),
        trade_constructor=ICTTradeConstructor(
            stop_loss_multiplier=stop_loss_multiplier,
            take_profit_multiplier=take_profit_multiplier,
            atr_period=atr_period,
            min_risk_reward=0.0,
        ),
        execution_planner=ICTExecutionPlanner(),
    )


class ICTStrategy(ExecutableStrategy):
    def __init__(self, obs_builder=None, semantic_pipeline=None,
                 sl_mult=3.0, tp_mult=4.0, atr_period=14):
        from data.builders.observation_history_builder import ObservationHistoryBuilder
        from domain.semantic_construction.semantic_construction_pipeline import (
            SemanticConstructionPipeline,
        )
        self._obs_builder = obs_builder or ObservationHistoryBuilder()
        self._semantic_pipeline = semantic_pipeline or SemanticConstructionPipeline()
        self._trading_pipeline = _build_pipeline(
            stop_loss_multiplier=sl_mult,
            take_profit_multiplier=tp_mult,
            atr_period=atr_period,
        )

    @property
    def name(self) -> str:
        return "ICT — Inner Circle Trader"

    def run(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
        day_type: str = "",
        stock_type: str = "",
        **kwargs,
    ) -> StrategyResult:
        try:
            obs = self._obs_builder.build(
                df=df,
                symbol=symbol,
                timeframe=timeframe,
                source="BACKTEST",
            )
            market = self._semantic_pipeline.build(obs)
            result = self._trading_pipeline.run(market)
        except Exception as e:
            _log.warning(f"ICT pipeline error: {e}")
            return StrategyResult()

        tcs: list[TradeCandidate] = []
        for tc in result.trade_candidates:
            if not getattr(tc, "is_executable", False):
                continue
            if tc.direction not in ("LONG", "SHORT"):
                continue
            if tc.entry_price is None or tc.stop_loss is None or tc.take_profit is None:
                continue

            score = 0
            for r in result.opportunity_rankings:
                if r.symbol == tc.symbol and r.timeframe == tc.timeframe and r.direction == tc.direction:
                    score = r.ranking_score
                    break

            tcs.append(TradeCandidate(
                direction=tc.direction,
                entry_price=tc.entry_price,
                stop_loss=tc.stop_loss,
                take_profit=tc.take_profit,
                is_executable=True,
                rationale=getattr(tc, "rationale", ""),
                symbol=symbol,
                timeframe=timeframe,
                ranking_score=score,
            ))

        return StrategyResult(trade_candidates=tcs)
