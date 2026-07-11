"""
Price Action Trading — swing high/low breakout with tight stops.

Direction is biased by day_type:
  - TREND_UP / GAP_UP   → LONG only
  - TREND_DOWN / GAP_DOWN → SHORT only
  - RANGE / CHOPPY      → both
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("price_action")


class PriceActionStrategy(ExecutableStrategy):
    def __init__(self, sl_mult: float = 1.5, tp_mult: float = 2.5,
                 swing_lookback: int = 5, **kwargs):
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult
        self.swing_lookback = swing_lookback

    @property
    def name(self) -> str:
        return "Price Action Trading"

    @staticmethod
    def _estimate_atr(df: pd.DataFrame, period: int = 14) -> float | None:
        try:
            d = df.copy()
            d["tr"] = d[["high", "low", "close"]].max(axis=1) - d[["high", "low", "close"]].min(axis=1)
            return float(d["tr"].tail(period).mean())
        except Exception:
            return None

    @staticmethod
    def _can_long(day_type: str) -> bool:
        return day_type in ("", "TREND_UP", "GAP_UP", "REVERSAL", "RANGE", "CHOPPY")

    @staticmethod
    def _can_short(day_type: str) -> bool:
        return day_type in ("", "TREND_DOWN", "GAP_DOWN", "REVERSAL", "RANGE", "CHOPPY")

    def run(self, df: pd.DataFrame, symbol: str, timeframe: str,
            day_type: str = "", stock_type: str = "", **kwargs) -> StrategyResult:
        if df is None or len(df) < self.swing_lookback + 5:
            return StrategyResult()

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        last = len(df) - 1

        swing_high = float(np.max(high[-self.swing_lookback - 1:-1]))
        swing_low = float(np.min(low[-self.swing_lookback - 1:-1]))

        atr = self._estimate_atr(df)
        if atr is None or atr <= 0:
            atr = float(close[last]) * 0.01

        tcs: list[TradeCandidate] = []
        entry = float(close[last])

        if entry > swing_high and self._can_long(day_type):
            tcs.append(TradeCandidate(
                direction="LONG",
                entry_price=entry,
                stop_loss=round(entry - atr * self.sl_mult, 2),
                take_profit=round(entry + atr * self.tp_mult, 2),
                ranking_score=75,
                rationale=f"Breakout above swing high ({swing_high:.1f})",
                symbol=symbol, timeframe=timeframe,
            ))

        if entry < swing_low and self._can_short(day_type):
            tcs.append(TradeCandidate(
                direction="SHORT",
                entry_price=entry,
                stop_loss=round(entry + atr * self.sl_mult, 2),
                take_profit=round(entry - atr * self.tp_mult, 2),
                ranking_score=75,
                rationale=f"Breakdown below swing low ({swing_low:.1f})",
                symbol=symbol, timeframe=timeframe,
            ))

        return StrategyResult(trade_candidates=tcs)
