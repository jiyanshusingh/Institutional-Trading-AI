"""
VWAP Pullback Strategy — enter when price pulls back to VWAP
in a trending market.

Direction is biased by day_type:
  - TREND_UP / GAP_UP   → LONG only
  - TREND_DOWN / GAP_DOWN → SHORT only
  - Other contexts       → skip

"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("vwap_pullback")


class VWAPPullbackStrategy(ExecutableStrategy):
    def __init__(self, sl_mult: float = 2.0, tp_mult: float = 3.0,
                 vwap_bounce_min: float = 0.3, **kwargs):
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult
        self.vwap_bounce_min = vwap_bounce_min

    @property
    def name(self) -> str:
        return "VWAP Pullback Strategy"

    @staticmethod
    def _estimate_atr(df: pd.DataFrame, period: int = 14) -> float | None:
        try:
            d = df.copy()
            d["tr"] = d[["high", "low", "close"]].max(axis=1) - d[["high", "low", "close"]].min(axis=1)
            return float(d["tr"].tail(period).mean())
        except Exception:
            return None

    @staticmethod
    def _compute_vwap(df: pd.DataFrame) -> pd.Series:
        tp = (df["high"] + df["low"] + df["close"]) / 3
        vol = df["volume"].replace(0, np.nan).fillna(1)
        cum_tpv = (tp * vol).cumsum()
        cum_vol = vol.cumsum()
        return cum_tpv / cum_vol

    def run(self, df: pd.DataFrame, symbol: str, timeframe: str,
            day_type: str = "", stock_type: str = "", **kwargs) -> StrategyResult:
        if df is None or len(df) < 25:
            return StrategyResult()

        can_long = day_type in ("TREND_UP", "GAP_UP")
        can_short = day_type in ("TREND_DOWN", "GAP_DOWN")
        if not can_long and not can_short:
            return StrategyResult()

        close = df["close"].values
        last = len(df) - 1

        vwap = self._compute_vwap(df)
        vwap_val = float(vwap.iloc[-1])

        vwap_slope = 0.0
        if len(vwap) >= 5:
            vwap_slope = float(vwap.iloc[-1] - vwap.iloc[-5])

        price_dist = abs(float(close[last]) - vwap_val) / vwap_val * 100
        if price_dist > self.vwap_bounce_min * 2:
            return StrategyResult()

        atr = self._estimate_atr(df)
        if atr is None or atr <= 0:
            atr = float(close[last]) * 0.01

        tcs: list[TradeCandidate] = []
        entry = float(close[last])

        if can_long and vwap_slope > 0:
            tcs.append(TradeCandidate(
                direction="LONG",
                entry_price=entry,
                stop_loss=round(entry - atr * self.sl_mult, 2),
                take_profit=round(entry + atr * self.tp_mult, 2),
                ranking_score=75,
                rationale=f"VWAP pullback at {price_dist:.2f}% dist, rising VWAP ({vwap_val:.1f}) "
                          f"[{day_type}]",
                symbol=symbol, timeframe=timeframe,
            ))

        if can_short and vwap_slope < 0:
            tcs.append(TradeCandidate(
                direction="SHORT",
                entry_price=entry,
                stop_loss=round(entry + atr * self.sl_mult, 2),
                take_profit=round(entry - atr * self.tp_mult, 2),
                ranking_score=75,
                rationale=f"VWAP pullback at {price_dist:.2f}% dist, falling VWAP ({vwap_val:.1f}) "
                          f"[{day_type}]",
                symbol=symbol, timeframe=timeframe,
            ))

        return StrategyResult(trade_candidates=tcs)
