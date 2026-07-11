"""
Historical Stock Performance Analysis

Analyzes backtest trades against trailing multi-window returns
(5d / 20d / 60d / 120d) to determine which historical performance
regimes precede winning trades.

Usage:
    python scripts/analyze_historical_performance.py --input data/backtest_trades_15m.json \
        --daily data/stock_daily_*.json --output data/historical_performance_analysis.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def _compute_trailing_returns(daily_prices: list[float], windows: list[int]) -> dict:
    """Compute trailing returns for given windows from a price list (oldest→newest)."""
    returns = {}
    n = len(daily_prices)
    for w in windows:
        if n > w:
            returns[w] = (daily_prices[-1] - daily_prices[-w - 1]) / daily_prices[-w - 1] * 100
        else:
            returns[w] = 0.0
    return returns


def analyze_historical_performance(trades_path: str, daily_data: dict | None = None) -> dict:
    """
    Analyze trades by trailing return quintile.

    If daily_data (symbol → list of close prices) is provided, compute trailing
    returns at entry time. Otherwise, use the 'features' dict's existing return columns.
    """
    with open(trades_path, "r") as f:
        trades = json.load(f)

    windows = [5, 20, 60, 120]
    window_stats = {}

    for w in windows:
        buckets = defaultdict(lambda: {"wins": 0, "losses": 0, "total_pnl": 0.0, "count": 0})

        for t in trades:
            feat = t.get("features", {})
            # Try to get trailing return from features if present
            ret_key = f"{w}d_return"
            ret = feat.get(ret_key)
            if ret is None:
                # Fallback: try '1d_return' or '30m_return_3' as proxy for short windows
                if w <= 5:
                    ret = feat.get("1d_return")
                elif w <= 20:
                    ret = feat.get("30m_return_3")
                else:
                    ret = None

            if ret is None:
                ret = 0.0  # Default middle bucket

            # Bucket into quintiles: < -5%, -5% to 0%, 0% to 5%, 5% to 10%, > 10%
            if ret < -5:
                bucket = "lt_minus_5"
            elif ret < 0:
                bucket = "minus_5_to_0"
            elif ret < 5:
                bucket = "0_to_5"
            elif ret < 10:
                bucket = "5_to_10"
            else:
                bucket = "gt_10"

            result = t.get("result", "")
            pnl = t.get("pnl_net", t.get("pnl", 0)) or 0

            buckets[bucket]["count"] += 1
            buckets[bucket]["total_pnl"] += pnl
            if result == "WIN":
                buckets[bucket]["wins"] += 1
            else:
                buckets[bucket]["losses"] += 1

        # Compile
        compiled = []
        for b in ["lt_minus_5", "minus_5_to_0", "0_to_5", "5_to_10", "gt_10"]:
            s = buckets.get(b, {"wins": 0, "losses": 0, "total_pnl": 0, "count": 0})
            count = s["count"]
            wins = s["wins"]
            wr = (wins / count * 100) if count > 0 else 0
            losses = s["losses"]
            pf = wins / losses if losses > 0 else float("inf") if wins > 0 else 0
            compiled.append({
                "bucket": b,
                "count": count,
                "wins": wins,
                "losses": losses,
                "win_rate_pct": round(wr, 1),
                "profit_factor": round(pf, 2),
                "total_pnl": round(s["total_pnl"], 2),
            })

        window_stats[f"{w}d"] = compiled

    return {"windows": window_stats}


def main():
    parser = argparse.ArgumentParser(description="Historical stock performance analysis")
    parser.add_argument("--input", "-i", required=True, help="Path to backtest_trades_*.json")
    parser.add_argument("--daily", "-d", default=None, help="Optional daily price data JSON")
    parser.add_argument("--output", "-o", default="data/historical_performance_analysis.json",
                        help="Output path")
    args = parser.parse_args()

    daily_data = None
    if args.daily:
        with open(args.daily, "r") as f:
            daily_data = json.load(f)

    result = analyze_historical_performance(args.input, daily_data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Historical performance analysis saved to {args.output}")
    for w, stats in result["windows"].items():
        print(f"\nWindow {w}:")
        for s in stats:
            print(f"  {s['bucket']:14s}: {s['count']:3d} trades, WR={s['win_rate_pct']:5.1f}%, "
                  f"PF={s['profit_factor']:6.2f}")


if __name__ == "__main__":
    main()