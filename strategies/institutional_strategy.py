"""
Institutional Probability Strategy — dual-score engine wrapper.

Uses the InstitutionalProbabilityEngine which returns separate bullish
and bearish scores (0-100 each). The engine emits LONG only when the
bullish score clears LONG_MIN_SCORE (70) and SHORT only when the bearish
score clears SHORT_MIN_SCORE (46); these thresholds live in
engines/institutional_probability_engine.py and are shared with the
walk-forward backtester's acceptance gate.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from engines.institutional_probability_engine import InstitutionalProbabilityEngine
from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("inst_strategy")


class InstitutionalStrategy(ExecutableStrategy):
    def __init__(self, sl_mult: float = 0.5, tp_mult: float = 5.0, atr_period: int = 14,
                 short_sl_mult: float = 1.0, short_tp_mult: float = 2.0):
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult
        self.short_sl_mult = short_sl_mult
        self.short_tp_mult = short_tp_mult
        self.atr_period = atr_period
        self._engine = InstitutionalProbabilityEngine(
            sl_mult=sl_mult, tp_mult=tp_mult, atr_period=atr_period,
        )

    @property
    def name(self) -> str:
        return "Institutional Probability"

    def _compute_sltp(self, df: pd.DataFrame, entry: float,
                      is_short: bool = False) -> tuple[float, float]:
        rr_info = None
        rr_value = None
        try:
            result = self._engine.compute(df, day_type="", stock_type="")
            rr_info = result["factors"].get("risk_reward", {}).get("detail", {})
            if is_short:
                rr_value = rr_info.get("rr_short", 0)
            else:
                rr_value = rr_info.get("rr_long", 0)
        except Exception:
            pass

        if rr_info and rr_value is not None and rr_value >= 1.0:
            if is_short:
                sl = rr_info.get("sl_short")
                tp = rr_info.get("tp_short")
            else:
                sl = rr_info.get("sl_long")
                tp = rr_info.get("tp_long")
            if sl is not None and tp is not None and sl > 0 and tp > 0:
                return round(sl, 2), round(tp, 2)

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        tr = np.maximum(
            high[1:] - low[1:],
            np.maximum(np.abs(high[1:] - close[:-1]), np.abs(low[1:] - close[:-1])),
        )
        atr_val = float(pd.Series(tr).rolling(self.atr_period).mean().iloc[-1])
        if atr_val <= 0:
            atr_val = entry * 0.01

        if is_short:
            return round(entry + atr_val * self.short_sl_mult, 2), round(entry - atr_val * self.short_tp_mult, 2)
        return round(entry - atr_val * self.sl_mult, 2), round(entry + atr_val * self.tp_mult, 2)

    def run(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
        day_type: str = "",
        stock_type: str = "",
        **kwargs,
    ) -> StrategyResult:
        if df is None or len(df) < 60:
            return StrategyResult()

        nifty_df = kwargs.get("nifty_df", None)
        stock_daily = kwargs.get("stock_daily", None)
        sector_name = kwargs.get("sector_name", None)
        htf_ctx = kwargs.get("htf_ctx", None)
        nifty_daily = kwargs.get("nifty_daily", None)

        # Entry time for session-timing factor
        entry_time = None
        if "timestamp" in df.columns and len(df) > 0:
            entry_time = str(df["timestamp"].iloc[-1])

        result = self._engine.compute(
            df=df,
            nifty_df=nifty_df,
            stock_daily=stock_daily,
            day_type=day_type,
            stock_type=stock_type,
            sector_name=sector_name,
            htf_ctx=htf_ctx,
            entry_time=entry_time,
            nifty_daily=nifty_daily,
        )

        direction = result["direction"]

        if direction == "NONE":
            return StrategyResult(
                metadata={
                    "bullish_score": result["bullish_score"],
                    "bearish_score": result["bearish_score"],
                    "direction": direction,
                    "reasons": result["reasons"],
                    "factors": result.get("detailed_breakdown", {}),
                }
            )

        is_short = direction == "SHORT"
        entry = float(df["close"].iloc[-1])
        sl, tp = self._compute_sltp(df, entry, is_short=is_short)

        ranking_score = result["bullish_score"] if not is_short else result["bearish_score"]

        tc = TradeCandidate(
            direction=direction,
            entry_price=entry,
            stop_loss=sl,
            take_profit=tp,
            is_executable=True,
            ranking_score=ranking_score,
            rationale=f"Inst. Probability (bull={result['bullish_score']} bear={result['bearish_score']}) — {result['reasons']}",
            symbol=symbol,
            timeframe=timeframe,
        )

        return StrategyResult(
            trade_candidates=[tc],
            metadata={
                "bullish_score": result["bullish_score"],
                "bearish_score": result["bearish_score"],
                "direction": direction,
                "reasons": result["reasons"],
                "factors": result.get("detailed_breakdown", {}),
            },
        )
