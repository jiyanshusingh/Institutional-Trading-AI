"""
Mean Reversion Trading — RSI + Bollinger Band mean reversion.

Direction is biased by (day_type, stock_type) context:
  - TREND_UP + WEAKNESS        → LONG only  (weak stock catching up)
  - TREND_DOWN + RS_LEADER     → SHORT only (strong stock catching down)
  - RANGE + IN_LINE/WEAKNESS   → LONG only  (bounce from lower boundary)
  - GAP_DOWN + RS_LEADER       → LONG only  (oversold bounce)
  - CHOPPY + RS_LEADER         → LONG only
  - RANGE + RS_LEADER          → SHORT only
  - Other contexts              → skip (no clear reversion edge)
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("mean_reversion")

_CONTEXT_DIRECTION: dict[tuple[str, str], str] = {
    ("TREND_UP", "WEAKNESS"): "LONG",      # weak in strong market → catch-up
    ("TREND_DOWN", "RS_LEADER"): "SHORT",  # strong in weak market → catch-down
}


class MeanReversionStrategy(ExecutableStrategy):
    def __init__(self, rsi_oversold: int = 25, rsi_overbought: int = 75,
                 bb_mult: float = 2.0, sl_mult: float = 2.0,
                 tp_mult: float = 3.0, **kwargs):
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.bb_mult = bb_mult
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult

    @property
    def name(self) -> str:
        return "Mean Reversion Trading"

    @staticmethod
    def _estimate_atr(df: pd.DataFrame, period: int = 14) -> float | None:
        try:
            d = df.copy()
            d["tr"] = d[["high", "low", "close"]].max(axis=1) - d[["high", "low", "close"]].min(axis=1)
            return float(d["tr"].tail(period).mean())
        except Exception:
            return None

    @staticmethod
    def _compute_rsi(series: pd.Series, period: int = 14) -> float | None:
        try:
            delta = series.diff()
            gain = delta.where(delta > 0, 0.0).rolling(period).mean()
            loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))
            return float(rsi.iloc[-1])
        except Exception:
            return None

    @staticmethod
    def _compute_bb(df: pd.DataFrame, period: int = 20, mult: float = 2.0):
        try:
            sma = df["close"].rolling(period).mean()
            std = df["close"].rolling(period).std()
            upper = sma + mult * std
            lower = sma - mult * std
            return float(upper.iloc[-1]), float(lower.iloc[-1])
        except Exception:
            return None, None

    def run(self, df: pd.DataFrame, symbol: str, timeframe: str,
            day_type: str = "", stock_type: str = "", **kwargs) -> StrategyResult:
        if df is None or len(df) < 25:
            return StrategyResult()

        allowed = _CONTEXT_DIRECTION.get((day_type, stock_type), "")
        if not allowed:
            return StrategyResult()

        close = df["close"].values
        last = len(df) - 1

        rsi = self._compute_rsi(df["close"])
        if rsi is None:
            return StrategyResult()

        upper_bb, lower_bb = self._compute_bb(df, mult=self.bb_mult)
        if upper_bb is None:
            return StrategyResult()

        atr = self._estimate_atr(df)
        if atr is None or atr <= 0:
            atr = float(close[last]) * 0.01

        tcs: list[TradeCandidate] = []
        entry = float(close[last])

        if allowed == "LONG" and rsi < self.rsi_oversold and entry <= lower_bb * 1.01:
            tcs.append(TradeCandidate(
                direction="LONG",
                entry_price=entry,
                stop_loss=round(entry - atr * self.sl_mult, 2),
                take_profit=round(entry + atr * self.tp_mult, 2),
                ranking_score=70,
                rationale=f"RSI {rsi:.0f} < {self.rsi_oversold}, close near lower BB ({lower_bb:.1f}) "
                          f"[{day_type}+{stock_type}]",
                symbol=symbol, timeframe=timeframe,
            ))

        if allowed == "SHORT" and rsi > self.rsi_overbought and entry >= upper_bb * 0.99:
            tcs.append(TradeCandidate(
                direction="SHORT",
                entry_price=entry,
                stop_loss=round(entry + atr * self.sl_mult, 2),
                take_profit=round(entry - atr * self.tp_mult, 2),
                ranking_score=70,
                rationale=f"RSI {rsi:.0f} > {self.rsi_overbought}, close near upper BB ({upper_bb:.1f}) "
                          f"[{day_type}+{stock_type}]",
                symbol=symbol, timeframe=timeframe,
            ))

        return StrategyResult(trade_candidates=tcs)
