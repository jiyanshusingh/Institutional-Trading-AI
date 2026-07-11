"""
Trend Following Strategy — Donchian channel breakout stub.

Entry: close above 20-period Donchian high (long) /
       close below 20-period Donchian low (short).
Exit: ATR-based stop loss and take profit.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("trend_follow")


class TrendFollowingStrategy(ExecutableStrategy):
    def __init__(self, entry_channel: int = 20, sl_mult: float = 3.0,
                 tp_mult: float = 4.0, **kwargs):
        self.entry_channel = entry_channel
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult

    @property
    def name(self) -> str:
        return "Trend Following"

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
        if df is None or len(df) < self.entry_channel + 5:
            return StrategyResult()

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values

        last = len(df) - 1
        recent_high = float(np.max(high[-self.entry_channel - 1:-1]))
        recent_low = float(np.min(low[-self.entry_channel - 1:-1]))

        tcs: list[TradeCandidate] = []
        atr = self._estimate_atr(df)
        if atr is None or atr <= 0:
            atr = float(close[last]) * 0.01

        entry = float(close[last])

        if entry > recent_high and self._can_long(day_type):
            tcs.append(TradeCandidate(
                direction="LONG",
                entry_price=entry,
                stop_loss=round(entry - atr * self.sl_mult, 2),
                take_profit=round(entry + atr * self.tp_mult, 2),
                ranking_score=85,
                rationale=f"Donchian breakout above {self.entry_channel}-period high ({recent_high:.1f})",
                symbol=symbol, timeframe=timeframe,
            ))

        if entry < recent_low and self._can_short(day_type):
            tcs.append(TradeCandidate(
                direction="SHORT",
                entry_price=entry,
                stop_loss=round(entry + atr * self.sl_mult, 2),
                take_profit=round(entry - atr * self.tp_mult, 2),
                ranking_score=85,
                rationale=f"Donchian breakdown below {self.entry_channel}-period low ({recent_low:.1f})",
                symbol=symbol, timeframe=timeframe,
            ))

        return StrategyResult(trade_candidates=tcs)
