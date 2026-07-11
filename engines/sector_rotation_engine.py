"""
Sector Rotation Engine

Tracks sector performance, relative strength vs NIFTY, and volume flow
to classify sectors into tiers (Tier 1 / Tier 2 / Avoid).

Data sources:
  - Sector ETFs via yfinance (primary): sector-level price & volume
  - sector_map.json (secondary): stock→sector mapping for depth
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf

_log = logging.getLogger("sector_rotation")

# Core sector ETFs tracked for performance
SECTOR_ETFS: dict[str, str] = {
    "Financial Services": "^NSEBANK",
    "IT": "^CNXIT",
    "Pharma": "^CNXPHARMA",
    "Auto": "^CNXAUTO",
    "Midcap": "^NSMIDCP",
    "Energy": "^CNXENERGY",
    "FMCG": "^CNXFMCG",
    "Metals": "^CNXMETAL",
    "Media": "^CNXMEDIA",
    "Realty": "^CNXREALTY",
    "PSU Banks": "^CNXPSE",
}

_SECTOR_MAP_PATH = Path("data/sector_map.json")


def _load_sector_map() -> dict[str, dict]:
    """Load cached stock→sector mapping."""
    if not _SECTOR_MAP_PATH.exists():
        _log.warning("sector_map.json not found at %s", _SECTOR_MAP_PATH)
        return {}
    try:
        return json.loads(_SECTOR_MAP_PATH.read_text())
    except Exception as exc:
        _log.warning("Failed to load sector_map.json: %s", exc)
        return {}


def _build_reverse_map(
    sector_map: dict[str, dict],
) -> dict[str, list[str]]:
    """Build sector → [stock_symbols] from stock→sector mapping."""
    rev: dict[str, list[str]] = {}
    for sym, info in sector_map.items():
        sec = info.get("sector")
        if sec:
            rev.setdefault(sec, []).append(f"{sym}.NS")
    return rev


def _extract_closes(df: pd.DataFrame, ticker: str | None = None) -> list[float]:
    """Extract close prices as a flat list from a yfinance DataFrame."""
    try:
        if df is None or df.empty:
            return []
        if ticker and isinstance(df.columns, pd.MultiIndex):
            try:
                series = df.xs(ticker, axis=1, level=0)["Close"]
            except KeyError:
                series = df.xs(ticker, axis=1, level=0).iloc[:, 2]
        elif isinstance(df.columns, pd.MultiIndex):
            series = df.xs("Close", axis=1, level=0).iloc[:, 0]
        else:
            series = df["Close"] if "Close" in df.columns else df.iloc[:, 3]
        vals = series.values.flatten()
        vals = vals[~pd.isna(vals)]
        return [float(v) for v in vals]
    except Exception:
        return []


def _fetch_etf_performance() -> dict[str, dict]:
    """Fetch 5-day + 21-day returns for tracked sector ETFs."""
    tickers = list(SECTOR_ETFS.values())
    try:
        df_5 = yf.download(tickers, period="6d", interval="1d", progress=False, group_by="ticker")
        df_21 = yf.download(tickers, period="1mo", interval="1d", progress=False, group_by="ticker")
    except Exception as exc:
        _log.warning("ETF data fetch failed: %s", exc)
        return {}

    results: dict[str, dict] = {}
    for sector, ticker in SECTOR_ETFS.items():
        try:
            prices_5 = _extract_closes(df_5, ticker)
            prices_21 = _extract_closes(df_21, ticker)
            if len(prices_5) < 2:
                continue
            ret_1d = (prices_5[-1] / prices_5[-2] - 1) * 100
            ret_5d = (prices_5[-1] / prices_5[0] - 1) * 100 if len(prices_5) >= 2 else 0.0
            ret_21d = (prices_21[-1] / prices_21[0] - 1) * 100 if len(prices_21) >= 2 else 0.0
            results[sector] = {
                "ret_1d_pct": round(ret_1d, 2),
                "ret_5d_pct": round(ret_5d, 2),
                "ret_21d_pct": round(ret_21d, 2),
                "last_price": round(prices_5[-1], 2),
            }
        except Exception as exc:
            _log.debug("Failed processing sector %s: %s", sector, exc)
    return results


def _rank_sectors(
    etf_perf: dict[str, dict],
    nifty_5d_ret: float,
    nifty_21d_ret: float,
) -> dict[str, Any]:
    """Rank sectors into tiers based on relative strength."""
    scored = []
    for sector, data in etf_perf.items():
        rs_5d = data["ret_5d_pct"] - nifty_5d_ret
        rs_21d = data["ret_21d_pct"] - nifty_21d_ret
        momentum = rs_5d * 0.6 + rs_21d * 0.4
        scored.append({
            "name": sector,
            "ret_1d_pct": data["ret_1d_pct"],
            "ret_5d_pct": data["ret_5d_pct"],
            "ret_21d_pct": data["ret_21d_pct"],
            "rs_5d": round(rs_5d, 2),
            "rs_21d": round(rs_21d, 2),
            "momentum": round(momentum, 2),
        })

    scored.sort(key=lambda x: x["momentum"], reverse=True)

    tier_1 = []
    tier_2 = []
    avoid = []
    for item in scored:
        if item["momentum"] > 2.0:
            tier_1.append(item)
        elif item["momentum"] > -1.0:
            tier_2.append(item)
        else:
            avoid.append(item)

    return {
        "tier_1": tier_1,
        "tier_2": tier_2,
        "avoid": avoid,
        "nifty_5d_ret": round(nifty_5d_ret, 2),
        "nifty_21d_ret": round(nifty_21d_ret, 2),
    }


def _fetch_nifty_returns() -> tuple[float, float]:
    """Fetch NIFTY 5d and 21d returns."""
    try:
        df = yf.download("^NSEI", period="1mo", interval="1d", progress=False)
        if df is None or df.empty:
            return 0.0, 0.0
        if isinstance(df.columns, pd.MultiIndex):
            closes = df.xs("Close", axis=1, level=0)
        else:
            closes = df["Close"] if "Close" in df.columns else df.iloc[:, df.columns.get_loc("Close")]
        vals = closes.values.flatten()
        vals = vals[~pd.isna(vals)]
        if len(vals) < 2:
            return 0.0, 0.0
        ret_5d = (float(vals[-1]) / float(vals[-2]) - 1) * 100
        ret_21d = (float(vals[-1]) / float(vals[0]) - 1) * 100
        return round(ret_5d, 2), round(ret_21d, 2)
    except Exception as exc:
        _log.warning("NIFTY fetch failed: %s", exc)
        return 0.0, 0.0


def get_sector_rotation() -> dict[str, Any]:
    """Run full sector rotation analysis.

    Returns:
      {
        "tier_1": [...],  # Leading sectors
        "tier_2": [...],  # Neutral sectors
        "avoid":  [...],  # Underperforming sectors
        "nifty_5d_ret": float,
        "nifty_21d_ret": float,
      }
    """
    nifty_5d, nifty_21d = _fetch_nifty_returns()
    etf_perf = _fetch_etf_performance()
    if not etf_perf:
        _log.warning("No ETF performance data retrieved")
        return {"tier_1": [], "tier_2": [], "avoid": [], "nifty_5d_ret": nifty_5d, "nifty_21d_ret": nifty_21d}

    result = _rank_sectors(etf_perf, nifty_5d, nifty_21d)
    result["nifty_5d_ret"] = round(nifty_5d, 2)
    result["nifty_21d_ret"] = round(nifty_21d, 2)
    return result


def get_stock_sector(symbol: str) -> str | None:
    """Look up sector for a stock symbol from the cached mapping."""
    sm = _load_sector_map()
    base = symbol.replace(".NS", "")
    entry = sm.get(base)
    if entry:
        return entry.get("sector")
    return None


def get_sector_stocks(sector_name: str) -> list[str]:
    """Return all mapped stock symbols in a given sector."""
    sm = _load_sector_map()
    return [sym for sym, info in sm.items() if info.get("sector") == sector_name]
