"""
Phase 6 (corrected) — Walk-forward / out-of-sample validation.

FIXES the earlier leakage:
  1. The engine no longer sees future data (scripts/backtest.py now slices
     nifty_daily / stock_daily / nifty_intraday to point-in-time).
  2. THIS harness now uses NON-OVERLAPPING windows: train on an EARLIER
     period, build the whitelist, then test on a STRICTLY LATER, disjoint
     period. (Previously test ⊂ train, so it was in-sample.)

Usage
-----
  Single train/test pair:
    .venv/bin/python -m scripts.walkforward_validate --timeframe 1h --no-intraday \
        --train-start 2023-07-01 --train-end 2025-01-01 \
        --test-start 2025-01-01 --test-end 2026-07-10 \
        --sl 1.5 --tp 4.0

  Rolling walk-forward (N out-of-sample folds):
    .venv/bin/python -m scripts.walkforward_validate --timeframe 1h --no-intraday \
        --train-start 2023-07-28 --test-end 2024-12-31 --folds 3 \
        --symbols WIPRO,RELIANCE,ONGC,BSE,ADANIENT --sl 1.5 --tp 4.0
"""

from __future__ import annotations

import argparse
import json
import sys as _sys

_sys.path.insert(0, ".")

from datetime import datetime

from data.downloader.watched_symbols import SYMBOLS
from config.symbol_whitelist import MIN_PF, MIN_TRADES, bucket_key
from scripts.backtest import WalkForwardBacktest, resolve_upstox_key


def _portfolio_stats(tf: str, intraday: bool, start: str, end: str,
                     sl: float, tp: float, symbols=None) -> list[dict]:
    from data.downloader.data_registry import get_bars
    if symbols is None:
        from data.downloader.watched_symbols import SYMBOLS as symbols
    tuning = {"sl_mult": sl, "tp_mult": tp, "atr_period": 14}
    rows = []
    for sym in symbols:
        key = resolve_upstox_key(f"{sym}.NS", "upstox")
        if key == f"{sym}.NS":
            continue
        # Load the FULL cached series and slice to [start, end] ourselves so
        # the backtester's point-in-time logic has the right window.
        try:
            df = get_bars(sym, tf, 4000, live=False)
            if df is None or df.empty:
                continue
            df["timestamp"] = pd_to_ts(df["timestamp"])
            mask = (df["timestamp"] >= pd_Timestamp(start)) & (df["timestamp"] < pd_Timestamp(end))
            df = df[mask].reset_index(drop=True)
            if len(df) < 200:
                continue
        except Exception:
            continue
        try:
            # Redirect the data-registry cache root to a scratch dir so the
            # sliced window is what the backtester reads, WITHOUT overwriting
            # the real data/cache (which was being destroyed on every run).
            from pathlib import Path
            from data.downloader import data_registry as _dr
            scratch = Path("data/cache_wf")
            scratch.mkdir(parents=True, exist_ok=True)
            tf_dir = _dr._INTERVAL_MAP.get(tf, tf)
            dest = scratch / tf_dir / f"{sym}.parquet"
            dest.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(dest, index=False)

            with _dr.override_cache_dir(scratch):
                bt = WalkForwardBacktest(
                    key, sym, tf, "upstox", intraday_mode=intraday,
                    force_strategy="Institutional Probability", tuning_override=tuning,
                )
                s = bt.run(days=len(df))  # sliced file bounds the window
        except Exception:
            continue
        if s.total_trades >= 1:
            rows.append({
                "symbol": sym, "timeframe": tf, "trades": s.total_trades,
                "wins": s.wins, "losses": s.losses,
                "win_rate": round(s.win_rate, 1),
                "avg_r": round(s.avg_r, 3),
                "profit_factor": round(s.profit_factor, 2),
                "total_pnl_pct": round(s.total_pnl_pct, 2),
            })
    return rows


def _build_whitelist_from(rows: list[dict]) -> list[str]:
    return [r["symbol"] for r in rows if r["profit_factor"] >= MIN_PF and r["trades"] >= MIN_TRADES]


def _fold_boundaries(start: str, end: str, n: int) -> list:
    """Chronological boundaries dividing [start, end] into n equal segments.
    Fold i (1..n) trains on [s0, s_i) and tests on [s_i, s_{i+1})."""
    s = pd_Timestamp(start)
    e = pd_Timestamp(end)
    return [s + (e - s) * i / n for i in range(n + 1)]


def _run_pair(tf, intraday, tr_s, tr_e, te_s, te_e, sl, tp, symbols, key):
    """Train on [tr_s,tr_e), build whitelist, report OOS on [te_s,te_e)."""
    train = _portfolio_stats(tf, intraday, tr_s, tr_e, sl, tp, symbols)
    wl = _build_whitelist_from(train)
    print(f"  train [{tr_s} -> {tr_e}): {len(train)} syms tested, "
          f"{len(wl)} passed whitelist ({', '.join(wl) or '-'})")
    test = _portfolio_stats(tf, intraday, te_s, te_e, sl, tp, symbols)
    test_wl = [r for r in test if r["symbol"] in wl]
    return wl, test_wl


def _report_oos(key: str, test_wl: list[dict]) -> None:
    tr = sum(r["trades"] for r in test_wl)
    if tr:
        wr = sum(r["wins"] for r in test_wl) / tr * 100
        exp = sum(r["avg_r"] * r["trades"] for r in test_wl) / tr
        pnl = sum(r["total_pnl_pct"] for r in test_wl)
        prof = sum(1 for r in test_wl if r["profit_factor"] >= MIN_PF)
        print(f"  [OUT-OF-SAMPLE] {key}: {len(test_wl)} whitelisted symbols, "
              f"{tr} trades")
        print(f"    WR={wr:.1f}%  expectancy={exp:+.3f}R  sumPnL%={pnl:+.1f}  "
              f"PF>=1.5 symbols={prof}/{len(test_wl)}")
        for r in test_wl:
            print(f"      {r['symbol']:10s} trades={r['trades']:4d}  "
                  f"WR={r['win_rate']:.1f}%  PF={r['profit_factor']:.2f}  "
                  f"exp={r['avg_r']:+.3f}R")
    else:
        print(f"  [OUT-OF-SAMPLE] {key}: no trades in test window for whitelist")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeframe", "-t", required=True)
    ap.add_argument("--no-intraday", action="store_true")
    ap.add_argument("--train-start", default=None)
    ap.add_argument("--train-end", default=None)
    ap.add_argument("--test-start", default=None)
    ap.add_argument("--test-end", default=None)
    ap.add_argument("--sl", type=float, required=True)
    ap.add_argument("--tp", type=float, required=True)
    ap.add_argument("--symbols", default=None,
                    help="Restrict to a subset (comma/space separated)")
    ap.add_argument("--folds", type=int, default=None,
                    help="Rolling walk-forward: N out-of-sample windows "
                         "(requires --train-start and --test-end)")
    args = ap.parse_args()
    intraday = not args.no_intraday
    key = bucket_key(args.timeframe, intraday)

    # imports for timestamp handling
    global pd_to_ts, pd_Timestamp
    import pandas as pd
    pd_to_ts = lambda s: pd.to_datetime(s)
    pd_Timestamp = pd.Timestamp

    # Resolve symbol subset (strip .NS, allow comma/space).
    if args.symbols:
        symbols = []
        for tok in args.symbols.replace(",", " ").split():
            tok = tok.strip()
            if tok.endswith(".NS"):
                tok = tok[:-3]
            if tok:
                symbols.append(tok)
    else:
        symbols = None

    if args.folds:
        if not (args.train_start and args.test_end):
            print("[ERROR] --folds requires --train-start and --test-end",
                  file=_sys.stderr)
            _sys.exit(2)
        # folds N out-of-sample windows require N+1 segments (N+2 boundaries).
        bnds = _fold_boundaries(args.train_start, args.test_end, args.folds + 1)
        print(f"[walk-forward] {args.timeframe} {args.train_start} -> "
              f"{args.test_end}  ({args.folds} OOS folds)")
        all_wl = []
        for i in range(1, args.folds + 1):
            tr_s, tr_e = bnds[0], bnds[i]
            te_s, te_e = bnds[i], bnds[i + 1]
            print(f"\n=== FOLD {i}: train [{tr_s.date()} -> {tr_e.date()}) "
                  f"| test [{te_s.date()} -> {te_e.date()}) ===")
            wl, test_wl = _run_pair(args.timeframe, intraday, tr_s, tr_e,
                                    te_s, te_e, args.sl, args.tp, symbols, key)
            _report_oos(key, test_wl)
            all_wl.extend(test_wl)
        print("\n[AGGREGATE OOS across all folds]")
        _report_oos(f"{key} (all folds)", all_wl)
        return

    # --- original single train/test behaviour ---
    if not (args.train_start and args.train_end and args.test_start
            and args.test_end):
        print("[ERROR] single-pair mode requires --train-start/end and "
              "--test-start/end (or use --folds)", file=_sys.stderr)
        _sys.exit(2)
    if pd_Timestamp(args.test_start) < pd_Timestamp(args.train_end):
        print(
            f"[ERROR] test window ({args.test_start}) starts before train "
            f"window ends ({args.train_end}). Windows overlap — OOS result "
            f"would be invalid. Use --test-start >= --train-end.",
            file=_sys.stderr,
        )
        _sys.exit(2)

    print(f"[train] {args.timeframe} {args.train_start} → {args.train_end}")
    train = _portfolio_stats(args.timeframe, intraday, args.train_start,
                             args.train_end, args.sl, args.tp, symbols)
    wl = _build_whitelist_from(train)
    print(f"[train] {len(wl)} symbols passed (PF>={MIN_PF}, trades>={MIN_TRADES})")

    print(f"[test]  {args.timeframe} {args.test_start} → {args.test_end} (disjoint)")
    test = _portfolio_stats(args.timeframe, intraday, args.test_start,
                            args.test_end, args.sl, args.tp, symbols)
    test_wl = [r for r in test if r["symbol"] in wl]
    _report_oos(key, test_wl)


if __name__ == "__main__":
    main()
