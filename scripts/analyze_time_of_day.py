"""
Phase 2 — Time-of-day analysis from REAL backtested trades.

The legacy data/time_of_day_analysis.json was computed over ALL raw signals
(not the gated/whitelisted trade population). This recomputes per-session and
per-hour stats from the whitelisted, regime-gated trade set so the session
filter is calibrated on the live signal path.

Usage
-----
    .venv/bin/python -m scripts.analyze_time_of_day data/backtest_trades_15m_wl.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


# Must match SESSION_STARTS/ENDS in config/trading_config.py
_SESSION_RANGES = [
    ("opening", (9, 15), (9, 45)),
    ("morning", (9, 45), (11, 30)),
    ("midday", (11, 30), (13, 30)),
    ("afternoon", (13, 30), (15, 0)),
    ("closing", (15, 0), (15, 30)),
]


def _session_of(ts: str) -> str:
    try:
        from datetime import datetime as _dt
        dt = _dt.fromisoformat(ts.replace("Z", "+00:00"))
        h = dt.hour + dt.minute / 60.0
        for name, (sh, sm), (eh, em) in _SESSION_RANGES:
            s = sh + sm / 60.0
            e = eh + em / 60.0
            if s <= h < e:
                return name
        return "unknown"
    except Exception:
        return "unknown"


def analyze(trades_path: str) -> dict:
    trades = json.loads(Path(trades_path).read_text())
    by_session = defaultdict(lambda: {"count": 0, "wins": 0, "pnl": 0.0})
    by_hour = defaultdict(lambda: {"count": 0, "wins": 0, "pnl": 0.0})

    for t in trades:
        # only resolved trades with an R multiple
        r = t.get("r_multiple")
        if r is None:
            continue
        win = r > 0
        pnl = t.get("pnl_pct", 0.0) or 0.0
        sess = _session_of(t["entry_timestamp"])
        by_session[sess]["count"] += 1
        by_session[sess]["wins"] += 1 if win else 0
        by_session[sess]["pnl"] += pnl
        hr = int(t["entry_timestamp"][11:13])
        by_hour[hr]["count"] += 1
        by_hour[hr]["wins"] += 1 if win else 0
        by_hour[hr]["pnl"] += pnl

    def _summ(d):
        out = []
        for k, v in sorted(d.items()):
            c = v["count"]
            if c == 0:
                continue
            out.append({
                "bucket": k, "count": c, "wins": v["wins"],
                "win_rate_pct": round(v["wins"] / c * 100, 1),
                "total_pnl_pct": round(v["pnl"], 2),
            })
        return out

    sessions = _summ(by_session)
    hours = _summ(by_hour)
    best_session = max((s for s in sessions if s["bucket"] != "unknown"),
                       key=lambda s: s["total_pnl_pct"], default=None)
    worst_session = min((s for s in sessions if s["bucket"] != "unknown"),
                        key=lambda s: s["total_pnl_pct"], default=None)
    return {
        "source": trades_path,
        "sessions": sessions,
        "hours": hours,
        "best_session": best_session["bucket"] if best_session else None,
        "worst_session": worst_session["bucket"] if worst_session else None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("trades", help="backtest_trades_*.json path")
    args = ap.parse_args()
    res = analyze(args.trades)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
