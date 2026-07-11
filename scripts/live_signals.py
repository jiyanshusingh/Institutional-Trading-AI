"""
Live trade recommendations — uses Upstox WebSocket + REST for today's data.
"""

from __future__ import annotations

import logging
import sys as _sys
import time

_sys.path.insert(0, ".")

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")

from data.downloader.watched_symbols import SYMBOLS

import numpy as np
import pandas as pd
from scripts.backtest import (
    fetch_data,
    _normalize_timestamp_tz,
    resolve_upstox_key,
)
from engines.stock_type_engine import StockTypeEngine
from strategies.selector import select, get_recommended_tuning


_log = logging.getLogger(__name__)


def _fetch_stock_data(sym_name: str) -> pd.DataFrame | None:
    """Fetch stock data — yfinance for today + REST historical behind the scenes."""
    return fetch_data(f"{sym_name}.NS", "15m", "yfinance", 5, live=True)


def _classify_day_type() -> str:
    """Classify today's day type via live_scanner, or fall back to TREND_UP."""
    try:
        from scripts.live_scanner import classify_today_day_type
        result = classify_today_day_type()
        dt = result.get("day_type", "TREND_UP")
        return dt if dt != "UNKNOWN" else "TREND_UP"
    except Exception:
        return "TREND_UP"


def main():
    today = pd.Timestamp.now(tz="Asia/Kolkata").date()
    day_type = _classify_day_type()

    print(f"\n{'=' * 70}")
    print(f"  LIVE TRADE RECS — {today} {pd.Timestamp.now(tz='Asia/Kolkata').strftime('%H:%M %Z')}")
    print(f"  Day Type: {day_type}")
    print(f"{'=' * 70}")

    nifty_intra = fetch_data("^NSEI", "15m", "yfinance", 5)
    if nifty_intra is None:
        print("No NIFTY data")
        return
    nifty_intra = _normalize_timestamp_tz(nifty_intra)
    today_nifty = nifty_intra[nifty_intra["timestamp"].dt.date == today]
    if today_nifty.empty:
        print("No NIFTY data for today")
        return
    nifty_change = ((today_nifty.iloc[-1]["close"] - today_nifty.iloc[0]["open"]) / today_nifty.iloc[0]["open"]) * 100
    print(f"  NIFTY: {today_nifty.iloc[-1]['close']:.0f} ({nifty_change:+.1f}% today, "
          f"{len(today_nifty)} bars)\n")

    try:
        screener = pd.read_csv("data/live_scan_results.csv")
    except FileNotFoundError:
        screener = pd.read_csv("data/nse_screener_results.csv")

    results = []
    for sym_name in SYMBOLS:
        stock_df = _fetch_stock_data(sym_name)
        if stock_df is None or stock_df.empty:
            continue
        stock_df = _normalize_timestamp_tz(stock_df)
        today_stock = stock_df[stock_df["timestamp"].dt.date == today]
        if today_stock.empty:
            continue

        current_price = float(today_stock.iloc[-1]["close"])
        open_price = float(today_stock.iloc[0]["open"])
        change_pct = ((current_price - open_price) / open_price) * 100

        # ATR(14) from yfinance data
        h = stock_df["high"].values
        l = stock_df["low"].values
        c = stock_df["close"].values
        tr = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
        tr = np.insert(tr, 0, h[0] - l[0])
        atr = float(pd.Series(tr).rolling(14).mean().iloc[-1])

        # Stock type from last 100 bars
        from scripts.backtest import WINDOW_SIZE
        window = stock_df.tail(WINDOW_SIZE).reset_index(drop=True)
        stock_up = window.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
        nifty_win = nifty_intra.tail(WINDOW_SIZE).reset_index(drop=True)
        if len(nifty_win) >= WINDOW_SIZE:
            nifty_up = nifty_win.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
            try:
                stk_res = StockTypeEngine.classify(stock_up, nifty_up)
                stock_type = stk_res.get("type", "UNKNOWN")
            except Exception as e:
                _log = logging.getLogger()
                _log.debug(f"StockType failed for {sym_name}: {e}")
                stock_type = "UNKNOWN"
        else:
            stock_type = "UNKNOWN"

        strat, rationale = select(day_type, stock_type)
        rec_strategy = strat.name if strat else "N/A"
        tuning = get_recommended_tuning(day_type, stock_type)
        sl_mult = tuning.get("sl_mult", 3.0)
        tp_mult = tuning.get("tp_mult", 4.0)

        sl = current_price - atr * sl_mult if current_price > 0 else 0
        tp = current_price + atr * tp_mult if current_price > 0 else 0

        row = screener[screener["symbol"] == sym_name]
        hist_trades = int(row.iloc[0]["trades"]) if not row.empty else 0
        hist_wr = float(row.iloc[0]["win_rate"]) if not row.empty else 0
        hist_pf = float(row.iloc[0]["profit_factor"]) if not row.empty else 0.0

        results.append({
            "name": sym_name,
            "price": current_price,
            "change_pct": change_pct,
            "stock_type": stock_type,
            "strategy": rec_strategy,
            "sl": sl,
            "tp": tp,
            "sl_pct": -atr * sl_mult / current_price * 100 if current_price > 0 else 0,
            "tp_pct": atr * tp_mult / current_price * 100 if current_price > 0 else 0,
            "atr": atr,
            "hist_trades": hist_trades,
            "hist_wr": hist_wr,
            "hist_pf": hist_pf,
        })
        time.sleep(0.1)

    # ── BUY candidates ──
    buy_candidates = [
        r for r in results
        if r["stock_type"] in ("RS_LEADER", "BREAKOUT", "FOLLOWER", "IN_LINE", "DEFENSIVE")
        and r["hist_trades"] >= 5 and r["hist_pf"] >= 1.3
    ]
    buy_candidates.sort(key=lambda x: -x["hist_pf"])

    avoid = [r for r in results if r["stock_type"] in ("WEAKNESS", "BREAKDOWN")]

    print(f"  🔵 BUY SETUPS ({len(buy_candidates)})")
    print(f"  {'─' * 70}")
    if buy_candidates:
        for r in buy_candidates[:10]:
            print(f"  {r['name']:18s} @ ₹{r['price']:>8.2f} {r['change_pct']:+5.1f}%  "
                  f"st={r['stock_type']:12s}  → {r['strategy']:30s}")
            print(f"  {' ' * 18}  "
                  f"SL ₹{r['sl']:>8.2f} ({r['sl_pct']:.1f}%)  "
                  f"TP ₹{r['tp']:>8.2f} ({r['tp_pct']:.1f}%)  "
                  f"ATR ₹{r['atr']:.2f}  "
                  f"(hist: {r['hist_trades']}t WR={r['hist_wr']:.0f}% PF={r['hist_pf']:.2f})")
            print()
    else:
        print("  None — check stock types or historical performance thresholds\n")

    print(f"  🔴 AVOID (WEAKNESS/BREAKDOWN in {day_type})")
    print(f"  {'─' * 70}")
    if avoid:
        for r in avoid:
            print(f"  {r['name']:18s} @ ₹{r['price']:>8.2f} {r['change_pct']:+5.1f}%  "
                  f"st={r['stock_type']:12s} (hist: {r['hist_trades']}t WR={r['hist_wr']:.0f}%)")
    else:
        print("  None")
    print()

    total = len(results)
    buy = len(buy_candidates)
    av = len(avoid)
    print(f"  {buy} BUY | {av} AVOID | {total - buy - av} neutral | {total} total")
    print(f"{'=' * 70}\n")

    # ── Save to JSON for dashboard ──────────────────────────
    scan_data = {
        "timestamp": pd.Timestamp.now(tz="Asia/Kolkata").strftime("%Y-%m-%d %H:%M %Z"),
        "day_type": day_type,
        "nifty": round(float(today_nifty.iloc[-1]["close"]), 2) if len(today_nifty) > 0 else None,
        "nifty_change_pct": round(nifty_change, 2),
        "bars_today": len(today_nifty),
        "buys": [
            {
                "name": r["name"],
                "price": round(r["price"], 2),
                "change_pct": round(r["change_pct"], 2),
                "stock_type": r["stock_type"],
                "strategy": r["strategy"],
                "sl": round(r["sl"], 2),
                "tp": round(r["tp"], 2),
                "atr": round(r["atr"], 2),
                "sl_pct": round(r["sl_pct"], 1),
                "tp_pct": round(r["tp_pct"], 1),
                "hist_trades": r["hist_trades"],
                "hist_wr": round(r["hist_wr"], 1),
                "hist_pf": round(r["hist_pf"], 2),
            }
            for r in buy_candidates
        ],
        "avoids": [
            {
                "name": r["name"],
                "price": round(r["price"], 2),
                "change_pct": round(r["change_pct"], 2),
                "stock_type": r["stock_type"],
                "hist_trades": r["hist_trades"],
                "hist_wr": round(r["hist_wr"], 1),
                "hist_pf": round(r["hist_pf"], 2),
            }
            for r in avoid
        ],
    }

    import os as _os, json as _json
    _os.makedirs("data", exist_ok=True)
    with open("data/live_scan.json", "w") as f:
        _json.dump(scan_data, f, indent=2)
    print(f"  Saved to data/live_scan.json")


if __name__ == "__main__":
    main()
