"""
Bulk historical data downloader (yfinance, tokenless) — Phase 0.4.

Extends the local Parquet cache to the maximum history yfinance allows per
interval, for every symbol in the watched list. This gives the backtester a
long enough window that 1d/longer-warmup timeframes stop producing 0 trades and
walk-forward / out-of-sample validation becomes trustworthy.

yfinance interval limits (approx):
    1h  -> 730 days
    15m -> 60 days
    1d  -> years (we request 5y)

Existing cache rows are merged (dedup on timestamp), never lost.

Usage
-----
    .venv/bin/python scripts/download_history.py                 # all TFs, all symbols
    .venv/bin/python scripts/download_history.py --tf 1h 1d      # specific TFs
    .venv/bin/python scripts/download_history.py --symbols RELIANCE TCS
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from data.downloader.watched_symbols import SYMBOLS, YF_SUFFIX

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
_log = logging.getLogger("download_history")

_CACHE_DIR = Path("data/cache")

# interval -> (yfinance period, cache sub-dir)
_TF_CONFIG = {
    "15m": ("60d", "15m"),
    "1h": ("730d", "1h"),
    "1d": ("5y", "1d"),
}

_COLS = ["timestamp", "open", "high", "low", "close", "volume"]


def _fetch_yf(symbol: str, period: str, interval: str) -> pd.DataFrame | None:
    import yfinance as yf

    try:
        raw = yf.Ticker(f"{symbol}{YF_SUFFIX}").history(period=period, interval=interval)
    except Exception as e:
        _log.warning("  %s %s: fetch error %s", symbol, interval, e)
        return None
    if raw is None or raw.empty:
        return None

    df = raw.reset_index()
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    df = df.rename(columns={"datetime": "timestamp", "date": "timestamp"})
    for drop_col in ("dividends", "stock_splits", "capital_gains"):
        if drop_col in df.columns:
            df.drop(columns=[drop_col], inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)
    missing = [c for c in _COLS if c not in df.columns]
    if missing:
        _log.warning("  %s %s: missing cols %s", symbol, interval, missing)
        return None
    return df[_COLS]


def _merge_write(new_df: pd.DataFrame, symbol: str, tf_dir: str) -> int:
    path = _CACHE_DIR / tf_dir / f"{symbol}.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            old = pd.read_parquet(path)
            old["timestamp"] = pd.to_datetime(old["timestamp"]).dt.tz_localize(None)
            new_df = pd.concat([old[_COLS], new_df], ignore_index=True)
        except Exception as e:
            _log.debug("  %s: could not merge old cache (%s) — overwriting", symbol, e)
    merged = (
        new_df.dropna(subset=["open", "high", "low", "close"])
        .drop_duplicates(subset=["timestamp"])
        .sort_values("timestamp")
        .reset_index(drop=True)
    )
    merged["volume"] = pd.to_numeric(merged["volume"], errors="coerce").fillna(0).astype(int)
    merged.to_parquet(path, index=False)
    return len(merged)


def run(timeframes: list[str], symbols: list[str]) -> None:
    for tf in timeframes:
        if tf not in _TF_CONFIG:
            _log.warning("Unsupported timeframe %s (skip)", tf)
            continue
        period, tf_dir = _TF_CONFIG[tf]
        _log.info("=== %s (period=%s) ===", tf, period)
        for sym in symbols:
            df = _fetch_yf(sym, period, tf)
            if df is None or df.empty:
                _log.warning("  %s: no data", sym)
                continue
            total = _merge_write(df, sym, tf_dir)
            _log.info("  %s: +%d fetched -> %d total bars", sym, len(df), total)


def main() -> None:
    ap = argparse.ArgumentParser(description="Bulk yfinance history downloader")
    ap.add_argument("--tf", nargs="*", default=list(_TF_CONFIG.keys()),
                    help="Timeframes to download (default: 15m 1h 1d)")
    ap.add_argument("--symbols", nargs="*", default=None,
                    help="Restrict to specific symbols (default: full watchlist)")
    args = ap.parse_args()
    syms = args.symbols if args.symbols else SYMBOLS
    run(args.tf, syms)


if __name__ == "__main__":
    main()
