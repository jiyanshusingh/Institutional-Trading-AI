#!/usr/bin/env python3
"""
Institutional Trading AI — Main Runner

Fetches live market data, runs the full analysis pipeline,
backtests the logic, and prints explainable trade results.

Usage:
    python run.py MARICO.NS --timeframe 1d --backtest
    python run.py RELIANCE.NS --timeframe 1h --capital 50000
"""

from __future__ import annotations

import sys
import argparse
from datetime import datetime
from pathlib import Path


def build_pipeline(available_capital: float = 100.0):
    """Build and return a configured TradingPipeline."""
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
        trade_constructor=ICTTradeConstructor(),
        execution_planner=ICTExecutionPlanner(),
        available_capital=available_capital,
    )


def fetch_and_build_market(
    symbol: str,
    timeframe: str,
    lookback: int = 500,
) -> tuple:
    """
    Fetch live data and build a CanonicalMarketModel.

    Returns (CanonicalMarketModel, ObservationHistory).
    """
    from data.live.live_market_data_provider import LiveMarketDataProvider
    from data.builders.observation_history_builder import (
        ObservationHistoryBuilder,
    )
    from domain.semantic_construction.semantic_construction_pipeline import (
        SemanticConstructionPipeline,
    )

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

    semantic = SemanticConstructionPipeline()
    market = semantic.build(obs_history)

    return market, obs_history


def print_reasoning(result) -> None:
    """Print the reasoning chain for each trade candidate."""
    print("\n" + "=" * 70)
    print("MARKET ANALYSIS & REASONING")
    print("=" * 70)

    for thesis in result.market_theses:
        print(f"\n📊 Thesis [{thesis.symbol} @ {thesis.timeframe}]")
        print(f"   Theory:     {thesis.theory} v{thesis.version}")
        print(f"   Claim:      {thesis.central_claim}")
        print(f"   Regime:     {thesis.market_regime}")
        if thesis.supporting_evidence:
            print(f"   Supporting:")
            for ev in thesis.supporting_evidence:
                print(f"     ✅ {ev}")
        if thesis.counter_evidence:
            print(f"   Counter:")
            for ev in thesis.counter_evidence:
                print(f"     ⚠️  {ev}")
        print(f"   Uncertainty: {thesis.uncertainty}")
        if thesis.expected_structural_evolution:
            print(f"   Expected:   {thesis.expected_structural_evolution}")
        if thesis.invalidation:
            print(f"   Invalidation: {thesis.invalidation}")

    for rank in result.opportunity_rankings:
        print(f"\n📈 Rank #{rank.rank_position} [{rank.symbol} @ {rank.timeframe}]")
        print(f"   Direction:  {rank.direction}")
        print(f"   Score:      {rank.ranking_score}/100")
        print(f"   Priority:   {rank.priority}")
        print(f"   Eligible:   {rank.portfolio_eligible}")

    pd = result.portfolio_decision
    if pd.selected_ranking_ids:
        print(f"\n💰 Portfolio Decision")
        print(f"   Method:     {pd.allocation_method}")
        print(f"   Allocated:  {pd.total_allocated:.1f}%")
        print(f"   Cash:       {pd.cash_reserve:.1f}%")
        for i, sym in enumerate(pd.symbols):
            print(
                f"   {i+1}. {sym} ({pd.directions[i]}) "
                f"→ {pd.capital_allocations[i]:.1f}%"
            )

    for tc in result.trade_candidates:
        print(f"\n🎯 Trade Candidate [{tc.symbol} @ {tc.timeframe}]")
        print(f"   Direction:  {tc.direction}")
        print(f"   Entry:      {tc.entry_price}")
        print(f"   Stop Loss:  {tc.stop_loss}")
        print(f"   Take Profit: {tc.take_profit}")
        print(f"   R:R Ratio:  {tc.risk_reward_ratio}")
        print(f"   Allocation: {tc.capital_allocation:.1f}%")
        print(f"   Order:      {tc.order_type}")
        if tc.rationale:
            print(f"   Rationale:  {tc.rationale}")

    for ep in result.execution_plans:
        print(f"\n⚡ Execution Plan")
        print(f"   Method:     {ep.execution_method}")
        print(f"   Order Type: {ep.order_type}")
        print(f"   Slippage:   {ep.maximum_slippage:.2f}%")


def print_backtest_summary(bt_result) -> None:
    """Print backtest results."""
    print("\n" + "=" * 70)
    print("BACKTEST RESULTS")
    print("=" * 70)
    print(f"   Symbol:        {bt_result.symbol}")
    print(f"   Total Trades:  {bt_result.total_trades}")
    print(f"   Win Rate:      {bt_result.win_rate:.1f}%")
    print(f"   Profit Factor: {bt_result.profit_factor:.2f}")
    print(f"   Avg Win:       ${bt_result.avg_win:.2f}")
    print(f"   Avg Loss:      ${bt_result.avg_loss:.2f}")
    print(f"   Total P&L:     ${bt_result.total_pnl:.2f}")
    print(f"   Max DD:        {bt_result.max_drawdown:.1f}%")
    print(f"   Avg R Multiple: {bt_result.avg_r_multiple:.2f}")

    if bt_result.trades:
        print(f"\n   Recent Trades:")
        for t in bt_result.trades[-5:]:
            print(
                f"     {t.direction:5s} | "
                f"Entry: {t.entry_price:8.2f} | "
                f"Result: {t.result or 'OPEN':4s} | "
                f"PnL: {t.pnl:8.2f}"
            )


def run_backtest(
    symbol: str,
    timeframe: str,
    lookback: int = 500,
) -> None:
    """
    Run a full backtest using the pipeline logic.
    """
    from data.live.live_market_data_provider import LiveMarketDataProvider
    from data.builders.observation_history_builder import (
        ObservationHistoryBuilder,
    )
    from domain.semantic_construction.semantic_construction_pipeline import (
        SemanticConstructionPipeline,
    )
    from backtesting.engine import BacktestingEngine

    print(f"\n🔄 Fetching {lookback} candles of {symbol} ({timeframe})...")
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

    pipeline = build_pipeline()

    def run_pipeline(obs_window):
        semantic = SemanticConstructionPipeline()
        market = semantic.build(obs_window)
        return pipeline.run(market)

    print(f"🔄 Running backtest over {len(obs_history)} candles...")
    engine = BacktestingEngine(pipeline_runner=run_pipeline)
    bt_result = engine.run(obs_history, symbol, timeframe)

    print_backtest_summary(bt_result)
    return bt_result


def main():
    parser = argparse.ArgumentParser(
        description="Institutional Trading AI — Live Analysis & Backtest"
    )
    parser.add_argument(
        "symbol",
        type=str,
        nargs="?",
        default=None,
        help="Ticker symbol (e.g. MARICO.NS, RELIANCE.NS, AAPL)",
    )
    parser.add_argument(
        "--timeframe",
        type=str,
        default="1d",
        help="Timeframe: 1m, 5m, 15m, 1h, 1d (default: 1d)",
    )
    parser.add_argument(
        "--backtest",
        action="store_true",
        help="Run backtest after analysis",
    )
    parser.add_argument(
        "--lookback",
        type=int,
        default=200,
        help="Number of candles to fetch (default: 200)",
    )
    parser.add_argument(
        "--capital",
        type=float,
        default=100.0,
        help="Available capital as percentage (default: 100.0)",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Start continuous intraday monitoring daemon",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run one daemon analysis cycle, print results, then exit",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print daemon state summary and exit",
    )

    args = parser.parse_args()

    # ── Daemon mode ──
    if args.daemon or args.dry_run or args.status:
        from scheduler import main as daemon_main
        import sys as _sys
        _sys.argv = [
            "scheduler.py",
            "--dry-run" if args.dry_run else "",
            "--status" if args.status else "",
        ]
        _sys.argv = [a for a in _sys.argv if a]
        daemon_main()
        return

    # ── Single symbol mode ──
    if args.symbol is None:
        parser.print_help()
        return

    print(f"\n🔍 Analyzing {args.symbol} @ {args.timeframe}")
    print(f"   Lookback: {args.lookback} candles")

    if args.backtest:
        run_backtest(
            symbol=args.symbol,
            timeframe=args.timeframe,
            lookback=args.lookback * 3,
        )

    print(f"\n🔄 Fetching live data for {args.symbol}...")
    try:
        market, obs_history = fetch_and_build_market(
            symbol=args.symbol,
            timeframe=args.timeframe,
            lookback=args.lookback,
        )
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        sys.exit(1)

    pipeline = build_pipeline(available_capital=args.capital)

    print(f"🔄 Running analysis pipeline...")
    try:
        result = pipeline.run(market)
    except Exception as e:
        import traceback
        print(f"❌ Pipeline error: {e}")
        traceback.print_exc()
        sys.exit(1)

    print_reasoning(result)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    summary = result.summary
    for key, value in summary.items():
        print(f"   {key}: {value}")
    print()

    return result


if __name__ == "__main__":
    main()