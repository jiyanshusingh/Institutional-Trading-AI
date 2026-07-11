"""
Opening Range Breakout (ORB) — define first N bars of the day
as the opening range, then trade breakout.

Uses _date column (from backtest) or date column for day boundary detection.
Also checks _day_bar_idx if available.

Direction biased by day_type:
  - TREND_UP / GAP_UP   → LONG only
  - TREND_DOWN / GAP_DOWN → SHORT only
  - Other               → both
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from strategies.executable import ExecutableStrategy, StrategyResult, TradeCandidate

_log = logging.getLogger("orb")


class ORBStrategy(ExecutableStrategy):
    def __init__(self, orb_bars: int = 5, sl_mult: float = 1.5,
                 tp_mult: float = 2.0, min_vol_ratio: float = 1.5,
                 **kwargs):
        self.orb_bars = orb_bars
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult
        self.min_vol_ratio = min_vol_ratio

    @property
    def name(self) -> str:
        return "Opening Range Breakout (ORB)"

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
        if df is None or len(df) < self.orb_bars + 10:
            return StrategyResult()

        last = len(df) - 1
        close = df["close"].values
        volume = df["volume"].values if "volume" in df.columns else None

        # Detect opening range using _day_bar_idx (added by backtest) if available
        if "_day_bar_idx" in df.columns:
            bar_idx = df["_day_bar_idx"].values
            current_bar_idx = bar_idx[-1]
            if current_bar_idx < self.orb_bars:
                return StrategyResult()

            # Find start of current day (where _day_bar_idx resets to 0)
            day_starts = np.where(bar_idx == 0)[0]
            if len(day_starts) == 0:
                return StrategyResult()
            current_day_start = day_starts[-1]
            pos = np.arange(len(bar_idx))
            orb_mask = (pos >= current_day_start) & (bar_idx < self.orb_bars)
            if not orb_mask.any():
                return StrategyResult()

            orb_high = float(np.max(df["high"].values[orb_mask]))
            orb_low = float(np.min(df["low"].values[orb_mask]))
        else:
            # Fallback: use date column
            date_col = "_date" if "_date" in df.columns else ("date" if "date" in df.columns else None)
            if date_col is None and df.index.name != "date":
                return StrategyResult()

            if date_col is not None:
                ts = df[date_col]
            else:
                ts = df.index

            try:
                dates = pd.to_datetime(ts)
            except Exception:
                return StrategyResult()

            dates_series = pd.Series(dates)
            unique_dates = dates_series.dt.date.unique()
            if len(unique_dates) < 1:
                return StrategyResult()

            latest_date = unique_dates[-1]
            today_mask = dates_series.dt.date == latest_date
            today_indices = np.where(today_mask.values)[0]

            if len(today_indices) <= self.orb_bars:
                return StrategyResult()

            current_idx = today_indices[-1]
            if current_idx != last:
                return StrategyResult()

            orb_indices = today_indices[:self.orb_bars]
            orb_high = float(np.max(df["high"].iloc[orb_indices]))
            orb_low = float(np.min(df["low"].iloc[orb_indices]))

        atr = self._estimate_atr(df)
        if atr is None or atr <= 0:
            atr = float(close[last]) * 0.01

        avg_vol = float(np.mean(volume[:last])) if volume is not None else 0
        cur_vol = float(volume[last]) if volume is not None else 0
        vol_ok = volume is None or cur_vol > avg_vol * self.min_vol_ratio

        tcs: list[TradeCandidate] = []
        entry = float(close[last])

        if entry > orb_high and vol_ok and self._can_long(day_type):
            tcs.append(TradeCandidate(
                direction="LONG",
                entry_price=entry,
                stop_loss=round(entry - atr * self.sl_mult, 2),
                take_profit=round(entry + atr * self.tp_mult, 2),
                ranking_score=80,
                rationale=f"ORB breakout above {orb_high:.1f} (OR: {orb_low:.1f}-{orb_high:.1f})",
                symbol=symbol, timeframe=timeframe,
            ))

        if entry < orb_low and vol_ok and self._can_short(day_type):
            tcs.append(TradeCandidate(
                direction="SHORT",
                entry_price=entry,
                stop_loss=round(entry + atr * self.sl_mult, 2),
                take_profit=round(entry - atr * self.tp_mult, 2),
                ranking_score=80,
                rationale=f"ORB breakdown below {orb_low:.1f} (OR: {orb_low:.1f}-{orb_high:.1f})",
                symbol=symbol, timeframe=timeframe,
            ))

        return StrategyResult(trade_candidates=tcs)
