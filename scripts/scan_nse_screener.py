"""
NSE Equity Screener — runs full WalkForwardBacktest on each symbol.

Scans each stock using the real multi-strategy backtest engine with
15m intraday mode, reports performance metrics.

Usage:
    cd /Users/jiyanshusingh/Institutional-Trading-AI
    .venv/bin/python scripts/scan_nse_screener.py --short
    .venv/bin/python scripts/scan_nse_screener.py
"""

from __future__ import annotations

import json
import logging
import os
import sys as _sys
import time

import pandas as pd

_sys.path.insert(0, ".")

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
_log = logging.getLogger("screener")

LONG_SYMBOLS = sorted([
    "ASIANPAINT", "BSE", "OIL", "ACUTAAS", "POWERINDIA",
    "FORCEMOT", "ZEEL", "PHYSICSWALLAH", "ATHER",
])


def screen_symbol(name: str, instrument_key: str, days: int = 60) -> dict:
    from scripts.backtest import WalkForwardBacktest
    import logging as _logging
    _logging.getLogger("scripts.backtest").setLevel(logging.ERROR)

    try:
        bt = WalkForwardBacktest(
            instrument_key, name, "15m", "upstox",
            intraday_mode=True,
        )
        summary = bt.run(days=days)

        if summary.total_trades == 0:
            return {"symbol": name, "trades": 0, "reason": "no_trades"}

        total_r = round(summary.avg_r * summary.total_trades, 2)

        return {
            "symbol": name,
            "trades": summary.total_trades,
            "wins": summary.wins,
            "losses": summary.losses,
            "win_rate": round(summary.win_rate, 1),
            "profit_factor": round(summary.profit_factor, 2),
            "total_r": total_r,
            "avg_r": round(summary.avg_r, 2),
            "reason": "ok",
        }
    except Exception as e:
        return {"symbol": name, "trades": 0, "reason": f"error: {e}"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="NSE equity screener")
    parser.add_argument("--days", type=int, default=60,
                        help="Lookback days for backtest (default: 60)")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Delay between API calls in seconds (default: 0.5)")
    parser.add_argument("--output", default="data/nse_screener_results.csv",
                        help="Output CSV path")
    parser.add_argument("--short", action="store_true",
                        help="Run on short list only (for testing)")
    args = parser.parse_args()

    with open("data/sector_map.json") as f:
        all_syms = json.load(f)

    valid_syms = {
        k: v for k, v in all_syms.items()
        if v.get("sector") and v.get("sector") != ""
    }

    if args.short:
        scanned = sorted(LONG_SYMBOLS)
    else:
        scanned = sorted(valid_syms.keys())

    n_total = len(scanned)
    _log.info(f"Scanning {n_total} symbols ({'short' if args.short else 'full'} mode)")

    results: list[dict] = []
    start_time = time.time()

    for idx, sym_name in enumerate(scanned):
        try:
            from scripts.backtest import search_upstox_instrument
            key = search_upstox_instrument(sym_name)
            if key is None:
                _log.debug(f"[{idx + 1}/{n_total}] {sym_name}: no key")
                continue

            result = screen_symbol(sym_name, key, days=args.days)
            results.append(result)

            if result["trades"] > 0:
                _log.info(f"[{idx + 1}/{n_total}] {sym_name}: "
                          f"{result['trades']}t WR={result['win_rate']}% "
                          f"PF={result['profit_factor']}")
            else:
                _log.info(f"[{idx + 1}/{n_total}] {sym_name}: 0 trades "
                          f"({result.get('reason', 'n/a')})")

            time.sleep(args.delay)

        except KeyboardInterrupt:
            _log.warning("Interrupted — saving partial results")
            break
        except Exception as e:
            _log.warning(f"[{idx + 1}/{n_total}] {sym_name}: error: {e}")
            results.append({
                "symbol": sym_name, "trades": 0, "reason": f"error: {e}",
            })
            continue

    elapsed = time.time() - start_time
    csv_path = args.output
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)

    df_out = pd.DataFrame(results)
    df_out.to_csv(csv_path, index=False)
    _log.info(f"Saved {len(results)} results to {csv_path}")
    _log.info(f"Elapsed: {elapsed / 60:.1f} min")

    active = [r for r in results if r.get("trades", 0) >= 5]
    good = [r for r in active if r.get("win_rate", 0) >= 55 and r.get("profit_factor", 0) >= 1.3]
    maybe = [r for r in active if r not in good and r.get("win_rate", 0) >= 50 and r.get("profit_factor", 0) >= 1.1]

    print()
    print("=" * 65)
    print(f"SCREEN RESULTS ({len(results)} symbols)")
    print(f"  Active (>=5 trades):  {len(active)}")
    print(f"  GOOD (WR>=55% PF>=1.3):  {len(good)}")
    print(f"  MAYBE (WR>=50% PF>=1.1): {len(maybe)}")
    print(f"  No trades / data:       {len(results) - len(active)}")
    print()
    if good:
        print("  GOOD symbols:")
        for r in sorted(good, key=lambda x: -x["profit_factor"]):
            print(f"    {r['symbol']:30s}  n={r['trades']:3d}  "
                  f"WR={r['win_rate']:5.1f}%  PF={r['profit_factor']:5.2f}  "
                  f"avgR={r.get('avg_r', 0):+.2f}")
        print()
    if maybe:
        print("  Top MAYBE:")
        for r in sorted(maybe, key=lambda x: -x["profit_factor"])[:20]:
            print(f"    {r['symbol']:30s}  n={r['trades']:3d}  "
                  f"WR={r['win_rate']:5.1f}%  PF={r['profit_factor']:5.2f}  "
                  f"avgR={r.get('avg_r', 0):+.2f}")


if __name__ == "__main__":
    main()
