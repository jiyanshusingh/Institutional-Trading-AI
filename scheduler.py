#!/usr/bin/env python3
"""
Smart Tiered Intraday Monitoring Daemon

Scans configured symbols across 1m/15m/1h/1d timeframes
using the Smart Tier B approach:
  - 1m tick (60s): fetch price, check open trade stops/targets
  - 15m tick (900s): fetch 15m data, run full ICT pipeline, alert on new signals
  - 1h tick (3600s): fetch 1h data, run full ICT pipeline
  - 1d tick (86400s): fetch 1d data, run full ICT pipeline

Usage:
    python scheduler.py
    python scheduler.py --dry-run          # one full analysis cycle, don't loop
    python scheduler.py --interval 60      # override tick interval (seconds)
"""

from __future__ import annotations

import sys
import time
import argparse
import logging
from datetime import datetime, timezone

from config import daemon_config as cfg
from utils.state_manager import StateManager
from utils.telegram_notifier import (
    send_telegram,
    format_signal_alert,
    format_stop_hit_alert,
)

# ── Logger (set up once at module level without conflicting with utils.logger) ──
_log = logging.getLogger("monitor")


def _setup_logging():
    if _log.handlers:
        return
    _log.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    _log.addHandler(sh)
    from pathlib import Path
    Path("logs").mkdir(exist_ok=True)
    fh = logging.FileHandler("logs/monitor.log")
    fh.setFormatter(fmt)
    _log.addHandler(fh)

# ────────────────────────────────────────────────────────
# Lazy-loaded providers (imported on first use)
# ────────────────────────────────────────────────────────

_DATA_PROVIDERS: dict[str, object] = {}
_OBS_BUILDER = None
_SEMANTIC_PIPELINE = None
_TRADING_PIPELINE = None
_STATE = None


def _get_data_provider(provider_type: str = "yfinance"):
    if provider_type in _DATA_PROVIDERS:
        return _DATA_PROVIDERS[provider_type]

    if provider_type == "upstox":
        if not cfg.UPSTOX.get("access_token"):
            raise RuntimeError(
                "Upstox provider selected but UPSTOX_ACCESS_TOKEN not set "
                "in environment or daemon_config.py"
            )
        from data.upstox.upstox_market_data_provider import (
            UpstoxMarketDataProvider,
        )
        _DATA_PROVIDERS[provider_type] = UpstoxMarketDataProvider(
            access_token=cfg.UPSTOX["access_token"],
        )
    else:
        from data.live.live_market_data_provider import (
            LiveMarketDataProvider,
        )
        _DATA_PROVIDERS[provider_type] = LiveMarketDataProvider()

    return _DATA_PROVIDERS[provider_type]


def _get_obs_builder():
    global _OBS_BUILDER
    if _OBS_BUILDER is None:
        from data.builders.observation_history_builder import (
            ObservationHistoryBuilder,
        )
        _OBS_BUILDER = ObservationHistoryBuilder()
    return _OBS_BUILDER


def _get_semantic_pipeline():
    global _SEMANTIC_PIPELINE
    if _SEMANTIC_PIPELINE is None:
        from domain.semantic_construction.semantic_construction_pipeline import (
            SemanticConstructionPipeline,
        )
        _SEMANTIC_PIPELINE = SemanticConstructionPipeline()
    return _SEMANTIC_PIPELINE


def _get_trading_pipeline():
    global _TRADING_PIPELINE
    if _TRADING_PIPELINE is None:
        from application.pipeline.trading_pipeline import TradingPipeline
        from domain.reasoning.ict.ict_reasoning_model import ICTReasoningModel
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
        from domain.trade.ict_trade_constructor import ICTTradeConstructor
        from domain.execution.ict_execution_planner import ICTExecutionPlanner

        tc = cfg.TRADE_CONSTRUCTOR
        _TRADING_PIPELINE = TradingPipeline(
            reasoning_model=ICTReasoningModel(),
            opportunity_generator=ICTOpportunityGenerator(),
            opportunity_assessor=ICTOpportunityAssessor(),
            opportunity_ranker=ICTOpportunityRanker(),
            portfolio_allocator=ICTPortfolioAllocator(),
            trade_constructor=ICTTradeConstructor(
                stop_loss_multiplier=tc["stop_loss_multiplier"],
                take_profit_multiplier=tc["take_profit_multiplier"],
                atr_period=tc["atr_period"],
                min_risk_reward=tc["min_risk_reward"],
            ),
            execution_planner=ICTExecutionPlanner(),
        )
    return _TRADING_PIPELINE


def _get_state() -> StateManager:
    global _STATE
    if _STATE is None:
        _STATE = StateManager(cfg.STATE["db_path"])
    return _STATE


# ────────────────────────────────────────────────────────
# Core analysis
# ────────────────────────────────────────────────────────


def analyze_symbol(
    symbol: str,
    name: str,
    timeframe: str,
    lookback: int,
    provider_type: str = "yfinance",
) -> dict | None:
    """Run the full ICT pipeline for a symbol+timeframe.

    Returns trade signal dict or None if no actionable signal.
    """
    _log.info(f"Analyzing {symbol} @ {timeframe}")

    provider = _get_data_provider(provider_type)
    builder = _get_obs_builder()
    semantic = _get_semantic_pipeline()
    pipeline = _get_trading_pipeline()

    df = provider.load_latest_data(
        symbol=symbol,
        timeframe=timeframe,
        lookback=lookback,
    )
    if df is None or len(df) < 30:
        _log.warning(f"  {symbol} @ {timeframe}: insufficient data ({len(df) if df is not None else 0} rows)")
        return None

    obs_history = builder.build(
        df=df,
        symbol=symbol,
        timeframe=timeframe,
        source="LIVE",
    )
    market = semantic.build(obs_history)
    result = pipeline.run(market)

    return _extract_signal(result, symbol, name, timeframe)


def _extract_signal(
    result,
    symbol: str,
    name: str,
    timeframe: str,
) -> dict | None:
    """Extract trade signal from pipeline result."""
    trades = result.trade_candidates
    if not trades:
        _log.info(f"  {symbol} @ {timeframe}: no trade candidates")
        return {"symbol": symbol, "name": name, "timeframe": timeframe,
                "direction": "NONE", "entry": None, "stop": None,
                "target": None, "rr": None, "regime": "NONE"}

    tc = trades[0]
    regime = (
        result.market_theses[0].market_regime
        if result.market_theses else ""
    )

    signal = {
        "symbol": symbol,
        "name": name,
        "timeframe": timeframe,
        "direction": tc.direction,
        "entry": tc.entry_price,
        "stop": tc.stop_loss,
        "target": tc.take_profit,
        "rr": tc.risk_reward_ratio,
        "regime": regime,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _log.info(
        f"  Signal: {signal['direction']} entry={signal['entry']} "
        f"stop={signal['stop']} target={signal['target']} "
        f"R:R={signal['rr']}"
    )
    return signal


def signal_is_actionable(signal: dict | None) -> bool:
    if signal is None:
        return False
    return signal.get("direction") in ("LONG", "SHORT")


# ────────────────────────────────────────────────────────
# Stop / Target monitoring
# ────────────────────────────────────────────────────────


def check_open_trade_stops(
    symbol: str,
    name: str,
    state: StateManager,
    timeframe: str,
    provider_type: str = "yfinance",
) -> None:
    """Check if any open trade hit its stop or target on this symbol."""
    trade = state.get_open_trade(symbol, timeframe)
    if trade is None:
        return

    direction = trade.get("direction")
    stop = trade.get("stop")
    target = trade.get("target")
    entry = trade.get("entry")
    if direction is None or stop is None or target is None:
        return

    provider = _get_data_provider(provider_type)
    df = provider.load_latest_data(symbol, "1m", 5)
    if df is None or len(df) == 0:
        return

    cols = {c.lower(): c for c in df.columns}
    latest_close = float(df[cols["close"]].iloc[-1])
    latest_high = float(df[cols["high"]].iloc[-1])
    latest_low = float(df[cols["low"]].iloc[-1])

    hit = False
    exit_price = None
    pnl_pct = 0.0

    if direction == "LONG":
        if latest_low <= stop:
            hit = True
            exit_price = stop
            pnl_pct = ((stop - entry) / entry) * 100 if entry else 0.0
            result = "STOP HIT"
        elif latest_high >= target:
            hit = True
            exit_price = target
            pnl_pct = ((target - entry) / entry) * 100 if entry else 0.0
            result = "TARGET HIT"
    elif direction == "SHORT":
        if latest_high >= stop:
            hit = True
            exit_price = stop
            pnl_pct = ((entry - stop) / entry) * 100 if entry else 0.0
            result = "STOP HIT"
        elif latest_low <= target:
            hit = True
            exit_price = target
            pnl_pct = ((entry - target) / entry) * 100 if entry else 0.0
            result = "TARGET HIT"

    if hit:
        _log.info(
            f"  {symbol} @ {timeframe}: {result} "
            f"entry={entry:.2f} exit={exit_price:.2f} PnL={pnl_pct:+.2f}%"
        )
        state.close_trade(symbol, timeframe)

        if cfg.TELEGRAM["enabled"]:
            msg = format_stop_hit_alert(
                symbol, name, timeframe, entry, exit_price, pnl_pct,
            )
            send_telegram(
                msg,
                cfg.TELEGRAM["bot_token"],
                cfg.TELEGRAM["chat_id"],
            )


# ────────────────────────────────────────────────────────
# Scheduler loop
# ────────────────────────────────────────────────────────


class Scheduler:
    def __init__(self, tick_interval: int = 60):
        self.tick_interval = tick_interval
        self.tick_count = 0
        self.state = _get_state()
        self._last_update: dict[str, float] = {}

    def _should_update(self, symbol: str, tf_name: str, tf_cfg: dict) -> bool:
        if not tf_cfg.get("enabled", False):
            return False
        key = f"{symbol}_{tf_name}"
        last = self._last_update.get(key, -99999.0)
        elapsed = time.time() - last
        return elapsed >= tf_cfg.get("update_every", 99999)

    def _mark_updated(self, symbol: str, tf_name: str):
        key = f"{symbol}_{tf_name}"
        self._last_update[key] = time.time()

    def run(self, dry_run: bool = False):
        _log.info("=" * 60)
        _log.info("Scheduler started")
        _log.info(f"  Watchlist: {[s[1] for s in cfg.WATCHLIST]}")
        _log.info(f"  Timeframes: {[k for k, v in cfg.TIMEFRAMES.items() if v['enabled']]}")
        _log.info(f"  Tick interval: {self.tick_interval}s")
        _log.info(f"  Telegram: {'enabled' if cfg.TELEGRAM['enabled'] else 'disabled'}")
        _log.info("=" * 60)

        if dry_run:
            self._cycle()
            _log.info("Dry run complete.")
            return

        while True:
            try:
                self._tick()
            except KeyboardInterrupt:
                _log.info("Scheduler stopped by user.")
                break
            except Exception as e:
                _log.error(f"Tick error: {e}", exc_info=True)

            time.sleep(self.tick_interval)

    def _tick(self):
        self.tick_count += 1
        now = datetime.now(timezone.utc)
        _log.debug(f"Tick #{self.tick_count} @ {now.isoformat()}")

        for symbol, name, provider_type in cfg.WATCHLIST:
            self._process_symbol(symbol, name, provider_type)

    def _cycle(self):
        """Run one full analysis cycle for all symbols."""
        for symbol, name, provider_type in cfg.WATCHLIST:
            self._process_symbol(symbol, name, provider_type)

    def _process_symbol(self, symbol: str, name: str, provider_type: str = "yfinance"):
        for tf_name, tf_cfg in cfg.TIMEFRAMES.items():
            if not tf_cfg.get("enabled", False):
                continue

            # ── Full pipeline run ──
            if tf_cfg.get("run_pipeline", False) and self._should_update(symbol, tf_name, tf_cfg):
                self._mark_updated(symbol, tf_name)
                _log.info(f"[{name}] Running analysis @ {tf_name}")

                signal = analyze_symbol(
                    symbol, name, tf_name, tf_cfg.get("lookback", 200), provider_type,
                )

                # Compare with last known signal
                if signal is not None:
                    is_new = self.state.update_signal(
                        symbol, tf_name, signal,
                    )
                    if is_new:
                        _log.info(f"  [{name}] NEW signal on {tf_name}: {signal['direction']}")
                        if signal_is_actionable(signal):
                            self.state.open_trade(symbol, tf_name, signal)

                        # Telegram alert
                        if cfg.TELEGRAM["enabled"]:
                            msg = format_signal_alert(
                                symbol=symbol,
                                name=name,
                                timeframe=tf_name,
                                direction=signal["direction"],
                                entry=signal["entry"],
                                stop=signal["stop"],
                                target=signal["target"],
                                rr=signal["rr"],
                                regime=signal.get("regime", ""),
                            )
                            send_telegram(
                                msg,
                                cfg.TELEGRAM["bot_token"],
                                cfg.TELEGRAM["chat_id"],
                            )
                    else:
                        _log.debug(f"  [{name}] Signal unchanged on {tf_name}")

            # ── Stop/target monitoring ──
            if tf_cfg.get("monitor_stops", False):
                check_open_trade_stops(symbol, name, self.state, tf_name, provider_type)

            # Also check stops on higher timeframes with open trades
            if tf_name == "1m":
                for higher_tf in ["15m", "1h", "1d"]:
                    if cfg.TIMEFRAMES.get(higher_tf, {}).get("enabled", False):
                        check_open_trade_stops(symbol, name, self.state, higher_tf, provider_type)


# ────────────────────────────────────────────────────────
# Entry point
# ────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Smart Tiered Intraday Monitoring Daemon",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run one full analysis cycle, print results, then exit",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Tick interval in seconds (default: 60)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print state summary and exit",
    )
    args = parser.parse_args()

    _setup_logging()

    if args.status:
        state = StateManager(cfg.STATE["db_path"])
        print(state.summary())
        return

    scheduler = Scheduler(tick_interval=args.interval)
    scheduler.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
