"""
Paper-trading simulator for the Institutional Probability strategy (15m intraday).

Reuses the EXACT live decision path as the backtest / live scanner
(``decide_trade`` + ``build_htf_context`` + the same yfinance live fetch), then
adds the missing piece for "paper trading": a simulated portfolio that

  * sizes positions by capital (1% risk = ₹500 on ₹50k, no leverage),
  * enforces max 5 new entries per day,
  * opens a paper position when ``decide_trade`` returns a LONG signal,
  * monitors open positions against the live close and fills SL/TP,
  * tracks cash, open positions, realized P&L and equity.

State persists to ``data/paper_portfolio.json`` so a crash/restart is safe.

NOTE: default live prices come from yfinance (delayed ~15-20 min). Pass --upstox
to use the Upstox real-broker feed (REST 1m→15m for bars, WebSocket for live
prices). This is still a SIMULATED portfolio — no real orders are placed; each
fill is logged with an Upstox-format order payload ready for deployment.

Usage
-----
  .venv/bin/python scripts/paper_trade.py                 # one scan+manage cycle
  .venv/bin/python scripts/paper_trade.py --loop --interval 15   # poll every 15m
  .venv/bin/python scripts/paper_trade.py --symbols ONGC,WIPRO,RELIANCE
  .venv/bin/python scripts/paper_trade.py --upstox --symbols ONGC,WIPRO,RELIANCE
  .venv/bin/python scripts/paper_trade.py --reset         # wipe state, start fresh
  .venv/bin/python scripts/paper_trade.py --upstox --loop --interval 15  # live broker feed
"""

from __future__ import annotations

import argparse
import json
import os
import sys as _sys
import time

_sys.path.insert(0, ".")

import pandas as pd

from scripts.backtest import (
    WINDOW_SIZE,
    build_htf_context,
    decide_trade,
    resolve_upstox_key,
)
from scripts.capital_model import (
    INITIAL_CAPITAL,
    MAX_TRADES_PER_DAY,
    RISK_PER_TRADE_PCT,
    position_size_for,
)
from scripts.live_institutional_scan import (
    FOCUSED_WATCHLIST,
    FORCE_STRATEGY,
    MIN_SCORE,
    TUNING,
    _bars_until_close,
    _classify_stock_type,
    _yf_live,
)
from scripts.live_scanner import classify_today_day_type

# ── Capital model ──
# Pulled from scripts/capital_model (shared with the backtest engine) so the
# risk model can never diverge between simulation and live trading.

STATE_PATH = "data/paper_portfolio.json"
TF = "15m"

USE_UPSTOX = False  # set True via --upstox; uses the Upstox real-broker feed
REAL_ORDERS = False  # set True via --real; places actual Upstox orders (live money)
ALLOW_SHORTS = False  # set True via --shorts; SHORT not yet OOS-validated


# ── Upstox live data (real broker feed) ──
def _instrument_key_for(symbol: str):
    """Resolve a yfinance-style symbol to an Upstox instrument key."""
    if symbol in ("^NSEI", "NIFTY", "Nifty 50"):
        return "NSE_INDEX|Nifty 50"
    if symbol in ("^NSEBANK", "^BANKNIFTY", "Bank Nifty"):
        return "NSE_INDEX|Nifty Bank"
    return resolve_upstox_key(f"{symbol}.NS", "upstox")


def _upstox_live(symbol: str, timeframe: str):
    """Fetch OHLCV from Upstox. 15m is built by resampling 1m (Upstox has no
    native 15m bar); 1d uses the daily interval. Returns the same DataFrame
    contract as ``_yf_live``: columns [timestamp, open, high, low, close,
    volume], tz-naive IST."""
    from config.daemon_config import UPSTOX
    from data.upstox.upstox_market_data_provider import UpstoxMarketDataProvider
    from datetime import datetime, timedelta

    token = UPSTOX.get("access_token", "")
    if not token:
        return None
    key = _instrument_key_for(symbol)
    if not key:
        return None
    try:
        provider = UpstoxMarketDataProvider(token)
        if timeframe == "15m":
            start = datetime.now() - timedelta(days=8)
            df = provider.load_historical_data(key, "1m", start_date=start)
            if df is None or len(df) < 200:
                return None
            df = _resample_safe(df, 15)
        elif timeframe == "1d":
            start = datetime.now() - timedelta(days=730)
            df = provider.load_historical_data(key, "1d", start_date=start)
        else:
            return None
        if df is None or df.empty:
            return None
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        if df["timestamp"].dt.tz is not None:
            df["timestamp"] = df["timestamp"].dt.tz_localize(None)
        return df
    except Exception:
        return None


def _upstox_live_price(symbol: str):
    """Latest tradable price for a held stock via Upstox WebSocket batch."""
    from data.downloader.data_registry import get_live_price
    try:
        px = get_live_price(symbol)
        if px and px.get("close"):
            return float(px["close"])
    except Exception:
        return None
    return None


def _order_payload(symbol, txn_type, qty, price, trigger, sl):
    """Upstox-format order payload for a fill (ready to POST to /v2/orders)."""
    return {
        "exchange": "NSE",
        "symbol": symbol,
        "instrument_key": _instrument_key_for(symbol) if USE_UPSTOX else None,
        "quantity": qty,
        "transaction_type": txn_type,
        "order_type": "SL" if (trigger is not None or sl is not None) else "MARKET",
        "price": price,
        "trigger_price": trigger,
        "stop_loss": sl,
    }


def place_upstox_order(order: dict) -> str | None:
    """Place a REAL order via Upstox ``/v2/order/place``. Returns order_id or None.

    Never raises — callers keep paper tracking if it fails (e.g. token lacks
    trade scope). Only invoke when REAL_ORDERS is set.
    """
    from config.daemon_config import UPSTOX
    token = UPSTOX.get("access_token", "")
    if not token:
        print("[order] WARN no Upstox token — cannot place real order")
        return None
    body = {
        "quantity": int(order["quantity"]),
        "product": "I",  # intraday
        "validity": "DAY",
        "price": float(order.get("price") or 0),
        "tag": "inst-prob",
        "instrument_token": order["instrument_key"],
        "order_type": order["order_type"],  # MARKET / LIMIT / SL / SL-M
        "transaction_type": order["transaction_type"],  # BUY / SELL
        "disclosed_quantity": 0,
        "trigger_price": float(order.get("trigger_price") or 0),
        "is_amo": False,
    }
    url = "https://api.upstox.com/v2/order/place"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    try:
        from data.upstox.upstox_http import upstox_post
        resp = upstox_post(url, headers=headers, json=body, timeout=15)
        if resp.status_code != 200:
            print(f"[order] WARN Upstox HTTP {resp.status_code}: {resp.text[:200]}")
            return None
        return resp.json().get("data", {}).get("order_id")
    except Exception as e:
        print(f"[order] WARN Upstox order error: {e}")
        return None



# ── sizing (delegates to shared scripts.capital_model.position_size_for) ──


def _load_state() -> dict:
    if not os.path.exists(STATE_PATH):
        return {
            "cash": INITIAL_CAPITAL,
            "day": None,
            "day_entries": 0,
            "positions": [],
            "trades": [],
            "equity_curve": [{"ts": None, "equity": INITIAL_CAPITAL}],
        }
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError) as e:
        import shutil
        backup = STATE_PATH + ".corrupt"
        try:
            shutil.copy2(STATE_PATH, backup)
        except Exception:
            backup = STATE_PATH
        print(f"[state] WARN corrupt state file ({e}); backed up to {backup}; "
              f"starting fresh")
        return {
            "cash": INITIAL_CAPITAL,
            "day": None,
            "day_entries": 0,
            "positions": [],
            "trades": [],
            "equity_curve": [{"ts": None, "equity": INITIAL_CAPITAL}],
        }


def _save_state(state: dict) -> None:
    os.makedirs("data", exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def _equity(state: dict, prices: dict) -> float:
    eq = state["cash"]
    for p in state["positions"]:
        px = prices.get(p["symbol"])
        if px is not None:
            if p["direction"] == "LONG":
                eq += p["shares"] * px
            else:  # SHORT mark-to-market: liability = shares * price
                eq += p["shares"] * (p["entry_price"] - px)
    return eq


def _record_exit(state: dict, p: dict, exit_price: float, now, result: str, reason: str) -> dict:
    """Close an open position at ``exit_price``; update cash + append a fill.

    LONG is closed with a SELL (cash returns at exit price); SHORT is closed
    with a BUY (net P&L booked — no cash moved at short open, so the whole
    ``pnl`` lands at exit). The order payload transaction_type follows the
    direction (SELL to close a LONG, BUY to close a SHORT).
    """
    direction = p["direction"]
    pnl = p["shares"] * (exit_price - p["entry_price"]) if direction == "LONG" \
        else p["shares"] * (p["entry_price"] - exit_price)
    risk = abs(p["entry_price"] - p["stop_loss"])
    r_mult = (abs(exit_price - p["entry_price"]) / risk) if result == "WIN" else -1.0
    if direction == "LONG":
        state["cash"] += p["shares"] * exit_price
    else:  # SHORT: net P&L lands at exit (no cash moved at open)
        state["cash"] += pnl
    close_txn = "BUY" if direction == "SHORT" else "SELL"
    fill = {
        "symbol": p["symbol"], "direction": direction, "side": "EXIT",
        "entry_price": round(p["entry_price"], 2), "exit_price": round(exit_price, 2),
        "shares": p["shares"], "pnl": round(pnl, 2),
        "r_multiple": round(r_mult, 3), "result": result,
        "ts": now.strftime("%Y-%m-%d %H:%M"), "reason": reason,
        "order": _order_payload(p["symbol"], close_txn, p["shares"],
                                round(exit_price, 2), None, None),
    }
    state["trades"].append(fill)
    return fill


def _evaluate_symbol(sym: str, nifty_15m, nifty_1d, now, live_price=None):
    """Fetch live data for one symbol, return (decision_or_None, current_price).

    Uses the Upstox feed when ``USE_UPSTOX`` is set, else yfinance. ``live_price``
    (when given) overrides the last-bar close as the current price for exit checks.
    """
    yf_sym = f"{sym}.NS"
    try:
        if USE_UPSTOX:
            stock_15m = _upstox_live(sym, TF)
        else:
            stock_15m = _yf_live(yf_sym, TF)
        if stock_15m is None or len(stock_15m) < WINDOW_SIZE + 5:
            return None, None
        if USE_UPSTOX:
            stock_1d = _upstox_live(sym, "1d")
        else:
            stock_1d = _yf_live(yf_sym, "1d")
        stock_30m = _resample_safe(stock_15m, 30)
    except Exception:
        return None, None

    last_ts = stock_15m["timestamp"].iloc[-1]
    today = last_ts.date() if hasattr(last_ts, "date") else last_ts
    current_price = live_price if live_price is not None else float(stock_15m["close"].iloc[-1])

    window = stock_15m.tail(WINDOW_SIZE).reset_index(drop=True)
    nifty_win = nifty_15m.tail(WINDOW_SIZE).reset_index(drop=True) if nifty_15m is not None else None
    if nifty_win is None or len(nifty_win) < WINDOW_SIZE:
        nifty_win = window

    day_info = classify_today_day_type()
    day_type = day_info.get("day_type", "UNKNOWN")
    stock_type = _classify_stock_type(window, nifty_win, stock_1d, today)
    htf_ctx = build_htf_context(stock_30m, stock_1d, last_ts)
    intraday_remaining = _bars_until_close(last_ts)

    decision = decide_trade(
        window, yf_sym, TF,
        day_type, stock_type,
        nifty_15m, stock_1d, stock_30m, last_ts,
        force_strategy=FORCE_STRATEGY,
        tuning_override=TUNING,
        multi_tf_filter=True,
        intraday_mode=True,
        intraday_remaining_bars=intraday_remaining,
        htf_ctx=htf_ctx,
    )
    return decision, current_price


def _resample_safe(df, minutes):
    from scripts.backtest import _resample_1m_to
    try:
        return _resample_1m_to(df, minutes)
    except Exception:
        return None


def run_cycle(state: dict, symbols: list[str]) -> dict:
    now = pd.Timestamp.now(tz="Asia/Kolkata")
    now_date = now.strftime("%Y-%m-%d")

    # reset daily entry counter on a new day
    if state.get("day") != now_date:
        state["day"] = now_date
        state["day_entries"] = 0

    print("=" * 70)
    print(f"  PAPER TRADING CYCLE — {now.strftime('%Y-%m-%d %H:%M %Z')}")
    print(f"  Cash: ₹{state['cash']:,.0f} | Day entries: {state['day_entries']}/{MAX_TRADES_PER_DAY} | "
          f"Open: {len(state['positions'])}")
    print("=" * 70)

    nifty_15m = _upstox_live("^NSEI", TF) if USE_UPSTOX else _yf_live("^NSEI", TF)
    nifty_1d = _upstox_live("^NSEI", "1d") if USE_UPSTOX else _yf_live("^NSEI", "1d")

    prices = {}
    new_fills = []

    # ── 0) intraday EOD force-close ──
    # Real NSE intraday (product "I") positions are auto-squared-off at 15:30 IST.
    # A paper position opened on a previous day must never be carried across the
    # close — close it at the current price to avoid fictitious overnight P&L.
    for p in list(state["positions"]):
        opened_date = (p.get("opened_at") or "")[:10]
        if opened_date and opened_date != now_date:
            live_price = _upstox_live_price(p["symbol"]) if USE_UPSTOX else None
            _, cur = _evaluate_symbol(p["symbol"], nifty_15m, nifty_1d, now, live_price=live_price)
            exit_price = cur if cur is not None else p["entry_price"]
            if p["direction"] == "LONG":
                result = "WIN" if (exit_price - p["entry_price"]) >= 0 else "LOSS"
            else:  # SHORT: profit when close is below entry
                result = "WIN" if (p["entry_price"] - exit_price) >= 0 else "LOSS"
            fill = _record_exit(state, p, exit_price, now, result, "EOD-FORCE-CLOSE")
            state["positions"].remove(p)
            new_fills.append(fill)
            print(f"  EOD   {p['symbol']:10s} close @₹{exit_price:.2f}  "
                  f"PnL=₹{fill['pnl']:+,.0f}  R={fill['r_multiple']:+.2f}  "
                  f"(opened {opened_date})")

    # ── 1) manage open positions (exit checks) ──
    still_open = []
    for p in state["positions"]:
        sym = p["symbol"]
        if p.get("exit_order_id"):
            still_open.append(p)  # exit order already placed; await fill
            continue
        live_price = _upstox_live_price(sym) if USE_UPSTOX else None
        decision, cur = _evaluate_symbol(sym, nifty_15m, nifty_1d, now, live_price=live_price)
        if cur is None:
            still_open.append(p)  # no data this cycle → keep holding
            continue
        prices[sym] = cur
        exit_price = None
        result = None
        if p["direction"] == "LONG":
            if cur <= p["stop_loss"]:
                exit_price, result = p["stop_loss"], "LOSS"
            elif cur >= p["take_profit"]:
                exit_price, result = p["take_profit"], "WIN"
        else:  # SHORT: SL above entry, TP below entry
            if cur >= p["stop_loss"]:
                exit_price, result = p["stop_loss"], "LOSS"
            elif cur <= p["take_profit"]:
                exit_price, result = p["take_profit"], "WIN"
        if exit_price is not None:
            fill = _record_exit(state, p, exit_price, now, result, "SIGNAL")
            new_fills.append(fill)
            print(f"  EXIT  {sym:10s} {result:4s} @₹{exit_price:.2f}  "
                  f"PnL=₹{fill['pnl']:+,.0f}  R={fill['r_multiple']:+.2f}")
        else:
            still_open.append(p)
    state["positions"] = still_open

    # ── 2) scan for new entries ──
    if state["day_entries"] >= MAX_TRADES_PER_DAY:
        print(f"  [cap] daily entry limit ({MAX_TRADES_PER_DAY}) reached — no new entries")
    else:
        open_syms = {p["symbol"] for p in state["positions"]}
        for sym in symbols:
            if sym in open_syms:
                continue
            if state["day_entries"] >= MAX_TRADES_PER_DAY:
                break
            live_price = _upstox_live_price(sym) if USE_UPSTOX else None
            decision, cur = _evaluate_symbol(sym, nifty_15m, nifty_1d, now, live_price=live_price)
            if decision is None or cur is None:
                continue
            # SHORT is opt-in (not yet OOS-validated — see AGENTS.md Phase 6).
            if decision.direction == "SHORT" and not ALLOW_SHORTS:
                continue
            direction = decision.direction
            notional = position_size_for(decision.entry_price, decision.stop_loss)
            if notional <= 0:
                continue
            # Cannot deploy more notional than free cash (no leverage across
            # concurrent positions — the backtest ignored this, paper trading
            # must not drive cash negative). Applies to LONG margin and SHORT
            # margin alike.
            notional = min(notional, state["cash"])
            shares = int(notional / decision.entry_price)
            if shares < 1:
                continue
            if direction == "LONG":
                state["cash"] -= shares * decision.entry_price
            # SHORT: no cash moved at open (proceeds tracked via mark-to-market
            # equity); the net P&L lands when the position is closed.
            entry_txn = "SELL" if direction == "SHORT" else "BUY"
            pos = {
                "symbol": sym, "direction": direction,
                "entry_price": round(decision.entry_price, 2),
                "stop_loss": round(decision.stop_loss, 2),
                "take_profit": round(decision.take_profit, 2),
                "shares": shares, "opened_at": now.strftime("%Y-%m-%d %H:%M"),
                "score": round(decision.score, 1),
            }
            state["positions"].append(pos)
            state["day_entries"] += 1
            state["trades"].append({
                "symbol": sym, "direction": direction, "side": "ENTRY",
                "entry_price": round(decision.entry_price, 2),
                "stop_loss": round(decision.stop_loss, 2),
                "take_profit": round(decision.take_profit, 2),
                "shares": shares, "ts": now.strftime("%Y-%m-%d %H:%M"),
                "order": _order_payload(sym, entry_txn, shares,
                                        round(decision.entry_price, 2), None,
                                        round(decision.stop_loss, 2)),
            })
            print(f"  ENTRY {sym:10s} {direction:5s} @₹{decision.entry_price:.2f}  "
                  f"SL=₹{decision.stop_loss:.2f} TP=₹{decision.take_profit:.2f}  "
                  f"shares={shares} (₹{shares*decision.entry_price:,.0f})")

    # ── 3) equity snapshot ──
    equity = _equity(state, prices)
    state["equity_curve"].append({"ts": now.strftime("%Y-%m-%d %H:%M"), "equity": round(equity, 2)})
    if len(state["equity_curve"]) > 5000:
        state["equity_curve"] = state["equity_curve"][-5000:]
    print(f"  Equity: ₹{equity:,.0f}  (cash ₹{state['cash']:,.0f} + "
          f"{len(state['positions'])} open positions)")
    return state


def _market_open(now: pd.Timestamp) -> bool:
    """True only during NSE trading hours on a non-holiday weekday.

    Delegates to ``data.utils.market_hours.is_market_open`` so weekends AND the
    NSE holiday calendar are respected (the paper trader must not open fake
    positions on a closed market with stale prices).
    """
    from data.utils.market_hours import is_market_open
    open_flag, _, _ = is_market_open(now)
    return open_flag


def _load_watchlist(name: str) -> list[str]:
    path = "data/symbol_watchlists.json"
    if not os.path.exists(path):
        raise SystemExit(f"  [error] watchlist file not found: {path}")
    data = json.load(open(path))
    if name not in data:
        avail = ", ".join(k for k in data if k != "details")
        raise SystemExit(f"  [error] unknown watchlist '{name}'. Available: {avail}")
    syms = list(data[name])
    if not syms:
        raise SystemExit(f"  [error] watchlist '{name}' is empty")
    print(f"  Loaded watchlist '{name}' ({len(syms)} symbols)")
    return syms


def _print_watchlists() -> None:
    path = "data/symbol_watchlists.json"
    if not os.path.exists(path):
        print(f"  [error] watchlist file not found: {path}")
        return
    data = json.load(open(path))
    print("Available watchlists (data/symbol_watchlists.json):")
    for k, v in data.items():
        if k == "details":
            continue
        n = len(v) if isinstance(v, list) else 0
        print(f"  {k:16s} {n} symbols")
    print("\nUse with: --watchlist <name>")


def main() -> None:
    ap = argparse.ArgumentParser(description="Paper-trading simulator (15m intraday)")
    ap.add_argument("--loop", action="store_true", help="Poll during market hours")
    ap.add_argument("--interval", type=int, default=15, help="Poll interval (min)")
    ap.add_argument("--symbols", default=None, help="comma/space separated subset")
    ap.add_argument("--watchlist", default=None,
                    help="named list from data/symbol_watchlists.json "
                         "(15m_intraday, 15m_swing, 1h_swing, consensus, full_consensus)")
    ap.add_argument("--list-watchlists", action="store_true",
                    help="print available watchlists and exit")
    ap.add_argument("--reset", action="store_true", help="wipe state and start fresh")
    ap.add_argument("--upstox", action="store_true",
                    help="Use Upstox real-broker feed instead of yfinance")
    ap.add_argument("--shorts", action="store_true",
                    help="Allow SHORT entries (off by default — not yet OOS-validated)")
    args = ap.parse_args()

    if args.list_watchlists:
        _print_watchlists()
        return

    global USE_UPSTOX, ALLOW_SHORTS
    USE_UPSTOX = args.upstox
    ALLOW_SHORTS = args.shorts

    if args.reset and os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)
        print("  [reset] cleared paper portfolio state")

    if args.symbols:
        symbols = []
        for tok in args.symbols.replace(",", " ").split():
            tok = tok.strip().replace(".NS", "").upper()
            if tok:
                symbols.append(tok)
    elif args.watchlist:
        symbols = _load_watchlist(args.watchlist)
    else:
        symbols = list(FOCUSED_WATCHLIST)

    state = _load_state()
    if args.reset:
        state = _load_state()  # already cleared; rebuild fresh

    if not args.loop:
        state = run_cycle(state, symbols)
        _save_state(state)
        return

    print(f"  Paper-trading loop started (interval={args.interval}m, "
          f"{len(symbols)} symbols). Ctrl-C to stop.")
    MAX_CONSECUTIVE_FAILURES = 5
    fail_count = 0
    try:
        while True:
            now = pd.Timestamp.now(tz="Asia/Kolkata")
            if _market_open(now):
                try:
                    state = run_cycle(state, symbols)
                    _save_state(state)
                    fail_count = 0
                except Exception as e:
                    fail_count += 1
                    import traceback
                    traceback.print_exc()
                    print(f"  [error] cycle {fail_count}/{MAX_CONSECUTIVE_FAILURES} "
                          f"failed: {e}")
                    if fail_count >= MAX_CONSECUTIVE_FAILURES:
                        print("  [stop] too many consecutive failures; aborting loop.")
                        raise
            else:
                print(f"  [skip] market closed ({now.strftime('%H:%M')}) — waiting")
            # sleep until next interval (or until next market open if closed)
            sleep_s = args.interval * 60
            if not _market_open(now):
                # wake at the next real market open (skips weekends + holidays)
                from data.utils.market_hours import next_market_open
                nxt = next_market_open(now)
                sleep_s = max(60, int((nxt - now).total_seconds()))
            time.sleep(sleep_s)
    except KeyboardInterrupt:
        print("\n  [stop] loop interrupted; state saved.")
        _save_state(state)


if __name__ == "__main__":
    main()
