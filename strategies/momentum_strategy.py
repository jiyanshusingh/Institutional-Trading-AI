"""
Momentum Strategy — breakout-based stub.

Entry: close above 20-period high (long) / close below 20-period low (short)
       with volume confirmation (>1.3x average).
Exit: ATR-based stop loss and take profit.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("momentum")


class MomentumStrategy(ExecutableStrategy):
    def __init__(self, lookback: int = 20, vol_mult: float = 1.3,
                 sl_mult: float = 2.0, tp_mult: float = 3.0, **kwargs):
        self.lookback = lookback
        self.vol_mult = vol_mult
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult

    @property
    def name(self) -> str:
        return "Momentum Trading"

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
        if df is None or len(df) < self.lookback + 5:
            return StrategyResult()

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        has_vol = "volume" in df.columns
        volume = df["volume"].values if has_vol else None

        last = len(df) - 1
        recent_high = float(np.max(high[-self.lookback - 1:-1]))
        recent_low = float(np.min(low[-self.lookback - 1:-1]))
        avg_vol = float(np.mean(volume[-self.lookback - 1:-1])) if has_vol else 0
        cur_vol = float(volume[last]) if has_vol else 0

        tcs: list[TradeCandidate] = []
        atr = self._estimate_atr(df)
        if atr is None or atr <= 0:
            atr = float(close[last]) * 0.01

        vol_ok = not has_vol or cur_vol > avg_vol * self.vol_mult
        entry = float(close[last])

        if entry > recent_high and vol_ok and self._can_long(day_type):
            tcs.append(TradeCandidate(
                direction="LONG",
                entry_price=entry,
                stop_loss=round(entry - atr * self.sl_mult, 2),
                take_profit=round(entry + atr * self.tp_mult, 2),
                ranking_score=85,
                rationale=f"Breakout above {self.lookback}-period high ({recent_high:.1f}) "
                          f"vol: {cur_vol:.0f} vs avg {avg_vol:.0f}",
                symbol=symbol, timeframe=timeframe,
            ))

        if entry < recent_low and vol_ok and self._can_short(day_type):
            tcs.append(TradeCandidate(
                direction="SHORT",
                entry_price=entry,
                stop_loss=round(entry + atr * self.sl_mult, 2),
                take_profit=round(entry - atr * self.tp_mult, 2),
                ranking_score=85,
                rationale=f"Breakdown below {self.lookback}-period low ({recent_low:.1f}) "
                          f"vol: {cur_vol:.0f} vs avg {avg_vol:.0f}",
                symbol=symbol, timeframe=timeframe,
            ))

        return StrategyResult(trade_candidates=tcs)
