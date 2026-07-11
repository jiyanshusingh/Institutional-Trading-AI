"""
Live market scanner for the Institutional Probability strategy.

Scans the profitable watchlists in priority order and reports actionable trade
signals *without* managing a portfolio or placing orders (that is paper_trade.py's
job). The scan tiers mirror the validated edge:

  1. consensus     → scanned in BOTH 15m intraday AND 15m swing
  2. 15m_intraday  → 15m intraday  (unique symbols only)
  3. 15m_swing     → 15m swing     (unique symbols only)
  4. 1h_swing      → 1h swing      (unique symbols only)

Each symbol is scanned with the parameter set that matches its watchlist
specification. Signals are reported grouped as INTRADAY vs SWING.

Usage
-----
  .venv/bin/python scripts/market_scan.py                 # yfinance (delayed)
  .venv/bin/python scripts/market_scan.py --upstox        # live Upstox feed
  .venv/bin/python scripts/market_scan.py --list-tiers    # show tier plan
  .venv/bin/python scripts/market_scan.py --loop --interval 15
  .venv/bin/python scripts/market_scan.py --json          # machine-readable
"""

from __future__ import annotations

import argparse
import json
import os
import sys as _sys
import threading
import time

_sys.path.insert(0, ".")

import http.server
import pandas as pd

import scripts.paper_trade as _pt  # reuse Upstox/yfinance bar fetchers + resample
from scripts.backtest import WINDOW_SIZE, build_htf_context, decide_trade
from scripts.live_institutional_scan import (
    FORCE_STRATEGY,
    MIN_SCORE,
    TUNING,
    _bars_until_close,
    _classify_stock_type,
    _yf_live,
)
from scripts.live_scanner import classify_today_day_type

WATCHLIST_PATH = "data/symbol_watchlists.json"

# (tier_label, watchlist_key, category, spec)
#   category: "intraday" | "swing"  — drives the report grouping
#   spec: tf / sl / tp / intraday    — the scan parameters for this tier
SCAN_TIERS = [
    ("consensus", "consensus", "intraday",
     {"tf": "15m", "sl": 0.5, "tp": 5.0, "intraday": True}),
    ("consensus", "consensus", "swing",
     {"tf": "15m", "sl": 0.5, "tp": 5.0, "intraday": False}),
    ("15m_intraday", "15m_intraday", "intraday",
     {"tf": "15m", "sl": 0.5, "tp": 5.0, "intraday": True}),
    ("15m_swing", "15m_swing", "swing",
     {"tf": "15m", "sl": 0.5, "tp": 5.0, "intraday": False}),
    ("1h_swing", "1h_swing", "swing",
     {"tf": "1h", "sl": 1.5, "tp": 4.0, "intraday": False}),
]


def _load_watchlists() -> dict:
    if not os.path.exists(WATCHLIST_PATH):
        raise SystemExit(f"  [error] watchlist file not found: {WATCHLIST_PATH}")
    return json.load(open(WATCHLIST_PATH))


def _fetch(symbol: str, tf: str) -> pd.DataFrame | None:
    """Fetch OHLCV for ``symbol`` at ``tf`` using the configured data source."""
    if _pt.USE_UPSTOX:
        return _pt._upstox_live(symbol, tf)
    return _yf_live(f"{symbol}.NS", tf)


def _scan_symbol(sym: str, spec: dict, allow_shorts: bool) -> dict | None:
    """Scan one symbol with one spec. Returns a signal dict or None."""
    tf = spec["tf"]
    intraday = spec["intraday"]
    try:
        stock = _fetch(sym, tf)
        if stock is None or len(stock) < WINDOW_SIZE + 5:
            return None
        # NSEI index symbol for yfinance is "^NSEI" (NOT "^NSEI.NS")
        nifty = _pt._upstox_live("^NSEI", tf) if _pt.USE_UPSTOX else _yf_live("^NSEI", tf)
        stock_1d = _fetch(sym, "1d")
    except Exception:
        return None

    last_ts = stock["timestamp"].iloc[-1]
    today = last_ts.date() if hasattr(last_ts, "date") else last_ts
    current_price = float(stock["close"].iloc[-1])

    window = stock.tail(WINDOW_SIZE).reset_index(drop=True)
    nifty_win = nifty.tail(WINDOW_SIZE).reset_index(drop=True) if nifty is not None else None
    if nifty_win is None or len(nifty_win) < WINDOW_SIZE:
        nifty_win = window

    day_info = classify_today_day_type()
    day_type = day_info.get("day_type", "UNKNOWN")
    stock_type = _classify_stock_type(window, nifty_win, stock_1d, today)
    stock_30m = _pt._resample_safe(stock, 30)
    htf_ctx = build_htf_context(stock_30m, stock_1d, last_ts)
    intraday_remaining = _bars_until_close(last_ts) if intraday else None

    tuning = {"sl_mult": spec["sl"], "tp_mult": spec["tp"], "atr_period": 14}
    decision = decide_trade(
        window, f"{sym}.NS", tf,
        day_type, stock_type,
        nifty, stock_1d, stock_30m, last_ts,
        force_strategy=FORCE_STRATEGY,
        tuning_override=tuning,
        multi_tf_filter=True,
        intraday_mode=intraday,
        intraday_remaining_bars=intraday_remaining,
        htf_ctx=htf_ctx,
    )
    if decision is None:
        return None
    if decision.direction == "SHORT" and not allow_shorts:
        return None

    risk = abs(decision.entry_price - decision.stop_loss)
    reward = abs(decision.take_profit - decision.entry_price)
    r_mult = (reward / risk) if risk > 0 else 0.0
    return {
        "symbol": sym,
        "tier": None,            # filled by caller
        "category": "intraday" if intraday else "swing",
        "tf": tf,
        "direction": decision.direction,
        "score": round(decision.score, 1),
        "entry": round(decision.entry_price, 2),
        "stop_loss": round(decision.stop_loss, 2),
        "take_profit": round(decision.take_profit, 2),
        "r_multiple": round(r_mult, 2),
        "price": round(current_price, 2),
    }


def _run_scan(allow_shorts: bool) -> tuple[list[dict], int]:
    data = _load_watchlists()
    scanned: dict[tuple, set] = {}   # (tf, intraday) -> symbols already scanned
    signals: list[dict] = []
    total_scanned = 0

    for tier_label, wl_key, category, spec in SCAN_TIERS:
        if wl_key not in data:
            continue
        key = (spec["tf"], spec["intraday"])
        done = scanned.setdefault(key, set())
        for sym in data[wl_key]:
            if sym in done:
                continue
            done.add(sym)
            total_scanned += 1
            sig = _scan_symbol(sym, spec, allow_shorts)
            if sig is not None:
                sig["tier"] = tier_label
                signals.append(sig)

    # stable order: intraday first, then swing; by score desc within group
    signals.sort(key=lambda s: (0 if s["category"] == "intraday" else 1, -s["score"]))
    return signals, total_scanned


def _print_report(signals: list[dict], source: str, scanned_n: int) -> None:
    now = pd.Timestamp.now(tz="Asia/Kolkata").strftime("%Y-%m-%d %H:%M %Z")
    intraday = [s for s in signals if s["category"] == "intraday"]
    swing = [s for s in signals if s["category"] == "swing"]

    print("=" * 74)
    print(f"  MARKET SCAN — {now}   source: {source}   scans: {scanned_n}")
    print("=" * 74)

    def _table(rows: list[dict], header: str, with_tf: bool) -> None:
        print(f"\n── {header} ({len(rows)}) ──")
        if not rows:
            print("  (no signals)")
            return
        if with_tf:
            print(f"  {'SYMBOL':10s} {'SCORE':>5s} {'DIR':5s} {'ENTRY':>10s} "
                  f"{'SL':>10s} {'TP':>10s} {'R':>5s} {'TF':>4s}")
        else:
            print(f"  {'SYMBOL':10s} {'SCORE':>5s} {'DIR':5s} {'ENTRY':>10s} "
                  f"{'SL':>10s} {'TP':>10s} {'R':>5s}")
        for s in rows:
            line = (f"  {s['symbol']:10s} {s['score']:>5.0f} {s['direction']:5s} "
                    f"₹{s['entry']:>9.2f} ₹{s['stop_loss']:>9.2f} "
                    f"₹{s['take_profit']:>9.2f} {s['r_multiple']:>5.2f}")
            if with_tf:
                line += f" {s['tf']:>4s}"
            print(line)

    _table(intraday, "INTRADAY TRADES (15m)", with_tf=False)
    _table(swing, "SWING TRADES (15m / 1h)", with_tf=True)

    print(f"\n── SUMMARY ──")
    print(f"  INTRADAY: {len(intraday)}  |  SWING: {len(swing)}  |  TOTAL: {len(signals)}")
    print(f"  Tiers: consensus→15m_intraday→15m_swing→1h_swing "
          f"(consensus scanned in both intraday + swing)")


# ── Web dashboard server (--serve) ────────────────────────────────────────────
_latest_scan: dict = {"ts": "", "signals": [], "scanned_n": 0,
                      "status": "starting", "cycles": 0, "uptime": 0.0}
_scan_lock = threading.Lock()
_server_start = time.time()


def _publish(signals: list[dict], scanned_n: int, status: str = "ok") -> None:
    with _scan_lock:
        _latest_scan.update({
            "ts": pd.Timestamp.now(tz="Asia/Kolkata").strftime("%Y-%m-%d %H:%M %Z"),
            "signals": signals,
            "scanned_n": scanned_n,
            "status": status,
            "cycles": _latest_scan.get("cycles", 0) + 1,
        })


def _scan_worker(allow_shorts: bool, interval_min: int, source: str) -> None:
    """Background thread: re-scans on a timer, publishes to ``_latest_scan``."""
    from data.utils.market_hours import is_market_open, next_market_open
    while True:
        now = pd.Timestamp.now(tz="Asia/Kolkata")
        open_flag, _, _ = is_market_open(now)
        if open_flag:
            try:
                signals, scanned_n = _run_scan(allow_shorts)
                _publish(signals, scanned_n, "ok")
                with _scan_lock:
                    _latest_scan["source"] = source
            except Exception as e:
                _publish([], 0, f"error: {e}")
        else:
            with _scan_lock:
                _latest_scan["status"] = "closed — market not open"
            nxt = next_market_open(now)
            sleep_s = max(60, int((nxt - now).total_seconds()))
            time.sleep(sleep_s)
            continue
        time.sleep(interval_min * 60)


_DASHBOARD_HTML = None


def _load_dashboard_html() -> str:
    global _DASHBOARD_HTML
    if _DASHBOARD_HTML is None:
        path = os.path.join(os.path.dirname(__file__), "..", "web", "dashboard.html")
        with open(path) as f:
            _DASHBOARD_HTML = f.read()
    return _DASHBOARD_HTML


class _ScanHTTPHandler(http.server.BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/dashboard", "/index.html"):
            html = _load_dashboard_html().encode("utf-8")
            self._send(200, html, "text/html; charset=utf-8")
        elif self.path == "/api/latest":
            with _scan_lock:
                payload = dict(_latest_scan)
                payload["uptime"] = round(time.time() - _server_start, 1)
            self._send(200, json.dumps(payload).encode("utf-8"))
        elif self.path == "/api/status":
            with _scan_lock:
                payload = {k: _latest_scan[k] for k in
                           ("ts", "status", "cycles", "scanned_n")}
                payload["uptime"] = round(time.time() - _server_start, 1)
            self._send(200, json.dumps(payload).encode("utf-8"))
        else:
            self._send(404, b'{"error":"Not Found"}')

    def log_message(self, *args):  # silence default logging
        return


def _start_server(port: int) -> None:
    srv = http.server.ThreadingHTTPServer(("0.0.0.0", port), _ScanHTTPHandler)
    print(f"\n  Dashboard: http://0.0.0.0:{port}/  (network-accessible)")
    print(f"  API:       http://0.0.0.0:{port}/api/latest")
    print(f"  Ctrl-C to stop.\n")
    srv.serve_forever()


def main() -> None:
    ap = argparse.ArgumentParser(description="Live market scan → trade signals")
    ap.add_argument("--upstox", action="store_true",
                    help="Use Upstox real-broker feed instead of yfinance")
    ap.add_argument("--shorts", action="store_true",
                    help="Allow SHORT signals (off by default — not OOS-validated)")
    ap.add_argument("--loop", action="store_true", help="Re-scan every --interval min")
    ap.add_argument("--interval", type=int, default=15, help="Loop interval (min)")
    ap.add_argument("--list-tiers", action="store_true",
                    help="Print the scan tier plan and exit")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    ap.add_argument("--serve", action="store_true",
                    help="Start the web dashboard server (network-accessible)")
    ap.add_argument("--port", type=int, default=8080, help="Dashboard port (with --serve)")
    args = ap.parse_args()

    if args.list_tiers:
        print("Scan tiers (priority order):")
        for tier_label, wl_key, category, spec in SCAN_TIERS:
            print(f"  {tier_label:14s} wl={wl_key:14s} {category:8s} "
                  f"tf={spec['tf']} sl={spec['sl']} tp={spec['tp']} "
                  f"intraday={spec['intraday']}")
        return

    # configure data source for the shared fetchers
    _pt.USE_UPSTOX = args.upstox
    source = "upstox" if args.upstox else "yfinance"

    if args.serve:
        worker = threading.Thread(
            target=_scan_worker, args=(args.shorts, args.interval, source),
            daemon=True,
        )
        worker.start()
        # The worker runs the first scan on its initial iteration, so the
        # server can start immediately (dashboard shows "waiting for first
        # scan" until that completes). No blocking scan here.
        try:
            _start_server(args.port)
        except KeyboardInterrupt:
            print("\n  [stop] dashboard server stopped.")
        return

    if not args.loop:
        signals, scanned_n = _run_scan(args.shorts)
        if args.json:
            print(json.dumps({"signals": signals}, indent=2))
        else:
            _print_report(signals, source, scanned_n)
        return

    print(f"  Market scan loop started (interval={args.interval}m, source={source}). "
          f"Ctrl-C to stop.")
    try:
        while True:
            now = pd.Timestamp.now(tz="Asia/Kolkata")
            from data.utils.market_hours import is_market_open
            open_flag, _, _ = is_market_open(now)
            if open_flag:
                signals, scanned_n = _run_scan(args.shorts)
                if args.json:
                    print(json.dumps({"ts": now.strftime("%Y-%m-%d %H:%M"),
                                      "signals": signals}, indent=2))
                else:
                    _print_report(signals, source, scanned_n)
            else:
                print(f"  [closed] market not open at {now:%H:%M} — skipping")
                from data.utils.market_hours import next_market_open
                nxt = next_market_open(now)
                sleep_s = max(60, int((nxt - now).total_seconds()))
            time.sleep(args.interval * 60)
    except KeyboardInterrupt:
        print("\n  [stop] scan loop interrupted.")


if __name__ == "__main__":
    main()
