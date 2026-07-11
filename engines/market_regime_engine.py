"""
Market Regime Engine

Combines DayTypeEngine (NIFTY price action) + VIX + FII/DII flows
into a unified market regime assessment.

Output:
  {
    "regime": "BULLISH" / "BEARISH" / "CAUTIOUS" / "RISK_OFF",
    "day_type": { ... }  (from DayTypeEngine.classify()),
    "vix": { "value": float, "zone": str, "change_pct": float },
    "fii_dii": { "fii_net_cr": float, "dii_net_cr": float, ... },
    "breadth_pct": float,
    "strength": int,   # 0-2
    "timestamp": str,
  }
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import pandas as pd
import requests
import yfinance as yf

from engines.day_type_engine import DayTypeEngine

_log = logging.getLogger("market_regime")

_FII_DII_URL = "https://fii-diidata.mrchartist.com/api/data"


def _fetch_vix() -> dict:
    """Fetch latest India VIX close via yfinance. Return dict with value/zone/change."""
    try:
        df = yf.download("^INDIAVIX", period="5d", interval="1d", progress=False)
        if df is None or df.empty:
            return {"value": None, "zone": "UNKNOWN", "change_pct": None}
        if isinstance(df.columns, pd.MultiIndex):
            closes = df.xs("Close", axis=1, level=0)
        else:
            closes = df["Close"] if "Close" in df.columns else df.iloc[:, df.columns.get_loc("Close")]
        vals = closes.values.flatten()
        vals = vals[~pd.isna(vals)]
        if len(vals) < 1:
            return {"value": None, "zone": "UNKNOWN", "change_pct": None}
        val = float(vals[-1])
        prev = float(vals[-2]) if len(vals) >= 2 else val
        change_pct = ((val - prev) / prev * 100) if prev else 0.0
        if val < 15:
            zone = "LOW"
        elif val < 22:
            zone = "NORMAL"
        else:
            zone = "HIGH_FEAR"
        return {"value": round(val, 2), "zone": zone, "change_pct": round(change_pct, 2)}
    except Exception as exc:
        _log.warning("VIX fetch failed: %s", exc)
        return {"value": None, "zone": "UNKNOWN", "change_pct": None}


def _fetch_fii_dii() -> dict:
    """Fetch latest FII/DII cash and F&O data from Mr. Chartist API."""
    try:
        resp = requests.get(_FII_DII_URL, timeout=15)
        if resp.status_code != 200:
            _log.warning("FII/DII API error %s", resp.status_code)
            return {}
        data = resp.json()
        return {
            "date": data.get("date"),
            "fii_net_cr": data.get("fii_net"),
            "dii_net_cr": data.get("dii_net"),
            "combined_net_cr": (data.get("fii_net") or 0) + (data.get("dii_net") or 0),
            "fii_idx_fut_net": data.get("fii_idx_fut_net"),
            "pcr": data.get("pcr"),
            "sentiment_score": data.get("sentiment_score"),
        }
    except Exception as exc:
        _log.warning("FII/DII fetch failed: %s", exc)
        return {}


def _determine_regime(
    day_type: str,
    vix_zone: str,
    fii_net_cr: float | None,
    breadth_pct: float,
    day_strength: int,
) -> tuple[str, int]:
    """Combine signals into (regime, strength)."""
    # Risk-off override: high VIX
    if vix_zone == "HIGH_FEAR":
        return "RISK_OFF", 0

    is_bullish_day = day_type in ("TREND_UP", "GAP_UP")
    is_bearish_day = day_type in ("TREND_DOWN", "GAP_DOWN")

    # FII signal
    fii_bullish = fii_net_cr is not None and fii_net_cr > 0

    # Breadth confirmation
    breadth_ok = breadth_pct >= 50.0

    if is_bullish_day and fii_bullish and breadth_ok:
        return "BULLISH", min(day_strength + 1, 2)
    if is_bullish_day and (fii_bullish or breadth_ok):
        return "BULLISH", day_strength
    if is_bullish_day:
        return "CAUTIOUS", max(day_strength - 1, 0)
    if is_bearish_day and not fii_bullish:
        return "BEARISH", day_strength
    if is_bearish_day:
        return "CAUTIOUS", max(day_strength - 1, 0)

    # Default: neutral / cautious
    if vix_zone == "NORMAL" and breadth_ok:
        return "CAUTIOUS", 1
    return "CAUTIOUS", 0


def classify() -> dict:
    """Run full market regime classification.

    Returns a dict with regime, day_type, vix, fii_dii, breadth, strength.
    """
    # 1. Day Type (live via DayTypeEngine)
    day_result = DayTypeEngine.classify()
    day_type = day_result.get("type", "UNKNOWN")
    day_strength = day_result.get("strength", 0)
    breadth_pct = day_result.get("sector_breadth", {}).get("breadth_pct", 50.0)

    # 2. VIX
    vix_data = _fetch_vix()

    # 3. FII/DII
    fii_data = _fetch_fii_dii()

    # 4. Combined regime
    regime, strength = _determine_regime(
        day_type=day_type,
        vix_zone=vix_data.get("zone", "UNKNOWN"),
        fii_net_cr=fii_data.get("fii_net_cr"),
        breadth_pct=breadth_pct,
        day_strength=day_strength,
    )

    return {
        "regime": regime,
        "strength": strength,
        "day_type": day_result,
        "vix": vix_data,
        "fii_dii": fii_data,
        "breadth_pct": breadth_pct,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
