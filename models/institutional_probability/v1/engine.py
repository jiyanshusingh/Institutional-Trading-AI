"""
Institutional Probability Engine — 8-factor scoring (0–100)

Factors:
  1. Market Regime   (15)   — NIFTY EMA alignment + HH/HL + breadth
  2. Sector Strength  (15)   — Relative performance + breadth + volume
  3. Price Action     (20)   — HH/HL structure + breakout + support quality
  4. Volume           (15)   — RVOL tiers
  5. Breakout Quality (15)   — A+ checklist
  6. Risk/Reward      (10)   — ATR-based RR scoring
  7. Indicators        (5)   — EMA + RSI + MACD + VWAP
  8. Catalyst          (5)   — Accumulation/distribution + news stub
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

_log = logging.getLogger("inst_prob_engine")


def _ema(series: pd.Series, period: int) -> float:
    return float(series.ewm(span=period, adjust=False).mean().iloc[-1])


def _rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])


def _atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
    h = high.values
    l = low.values
    c = close.values
    tr = np.maximum(
        h[1:] - l[1:],
        np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])),
    )
    return float(pd.Series(tr).rolling(period).mean().iloc[-1])


def _vwap(df: pd.DataFrame) -> float:
    tp = (df["high"] + df["low"] + df["close"]) / 3
    vol = df["volume"].replace(0, np.nan).fillna(1)
    return float((tp * vol).sum() / vol.sum())


def _detect_swing_hh_hl(df: pd.DataFrame, lookback: int = 5) -> dict:
    highs = df["high"].values
    lows = df["low"].values
    n = len(df)
    swing_highs = []
    swing_lows = []
    for i in range(lookback, n - lookback):
        if highs[i] == max(highs[i - lookback : i + lookback + 1]):
            swing_highs.append((i, highs[i]))
        if lows[i] == min(lows[i - lookback : i + lookback + 1]):
            swing_lows.append((i, lows[i]))

    last_sh_idx, last_sh_price = swing_highs[-1] if swing_highs else (0, 0)
    last_sl_idx, last_sl_price = swing_lows[-1] if swing_lows else (0, 0)
    prev_sh_price = swing_highs[-2][1] if len(swing_highs) >= 2 else 0
    prev_sl_price = swing_lows[-2][1] if len(swing_lows) >= 2 else 0

    hh = last_sh_price > prev_sh_price if prev_sh_price > 0 else True
    hl = last_sl_price > prev_sl_price if prev_sl_price > 0 else True

    return {
        "has_hh": hh,
        "has_hl": hl,
        "last_swing_high": last_sh_price,
        "last_swing_low": last_sl_price,
        "prev_swing_high": prev_sh_price,
        "prev_swing_low": prev_sl_price,
    }


def _nearest_resistance(highs: np.ndarray, price: float, lookback: int = 30) -> tuple[float | None, float]:
    recent = highs[-lookback:-1] if len(highs) > lookback else highs[:-1]
    above = recent[recent < price]
    if len(above) == 0:
        return None, 0.0
    nearest = float(np.max(above))
    pct = (price - nearest) / nearest * 100 if nearest > 0 else 0
    return nearest, pct


class InstitutionalProbabilityEngine:
    def __init__(self, sl_mult: float = 3.0, tp_mult: float = 4.0, atr_period: int = 14):
        self.sl_mult = sl_mult
        self.tp_mult = tp_mult
        self.atr_period = atr_period

    def compute(
        self,
        df: pd.DataFrame,
        nifty_df: pd.DataFrame | None = None,
        stock_daily: pd.DataFrame | None = None,
        day_type: str = "",
        stock_type: str = "",
        sector_name: str | None = None,
        htf_ctx: dict | None = None,
    ) -> dict:
        if df is None or len(df) < 60:
            return self._empty_result("Insufficient data")

        factors = {}
        reasons = []

        factors["market_regime"] = self._score_market_regime(nifty_df, day_type, htf_ctx)
        reasons.append(f"MarketRegime={factors['market_regime']['score']}")

        factors["sector_strength"] = self._score_sector_strength(
            df, stock_type, sector_name
        )
        reasons.append(f"Sector={factors['sector_strength']['score']}")

        factors["price_action"] = self._score_price_action(df, stock_daily)
        reasons.append(f"Price={factors['price_action']['score']}")

        factors["volume"] = self._score_volume(df)
        reasons.append(f"Volume={factors['volume']['score']}")

        factors["breakout_quality"] = self._score_breakout_quality(
            df, day_type, factors["market_regime"]["score"], htf_ctx
        )
        reasons.append(f"Breakout={factors['breakout_quality']['score']}")

        factors["risk_reward"] = self._score_risk_reward(df)
        reasons.append(f"RR={factors['risk_reward']['score']}")

        factors["indicators"] = self._score_indicators(df)
        reasons.append(f"Indicators={factors['indicators']['score']}")

        factors["catalyst"] = self._score_catalyst(df)
        reasons.append(f"Catalyst={factors['catalyst']['score']}")

        total = sum(f["score"] for f in factors.values())
        total = min(max(total, 0), 100)

        direction = "NONE"
        if total >= 80:
            direction = "LONG"
        elif total <= 20:
            direction = "SHORT"

        return {
            "total_score": total,
            "direction": direction,
            "factors": factors,
            "reasons": "; ".join(reasons),
            "detailed_breakdown": {
                name: {
                    "score": f["score"],
                    "max": f["max"],
                    **f.get("detail", {}),
                }
                for name, f in factors.items()
            },
        }

    # ── Factor 1: Market Regime (0–15) ──────────────────────

    def _score_market_regime(
        self, nifty_df: pd.DataFrame | None, day_type: str,
        htf_ctx: dict | None = None,
    ) -> dict:
        score = 0
        detail = {}

        if nifty_df is not None and len(nifty_df) >= 60:
            close = nifty_df["close"]
            ema20 = _ema(close, 20)
            ema50 = _ema(close, 50)
            ema200 = _ema(close, 200) if len(close) >= 200 else None
            last_close = float(close.iloc[-1])

            if last_close > ema20:
                score += 3
                detail["ema20"] = True
            else:
                detail["ema20"] = False

            if last_close > ema50:
                score += 3
                detail["ema50"] = True
            else:
                detail["ema50"] = False

            if ema200 is not None and last_close > ema200:
                score += 3
                detail["ema200"] = True
            elif ema200 is not None:
                detail["ema200"] = False

            swings = _detect_swing_hh_hl(nifty_df)
            if swings["has_hh"] and swings["has_hl"]:
                score += 3
                detail["hh_hl"] = 3
            elif swings["has_hh"] or swings["has_hl"]:
                score += 1
                detail["hh_hl"] = 1
            else:
                detail["hh_hl"] = 0
        else:
            detail["note"] = "No NIFTY data"

        trend_ok = day_type in ("TREND_UP", "GAP_UP", "REVERSAL")
        if trend_ok:
            score += 3
            detail["breadth_regime"] = True
        else:
            detail["breadth_regime"] = False

        # HTF bonus: 1d trend alignment
        htf_bonus = 0
        if htf_ctx:
            td = htf_ctx.get("1d_trend", "FLAT")
            if td == "UP":
                htf_bonus += 1
                detail["1d_trend_bonus"] = 1
            else:
                detail["1d_trend_bonus"] = 0
        score += htf_bonus

        return {"score": min(score, 15), "max": 15, "detail": detail}

    # ── Factor 2: Sector Strength (0–15) ────────────────────

    def _score_sector_strength(
        self, df: pd.DataFrame, stock_type: str, sector_name: str | None
    ) -> dict:
        score = 0
        detail = {}

        stock_strength_map = {
            "RS_LEADER": 5,
            "BREAKOUT": 5,
            "DEFENSIVE": 3,
            "FOLLOWER": 2,
            "IN_LINE": 1,
            "WEAKNESS": 0,
            "BREAKDOWN": 0,
        }
        rs = stock_strength_map.get(stock_type, 1)
        score += rs
        detail["relative_performance"] = rs

        avg_vol = float(df["volume"].tail(21).head(20).mean())
        last_vol = float(df["volume"].iloc[-1])
        rvol = last_vol / max(avg_vol, 1)
        if rvol > 2.0:
            vol_score = 8
        elif rvol > 1.5:
            vol_score = 6
        elif rvol > 1.0:
            vol_score = 4
        else:
            vol_score = 1
        score += vol_score
        detail["volume_ratio"] = vol_score

        return {"score": min(score, 15), "max": 15, "detail": detail}

    # ── Factor 3: Price Action (0–20) ───────────────────────

    def _score_price_action(
        self, df: pd.DataFrame, stock_daily: pd.DataFrame | None
    ) -> dict:
        score = 0
        detail = {}

        swings = _detect_swing_hh_hl(df)
        if swings["has_hh"] and swings["has_hl"]:
            score += 8
            detail["hh_hl_structure"] = 8
        elif swings["has_hh"] or swings["has_hl"]:
            score += 4
            detail["hh_hl_structure"] = 4
        else:
            detail["hh_hl_structure"] = 0

        close = df["close"].values
        last_close = float(close[-1])
        resist, break_pct = _nearest_resistance(df["high"].values, last_close)
        if resist is not None and break_pct > 0:
            if break_pct > 3.0:
                bos_score = 6
            elif break_pct > 1.5:
                bos_score = 4
            elif break_pct > 0.5:
                bos_score = 2
            else:
                bos_score = 1
            score += bos_score
            detail["breakout_structure"] = bos_score
            detail["breakout_pct"] = round(break_pct, 2)
        else:
            detail["breakout_structure"] = 0

        ema20 = _ema(pd.Series(close), 20)
        ema50 = _ema(pd.Series(close), 50)
        dist_20 = (last_close - ema20) / max(ema20, 1) * 100
        dist_50 = (last_close - ema50) / max(ema50, 1) * 100
        if dist_20 > 0 and dist_50 > 0:
            support_score = 6
        elif dist_20 > 0:
            support_score = 3
        else:
            support_score = 0
        score += support_score
        detail["support_quality"] = support_score

        return {"score": min(score, 20), "max": 20, "detail": detail}

    # ── Factor 4: Volume (0–15) ─────────────────────────────

    def _score_volume(self, df: pd.DataFrame) -> dict:
        if "volume" not in df.columns:
            return {"score": 0, "max": 15, "detail": {"rvol": 0}}

        avg_vol = float(df["volume"].tail(21).head(20).mean())
        last_vol = float(df["volume"].iloc[-1])
        rvol = last_vol / max(avg_vol, 1)

        if rvol >= 3.0:
            score = 15
        elif rvol >= 1.5:
            score = 10
        elif rvol >= 1.0:
            score = 5
        else:
            score = 0

        return {"score": score, "max": 15, "detail": {"rvol": round(rvol, 2)}}

    # ── Factor 5: Breakout Quality (0–15) ───────────────────

    def _score_breakout_quality(
        self, df: pd.DataFrame, day_type: str, regime_score: int,
        htf_ctx: dict | None = None,
    ) -> dict:
        score = 0
        detail = {}

        close = df["close"].values
        high = df["high"].values
        last_close = float(close[-1])

        resist, break_pct = _nearest_resistance(df["high"].values, last_close)
        if resist is not None and break_pct > 0.5:
            score += 3
            detail["breaks_resistance"] = True
        else:
            detail["breaks_resistance"] = False

        if resist is not None and float(close[-1]) > resist:
            score += 3
            detail["closes_above"] = True
        else:
            detail["closes_above"] = False

        avg_vol = float(df["volume"].tail(21).head(20).mean())
        last_vol = float(df["volume"].iloc[-1])
        rvol = last_vol / max(avg_vol, 1)
        if rvol > 1.5:
            score += 3
            detail["volume_confirmed"] = True
        else:
            detail["volume_confirmed"] = False

        low = df["low"].values
        recent_low = float(np.min(low[-10:-1])) if len(low) > 10 else float(np.min(low[:-1]))
        if resist is not None and recent_low > resist * 0.99:
            score += 3
            detail["retest_holds"] = True
        else:
            detail["retest_holds"] = False

        market_ok = day_type in ("TREND_UP", "GAP_UP") or regime_score >= 9
        if market_ok:
            score += 3
            detail["market_aligned"] = True
        else:
            detail["market_aligned"] = False

        # HTF bonus: 30m trend alignment for intraday
        htf_bonus = 0
        if htf_ctx:
            t30 = htf_ctx.get("30m_trend", "FLAT")
            if t30 == "UP":
                htf_bonus += 1
                detail["30m_trend_bonus"] = 1
            else:
                detail["30m_trend_bonus"] = 0
        score += htf_bonus

        return {"score": min(score, 15), "max": 15, "detail": detail}

    # ── Factor 6: Risk/Reward (0–10) ───────────────────────

    def _score_risk_reward(self, df: pd.DataFrame) -> dict:
        close = df["close"]
        high = df["high"]
        low = df["low"]
        entry = float(close.iloc[-1])
        atr_val = _atr(high, low, close, self.atr_period)
        if atr_val <= 0:
            atr_val = entry * 0.01

        stop = entry - atr_val * self.sl_mult
        target = entry + atr_val * self.tp_mult
        risk = entry - stop
        reward = target - entry
        rr = reward / max(risk, 0.01)

        if rr >= 3.0:
            score = 10
            tier = "institutional"
        elif rr >= 2.0:
            score = 7
            tier = "good"
        elif rr >= 1.5:
            score = 5
            tier = "acceptable"
        else:
            score = 0
            tier = "reject"

        return {
            "score": score,
            "max": 10,
            "detail": {
                "rr": round(rr, 2),
                "tier": tier,
                "sl": round(stop, 2),
                "tp": round(target, 2),
                "atr": round(atr_val, 2),
            },
        }

    # ── Factor 7: Indicators (0–5) ─────────────────────────

    def _score_indicators(self, df: pd.DataFrame) -> dict:
        score = 0
        detail = {}

        close = df["close"]
        last_close = float(close.iloc[-1])

        ema20 = _ema(close, 20)
        ema50 = _ema(close, 50)
        ema200 = _ema(close, 200) if len(close) >= 200 else None
        if ema20 > ema50 and (ema200 is None or ema50 > ema200):
            score += 2
            detail["ema_aligned"] = True
        else:
            detail["ema_aligned"] = False

        rsi_val = _rsi(close)
        if 50 <= rsi_val <= 70:
            score += 1
            detail["rsi_zone"] = "healthy"
        elif rsi_val > 70:
            detail["rsi_zone"] = "overbought"
        else:
            detail["rsi_zone"] = "weak"

        macd_line = close.ewm(span=12, adjust=False).mean() - close.ewm(
            span=26, adjust=False
        ).mean()
        signal = macd_line.ewm(span=9, adjust=False).mean()
        if float(macd_line.iloc[-1]) > float(signal.iloc[-1]):
            score += 1
            detail["macd_bullish"] = True
        else:
            detail["macd_bullish"] = False

        if "volume" in df.columns:
            vwap_val = _vwap(df)
            if last_close > vwap_val:
                score += 1
                detail["above_vwap"] = True
            else:
                detail["above_vwap"] = False
        else:
            detail["above_vwap"] = None

        return {"score": min(score, 5), "max": 5, "detail": detail}

    # ── Factor 8: Catalyst / Smart Money (0–5) ─────────────

    def _score_catalyst(self, df: pd.DataFrame) -> dict:
        score = 0
        detail = {}

        close = df["close"].values
        high = df["high"].values
        low = df["low"].values
        volume = df["volume"].values if "volume" in df.columns else None

        price_up = float(close[-1]) > float(close[-5]) if len(close) >= 5 else False
        detail["price_rising"] = price_up

        if volume is not None:
            vol_trend = float(np.mean(volume[-5:])) > float(np.mean(volume[-10:-5])) * 1.1
            detail["volume_rising"] = vol_trend
        else:
            vol_trend = False
            detail["volume_rising"] = False

        if price_up and vol_trend:
            score += 3
            detail["accumulation"] = True
        elif price_up or vol_trend:
            score += 1
            detail["accumulation"] = "partial"

        dips_absorbed = float(np.min(low[-5:])) > float(np.min(low[-10:-5])) if len(low) >= 10 else False
        if dips_absorbed:
            score += 2
            detail["dips_absorbed"] = True
        else:
            detail["dips_absorbed"] = False

        news_score = 0
        score += news_score
        detail["news"] = news_score

        return {"score": min(score, 5), "max": 5, "detail": detail}

    # ── Helpers ─────────────────────────────────────────────

    @staticmethod
    def _empty_result(reason: str) -> dict:
        return {
            "total_score": 0,
            "direction": "NONE",
            "factors": {
                k: {"score": 0, "max": m, "detail": {}}
                for k, m in [
                    ("market_regime", 15),
                    ("sector_strength", 15),
                    ("price_action", 20),
                    ("volume", 15),
                    ("breakout_quality", 15),
                    ("risk_reward", 10),
                    ("indicators", 5),
                    ("catalyst", 5),
                ]
            },
            "reasons": reason,
            "detailed_breakdown": {},
        }
