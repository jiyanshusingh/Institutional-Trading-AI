"""
Trade performance report — shows win/loss distribution per
(day_type, stock_type) combo from the portfolio backtest.

This is an analysis-only tool. True SL/TP optimization requires bar-level
data (GridSearchCV on WalkForwardBacktest) and is left for future work.

Usage:
    python scripts/run_backtest_portfolio.py
    python scripts/optimize_params.py
"""

from __future__ import annotations

import json as _json
import logging
import os as _os
import sys as _sys

_sys.path.insert(0, ".")

logging.basicConfig(level=logging.INFO, format="%(message)s")
_log = logging.getLogger("optimize")

import numpy as np

from strategies.selector import available_combinations, get_recommended_tuning

MIN_TRADES = 5


def _load_trades() -> list[dict]:
    for p in ("data/backtest_trades.json",):
        if _os.path.exists(p):
            with open(p) as f:
                data = _json.load(f)
            if isinstance(data, list):
                return data
    _log.error("No trade data — run run_backtest_portfolio.py first")
    return []


def _combo_stats(trades: list[dict]) -> dict:
    r_vals = [t.get("r_multiple", 0) for t in trades if t.get("r_multiple")]
    if not r_vals:
        return {"n": 0}
    n = len(r_vals)
    wins = sum(1 for r in r_vals if r > 0)
    losses = sum(1 for r in r_vals if r < 0)
    wr = (wins / n) if n > 0 else 0
    avg_r = float(np.mean(r_vals))
    std_r = float(np.std(r_vals)) if len(r_vals) > 1 else 0.001
    win_r = [r for r in r_vals if r > 0]
    loss_r = [r for r in r_vals if r < 0]
    return {
        "n": n,
        "wins": wins,
        "losses": losses,
        "win_rate": round(wr * 100, 1),
        "avg_r": round(avg_r, 3),
        "sharpe": round(avg_r / std_r, 3) if std_r > 0 else 0.0,
        "avg_win_r": round(float(np.mean(win_r)), 2) if win_r else 0,
        "avg_loss_r": round(float(np.mean(loss_r)), 2) if loss_r else -1.0,
        "max_win_r": round(max(win_r), 2) if win_r else 0,
        "max_loss_r": round(min(loss_r), 2) if loss_r else -1.0,
        "median_r": round(float(np.median(r_vals)), 3),
        "std_r": round(std_r, 3),
    }


def main():
    all_trades = _load_trades()
    if not all_trades:
        return

    groups: dict[str, list[dict]] = {}
    for t in all_trades:
        dt = t.get("day_type", "UNKNOWN")
        st = t.get("stock_type", "UNKNOWN")
        groups.setdefault(f"{dt}__{st}", []).append(t)

    combos = available_combinations()

    print("=" * 70)
    print("  TRADE ANALYSIS BY (DAY_TYPE, STOCK_TYPE) COMBO")
    print("=" * 70)
    print()
    print(f"  Total trades: {len(all_trades)}")
    print(f"  Combos with data: {len(groups)}/{len(combos)}")
    print()

    # Table
    header = (f"  {'Day Type':14s} {'Stock Type':12s} {'N':4s} "
              f"{'WR':6s} {'avgR':6s} {'medR':6s} "
              f"{'avgWinR':7s} {'avgLossR':8s} "
              f"{'Sharpe':7s} {'PF':6s}")
    print(header)
    print("  " + "─" * 82)

    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    total_n = 0
    for key, trades in sorted_groups:
        dt, st = key.split("__", 1)
        s = _combo_stats(trades)
        if s["n"] < MIN_TRADES:
            continue
        default = get_recommended_tuning(dt, st)

        # Compute profit factor from R multiples
        total_win_r = sum(r for r in [t.get("r_multiple", 0) for t in trades] if r > 0)
        total_loss_r = abs(sum(r for r in [t.get("r_multiple", 0) for t in trades] if r < 0))
        pf = round(total_win_r / total_loss_r, 2) if total_loss_r > 0 else 0

        print(f"  {dt:14s} {st:12s} {s['n']:4d} "
              f"{s['win_rate']:5.1f}% "
              f"{s['avg_r']:+5.2f} "
              f"{s['median_r']:+5.2f} "
              f"{s['avg_win_r']:+6.2f} "
              f"{s['avg_loss_r']:+6.2f} "
              f"{s['sharpe']:+6.3f} "
              f"{pf:5.2f}")
        total_n += s["n"]

    print("  " + "─" * 82)
    print(f"  {'Total':14s} {'':12s} {total_n:4d}")
    print()
    print("  Default tuning — SL/TP per combo (strategy defaults):")
    for dt, st in combos:
        t = get_recommended_tuning(dt, st)
        print(f"    {dt:14s} + {st:12s}: SL={t.get('sl_mult', 3.0)}  TP={t.get('tp_mult', 4.0)}  "
              f"entry={t.get('entry_channel', '?')}  exit={t.get('exit_channel', '?')}  "
              f"ATR={t.get('atr_mult', '?')}")

    print()
    print("  NOTE: This is an analysis report. True SL/TP optimization")
    print("  requires GridSearchCV on WalkForwardBacktest (full re-run per")
    print("  candidate). See scripts/grid_search_params.py for that approach.")
    print()


if __name__ == "__main__":
    main()
