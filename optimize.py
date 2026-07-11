#!/usr/bin/env python3
"""
Hyperparameter optimization for the ICT trading pipeline.

Runs a grid search over ATR multipliers, minimum R:R,
and minimum score thresholds, reporting the best combination
by total P&L.
"""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass, field

import pandas as pd

from data.live.live_market_data_provider import LiveMarketDataProvider
from data.builders.observation_history_builder import ObservationHistoryBuilder
from domain.semantic_construction.semantic_construction_pipeline import SemanticConstructionPipeline
from backtesting.engine import BacktestingEngine

from domain.trade.ict_trade_constructor import ICTTradeConstructor
from domain.opportunity.ict_opportunity_generator import ICTOpportunityGenerator
from domain.opportunity.ict_opportunity_assessor import ICTOpportunityAssessor
from domain.opportunity.ict_opportunity_ranker import ICTOpportunityRanker
from domain.portfolio.ict_portfolio_allocator import ICTPortfolioAllocator
from domain.execution.ict_execution_planner import ICTExecutionPlanner
from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
from application.pipeline.trading_pipeline import TradingPipeline


@dataclass
class TrialResult:
    stop_mult: float
    target_mult: float
    atr_period: int
    min_rr: float
    total_trades: int
    win_rate: float
    profit_factor: float
    total_pnl: float
    max_drawdown: float
    avg_r_multiple: float


def build_pipeline(
    stop_mult: float = 1.5,
    target_mult: float = 2.0,
    atr_period: int = 14,
    min_rr: float = 0.0,
    available_capital: float = 100.0,
) -> TradingPipeline:
    return TradingPipeline(
        reasoning_model=ICTReasoningModel(),
        opportunity_generator=ICTOpportunityGenerator(),
        opportunity_assessor=ICTOpportunityAssessor(),
        opportunity_ranker=ICTOpportunityRanker(),
        portfolio_allocator=ICTPortfolioAllocator(),
        trade_constructor=ICTTradeConstructor(
            stop_loss_multiplier=stop_mult,
            take_profit_multiplier=target_mult,
            atr_period=atr_period,
            min_risk_reward=min_rr,
        ),
        execution_planner=ICTExecutionPlanner(),
        available_capital=available_capital,
    )


def run_trial(
    symbol: str,
    timeframe: str,
    obs_history,
    stop_mult: float,
    target_mult: float,
    atr_period: int,
    min_rr: float,
) -> TrialResult:
    pipeline = build_pipeline(
        stop_mult=stop_mult,
        target_mult=target_mult,
        atr_period=atr_period,
        min_rr=min_rr,
    )

    def run_pipeline(obs_window):
        semantic = SemanticConstructionPipeline()
        market = semantic.build(obs_window)
        return pipeline.run(market)

    engine = BacktestingEngine(pipeline_runner=run_pipeline)
    bt_result = engine.run(obs_history, symbol, timeframe)

    return TrialResult(
        stop_mult=stop_mult,
        target_mult=target_mult,
        atr_period=atr_period,
        min_rr=min_rr,
        total_trades=bt_result.total_trades,
        win_rate=bt_result.win_rate,
        profit_factor=bt_result.profit_factor,
        total_pnl=bt_result.total_pnl,
        max_drawdown=bt_result.max_drawdown,
        avg_r_multiple=bt_result.avg_r_multiple,
    )


def main():
    symbol = sys.argv[1] if len(sys.argv) > 1 else "ACUTAAS.NS"
    timeframe = sys.argv[2] if len(sys.argv) > 2 else "1d"
    lookback = int(sys.argv[3]) if len(sys.argv) > 3 else 600

    print(f"🔄 Fetching {lookback} candles of {symbol} ({timeframe})...")
    provider = LiveMarketDataProvider()
    df = provider.load_latest_data(
        symbol=symbol,
        timeframe=timeframe,
        lookback=lookback,
    )

    builder = ObservationHistoryBuilder()
    obs_history = builder.build(
        df=df,
        symbol=symbol,
        timeframe=timeframe,
        source="LIVE",
    )
    print(f"   Got {len(obs_history)} observations")

    param_grid = {
        "stop_mult": [1.0, 1.5, 2.0, 2.5, 3.0],
        "target_mult": [1.5, 2.0, 2.5, 3.0, 4.0],
        "atr_period": [10, 14, 21],
        "min_rr": [0.0, 1.0, 1.5],
    }

    keys = list(param_grid.keys())
    combos = list(itertools.product(*(param_grid[k] for k in keys)))
    total = len(combos)
    print(f"🔄 Running {total} parameter combinations...")

    results: list[TrialResult] = []
    baseline: TrialResult | None = None

    for idx, combo in enumerate(combos, 1):
        stop_mult, target_mult, atr_period, min_rr = combo
        try:
            r = run_trial(
                symbol, timeframe, obs_history,
                stop_mult, target_mult, atr_period, min_rr,
            )
            results.append(r)

            if (
                stop_mult == 1.5
                and target_mult == 2.0
                and atr_period == 14
                and min_rr == 0.0
            ):
                baseline = r

            if idx % 10 == 0 or idx == total:
                print(f"   Progress: {idx}/{total} combos")
        except Exception as e:
            print(f"   ✗ Combo {idx} failed: {e}")

    if not results:
        print("❌ No successful trials")
        return

    results.sort(key=lambda r: r.total_pnl, reverse=True)

    print("\n" + "=" * 80)
    print("OPTIMIZATION RESULTS")
    print("=" * 80)

    print(f"\n📊 Baseline (1.5x stop, 2.0x target, ATR 14, no filter):")
    if baseline:
        print(f"   Trades: {baseline.total_trades} | Win Rate: {baseline.win_rate:.1f}% | "
              f"PF: {baseline.profit_factor:.2f} | P&L: ${baseline.total_pnl:.2f} | "
              f"DD: {baseline.max_drawdown:.1f}% | AvgR: {baseline.avg_r_multiple:.2f}")
    else:
        print("   (not found in results)")

    print(f"\n🏆 Top 10 by Total P&L:")
    print(f"   {'Rank':<5} {'Stop':<6} {'Target':<7} {'ATR':<4} {'MinRR':<6} "
          f"{'Trades':<7} {'Win%':<7} {'PF':<6} {'P&L':<10} {'DD%':<6} {'AvgR':<6}")
    print(f"   " + "-" * 70)
    for rank, r in enumerate(results[:10], 1):
        print(f"   {rank:<5} {r.stop_mult:<6.1f} {r.target_mult:<7.1f} {r.atr_period:<4} "
              f"{r.min_rr:<6.1f} {r.total_trades:<7} {r.win_rate:<6.1f}% "
              f"{r.profit_factor:<6.2f} ${r.total_pnl:<8.2f} {r.max_drawdown:<5.1f}% "
              f"{r.avg_r_multiple:<6.2f}")

    print(f"\n🏆 Top 3 by Profit Factor (min 20 trades):")
    filtered = [r for r in results if r.total_trades >= 20]
    filtered.sort(key=lambda r: r.profit_factor, reverse=True)
    for rank, r in enumerate(filtered[:3], 1):
        print(f"   {rank}. Stop={r.stop_mult:.1f} Target={r.target_mult:.1f} "
              f"ATR={r.atr_period} MinRR={r.min_rr:.1f} → "
              f"Win={r.win_rate:.1f}% PF={r.profit_factor:.2f} P&L=${r.total_pnl:.2f}")

    print(f"\n🏆 Top 3 by Win Rate (min 20 trades):")
    filtered.sort(key=lambda r: r.win_rate, reverse=True)
    for rank, r in enumerate(filtered[:3], 1):
        print(f"   {rank}. Stop={r.stop_mult:.1f} Target={r.target_mult:.1f} "
              f"ATR={r.atr_period} MinRR={r.min_rr:.1f} → "
              f"Win={r.win_rate:.1f}% PF={r.profit_factor:.2f} P&L=${r.total_pnl:.2f}")

    best = results[0]
    print(f"\n🎯 Best Parameters (by P&L):")
    print(f"   stop_loss_multiplier = {best.stop_mult}")
    print(f"   take_profit_multiplier = {best.target_mult}")
    print(f"   atr_period = {best.atr_period}")
    print(f"   min_risk_reward = {best.min_rr}")


if __name__ == "__main__":
    main()
