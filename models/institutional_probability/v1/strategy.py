"""
Institutional Probability Strategy — timeframe-agnostic 8-factor scoring.

Uses the InstitutionalProbabilityEngine to score trade setups 0–100,
accepting only scores >= 80. Works on any timeframe (1m, 15m, 1h, 1d).
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from engines.institutional_probability_engine import InstitutionalProbabilityEngine
from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("inst_strategy")


class InstitutionalStrategy(ExecutableStrategy):
    def __init__(self, sl_mult: float = 3.0, tp_mult: float = 4.0, atr_period: int = 14):
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult
        self.atr_period = atr_period
        self._engine = InstitutionalProbabilityEngine(
            sl_mult=sl_mult, tp_mult=tp_mult, atr_period=atr_period,
        )

    @property
    def name(self) -> str:
        return "Institutional Probability"

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

        result = self._engine.compute(
            df=df,
            nifty_df=nifty_df,
            stock_daily=stock_daily,
            day_type=day_type,
            stock_type=stock_type,
            sector_name=sector_name,
            htf_ctx=htf_ctx,
        )

        total_score = result["total_score"]
        direction = result["direction"]

        if total_score < 70 or direction == "NONE":
            return StrategyResult(
                metadata={
                    "score": total_score,
                    "direction": direction,
                    "reasons": result["reasons"],
                    "factors": result.get("detailed_breakdown", {}),
                }
            )

        rr_info = result["factors"].get("risk_reward", {}).get("detail", {})
        sl = rr_info.get("sl")
        tp = rr_info.get("tp")

        entry = float(df["close"].iloc[-1])
        if sl is None or tp is None:
            close = df["close"]
            high = df["high"]
            low = df["low"]
            tr = np.maximum(
                high[1:] - low[1:],
                np.maximum(np.abs(high[1:] - close[:-1]), np.abs(low[1:] - close[:-1])),
            )
            atr_val = float(pd.Series(tr).rolling(self.atr_period).mean().iloc[-1])
            if atr_val <= 0:
                atr_val = entry * 0.01
            sl = round(entry - atr_val * self.sl_mult, 2)
            tp = round(entry + atr_val * self.tp_mult, 2)

        tc = TradeCandidate(
            direction="LONG",
            entry_price=entry,
            stop_loss=sl,
            take_profit=tp,
            is_executable=True,
            ranking_score=total_score,
            rationale=f"Inst. Probability {total_score}/100 — {result['reasons']}",
            symbol=symbol,
            timeframe=timeframe,
        )

        return StrategyResult(
            trade_candidates=[tc],
            metadata={
                "score": total_score,
                "direction": direction,
                "reasons": result["reasons"],
                "factors": result.get("detailed_breakdown", {}),
            },
        )
