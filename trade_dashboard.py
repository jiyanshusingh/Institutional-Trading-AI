"""
ICT Trade Dashboard

Streamlit app that runs the ICT pipeline on selected stocks
and displays trade recommendations in detailed format.

Usage:
    streamlit run trade_dashboard.py
"""

import json
import os
import sys
from datetime import datetime, timezone

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.insert(0, ".")

from services.ict_analysis_service import ICTAnalysisService


# ── Watchlist ──────────────────────────────────────────────────────
# (symbol, display_name, provider_type, exchange)
WATCHLIST = [
    # NSE Stocks
    ("RELIANCE.NS", "Reliance Industries", "yfinance", "NSE"),
    ("TCS.NS", "Tata Consultancy Services", "yfinance", "NSE"),
    ("HDFCBANK.NS", "HDFC Bank", "yfinance", "NSE"),
    ("ICICIBANK.NS", "ICICI Bank", "yfinance", "NSE"),
    ("INFY.NS", "Infosys", "yfinance", "NSE"),
    ("SBIN.NS", "State Bank of India", "yfinance", "NSE"),
    ("LT.NS", "Larsen & Toubro", "yfinance", "NSE"),
    ("ITC.NS", "ITC", "yfinance", "NSE"),
    ("HINDUNILVR.NS", "Hindustan Unilever", "yfinance", "NSE"),
    ("BHARTIARTL.NS", "Bharti Airtel", "yfinance", "NSE"),
    ("MARUTI.NS", "Maruti Suzuki", "yfinance", "NSE"),
    ("TATAMOTORS.NS", "Tata Motors", "yfinance", "NSE"),
    ("AXISBANK.NS", "Axis Bank", "yfinance", "NSE"),
    ("KOTAKBANK.NS", "Kotak Mahindra Bank", "yfinance", "NSE"),
    ("BAJFINANCE.NS", "Bajaj Finance", "yfinance", "NSE"),
    ("WIPRO.NS", "Wipro", "yfinance", "NSE"),
    ("MARICO.NS", "Marico", "yfinance", "NSE"),
    ("TITAN.NS", "Titan Company", "yfinance", "NSE"),
    ("ASIANPAINT.NS", "Asian Paints", "yfinance", "NSE"),
    ("NESTLEIND.NS", "Nestle India", "yfinance", "NSE"),
    ("DMART.NS", "Avenue Supermarts", "yfinance", "NSE"),
    ("TRENT.NS", "Trent", "yfinance", "NSE"),
    ("ZOMATO.NS", "Zomato", "yfinance", "NSE"),
    ("PERSISTENT.NS", "Persistent Systems", "yfinance", "NSE"),
    ("MCX.NS", "MCX India", "yfinance", "NSE"),
    # COMEX Futures
    ("GC=F", "Gold Futures", "yfinance", "COMEX"),
    ("SI=F", "Silver Futures", "yfinance", "COMEX"),
    ("CL=F", "Crude Oil Futures", "yfinance", "COMEX"),
    ("NG=F", "Natural Gas Futures", "yfinance", "COMEX"),
]

COMMODITY_SYMBOLS = [
    ("MCX_FO|555922", "Gold MCX Mini", "upstox", "MCX"),
    ("MCX_FO|471726", "Silver MCX Mini", "upstox", "MCX"),
    ("MCX_FO|520702", "Crude Oil MCX", "upstox", "MCX"),
    ("MCX_FO|562048", "Copper MCX", "upstox", "MCX"),
]

TIMEFRAMES = [("15m", 200), ("1h", 96), ("1d", 200)]


# ── Page Config ────────────────────────────────────────────────────

st.set_page_config(
    page_title="Trading Setup",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Trading Setup")
st.caption("AI-powered trade recommendations")

# ── Market Overview (from live scanner) ────────────────────────────

_scan_path = "data/live_scan.json"
if os.path.exists(_scan_path):
    try:
        with open(_scan_path) as _f:
            _scan = json.load(_f)

        _ts = _scan.get("timestamp", "N/A")
        _dt = _scan.get("day_type", "N/A")
        _nifty = _scan.get("nifty")
        _nifty_chg = _scan.get("nifty_change_pct")
        _buys = _scan.get("buys", [])
        _avoids = _scan.get("avoids", [])

        # Color for day type
        _dt_color = {"TREND_UP": "🟢", "TREND_DOWN": "🔴", "RANGE": "🟡",
                     "GAP_UP": "🟢", "GAP_DOWN": "🔴", "REVERSAL": "🟠", "CHOPPY": "⚪"}
        _dt_icon = _dt_color.get(_dt, "⚪")

        with st.container(border=True):
            cols = st.columns([2, 1, 1, 1, 1, 1])
            with cols[0]:
                st.markdown(f"**📊 Market Overview**  \n"
                            f"Scan: {_ts}")
            with cols[1]:
                st.metric("Day Type", f"{_dt_icon} {_dt}")
            with cols[2]:
                st.metric("NIFTY", f"{_nifty:,.0f}" if _nifty else "—",
                          f"{_nifty_chg:+.2f}%" if _nifty_chg is not None else "")
            with cols[3]:
                st.metric("Buy Setups", len(_buys))
            with cols[4]:
                st.metric("Avoid", len(_avoids))
            with cols[5]:
                st.metric("Bars Today", _scan.get("bars_today", "—"))

        if _buys:
            with st.expander(f"🔵 Buy Setups ({len(_buys)})", expanded=True):
                _buy_df = pd.DataFrame([{
                    "Symbol": b["name"],
                    "Price": f"₹{b['price']:,.2f}",
                    "Chg%": f"{b['change_pct']:+.1f}%",
                    "Type": b["stock_type"],
                    "Strategy": b["strategy"],
                    "SL": f"₹{b['sl']:,.2f}",
                    "TP": f"₹{b['tp']:,.2f}",
                    "WR%": b["hist_wr"],
                    "PF": b["hist_pf"],
                    "Trades": b["hist_trades"],
                } for b in _buys])
                st.dataframe(_buy_df, hide_index=True, use_container_width=True)

        if _avoids:
            with st.expander(f"🔴 Avoid ({len(_avoids)})", expanded=False):
                _avoid_df = pd.DataFrame([{
                    "Symbol": a["name"],
                    "Price": f"₹{a['price']:,.2f}",
                    "Chg%": f"{a['change_pct']:+.1f}%",
                    "Type": a["stock_type"],
                    "WR%": a["hist_wr"],
                    "PF": a["hist_pf"],
                } for a in _avoids])
                st.dataframe(_avoid_df, hide_index=True, use_container_width=True)

        st.divider()

    except Exception as _e:
        st.caption(f"Market overview unavailable: {_e}")

# ── Live Prices (WebSocket) ────────────────────────────────────────

with st.expander("🔴 LIVE PRICES", expanded=False):
    try:
        from config.daemon_config import UPSTOX, UPSTOX_NSE_KEYS
        from data.upstox.upstox_live_feed import UpstoxLiveFeed
        _token = UPSTOX.get("access_token", "")
        if _token:
            # Resolve NSE watchlist to instrument keys
            _ws_keys = []
            _ws_names = []
            for _sym, _name, _prov, _exch in WATCHLIST:
                if _exch != "NSE":
                    continue
                _base = _sym.replace(".NS", "")
                _key = UPSTOX_NSE_KEYS.get(_base)
                if _key:
                    _ws_keys.append(_key)
                    _ws_names.append(_name)

            if _ws_keys:
                _feed = UpstoxLiveFeed(_token)
                _batch = _feed.get_live_batch(_ws_keys, mode="full", timeout=10)
                _rows = []
                for _k, _n in zip(_ws_keys, _ws_names):
                    _o = _batch.get(_k)
                    if _o is None:
                        continue
                    _intervals = _o.get("_intervals") or {}
                    _daily = _intervals.get("1d") or _o
                    _ltp = float(_daily.get("close", 0))
                    _open = float(_daily.get("open", 0))
                    _chg = ((_ltp - _open) / _open * 100) if _open else 0
                    _arrow = "🟢" if _chg > 0 else ("🔴" if _chg < 0 else "⚪")
                    _rows.append({"Symbol": _n, "LTP": f"₹{_ltp:,.2f}", "Chg%": f"{_arrow} {_chg:+.2f}%"})
                if _rows:
                    st.dataframe(pd.DataFrame(_rows), hide_index=True, use_container_width=True)
                else:
                    st.caption("No live data received")
            else:
                st.caption("No Upstox NSE keys cached — run scanner first")
        else:
            st.caption("No Upstox token")
    except Exception as _e:
        st.caption(f"Live prices unavailable: {_e}")

# ── Sidebar ────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Configuration")

    exchange_filter = st.multiselect(
        "Exchange",
        ["NSE", "COMEX", "MCX"],
        default=["NSE"],
    )

    available = WATCHLIST + (COMMODITY_SYMBOLS if "MCX" in exchange_filter else [])
    filtered = [s for s in available if s[3] in exchange_filter]

    selected = st.multiselect(
        "Stocks to Analyze",
        options=[s[0] for s in filtered],
        format_func=lambda x: next((s[1] for s in filtered if s[0] == x), x),
        default=[s[0] for s in filtered[:3]] if filtered else [],
    )

    analyze_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

    st.divider()
    st.subheader("Trade Parameters")

    sl_mult = st.slider("Stop Loss Multiplier", 1.0, 5.0, 3.0, 0.5)
    tp_mult = st.slider("Take Profit Multiplier", 1.0, 6.0, 4.0, 0.5)
    atr_period = st.slider("ATR Period", 7, 21, 14)
    min_rr = st.slider("Min Risk:Reward", 0.0, 3.0, 0.0, 0.25)

    st.caption(f"Using ICT trade constructor with ATR({atr_period}), "
               f"SL={sl_mult}x, TP={tp_mult}x")

# ── Session State ──────────────────────────────────────────────────

if "service" not in st.session_state:
    st.session_state.service = ICTAnalysisService()
if "results" not in st.session_state:
    st.session_state.results = {}

service = st.session_state.service


# ── Analysis Logic ─────────────────────────────────────────────────

def run_analysis(symbol, name, provider_type):
    """Run ICT pipeline on all timeframes for a single stock."""
    results = {}
    stock_profile = service.get_stock_profile(symbol)
    hist_context = service.get_historical_context(symbol)

    tf_results = service.analyze_all_timeframes(symbol, name, TIMEFRAMES, provider_type)
    if tf_results:
        results["timeframes"] = tf_results
    results["profile"] = stock_profile
    results["history"] = hist_context

    results["day_type"] = service.get_day_type()
    results["stock_type"] = service.get_stock_type(symbol, provider_type)
    results["strategy"] = service.get_strategy_recommendation(
        results["day_type"].get("type", "UNKNOWN"),
        results["stock_type"].get("type", "UNKNOWN"),
    )
    return results


# ── Display Functions ──────────────────────────────────────────────

def show_market_bias(context):
    st.subheader("Market Bias")
    cols = st.columns(len(context))
    for i, (name, data) in enumerate(context.items()):
        with cols[i]:
            if data["value"]:
                st.metric(name, f'{data["value"]:,.0f}', f'{data["change"]:+.2f}%')
            else:
                st.metric(name, "N/A")

    # Determine overall bias
    changes = [d["change"] for d in context.values() if d["change"] is not None]
    if changes:
        avg = sum(changes) / len(changes)
        if avg > 0.5:
            st.success(f"**Bias: Bullish** — Broad market participation is positive. Risk appetite is strong.")
        elif avg < -0.5:
            st.warning(f"**Bias: Bearish** — Broad market under pressure. Caution advised.")
        else:
            st.info(f"**Bias: Neutral** — Mixed market action. Stock-specific approach.")


def show_stock_analysis(name, symbol, profile, hist_context, tf_results):
    st.subheader(f"{name} ({symbol})")

    # Price snapshot
    cp = profile.get("current") or profile.get("today_close", "N/A")
    day_chg = profile.get("intraday_change_pct") or profile.get("daily_change_pct", 0)
    vol = profile.get("volume", 0)
    vol_ratio = profile.get("vol_ratio", 1.0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"₹{cp:,.2f}" if isinstance(cp, (int, float)) else str(cp),
                  f"{day_chg:+.2f}%" if isinstance(day_chg, (int, float)) else "")
    with col2:
        day_hi = profile.get("high", "—")
        day_lo = profile.get("low", "—")
        st.metric("Day Range", f"₹{day_lo:,.2f} – ₹{day_hi:,.2f}" if isinstance(day_lo, (int, float)) else "—")
    with col3:
        st.metric("Volume", f"{vol:,}" if vol else "—",
                  f"{vol_ratio:.2f}x avg" if isinstance(vol_ratio, (int, float)) else "")
    with col4:
        pos = profile.get("day_range_pct")
        st.metric("Position in Range", f"{pos:.0f}%" if pos is not None else "—",
                  "Near High" if pos and pos >= 80 else "Near Low" if pos and pos <= 20 else "Mid-Range")

    # Institutional reading
    prev_close = hist_context.get("prev_day_close")
    prev_low = hist_context.get("prev_day_low")
    prev_hi = hist_context.get("prev_day_high")

    with st.expander("📊 Institutional Reading", expanded=True):
        col_a, col_b = st.columns(2)

        with col_a:
            if prev_low and profile.get("low") is not None:
                made_lower_low = profile["low"] < prev_low
                if made_lower_low:
                    st.markdown("**Yesterday:** Distribution / selloff below prior support")
                    st.markdown(f"- Closed at ₹{prev_close:,.2f}")
                    st.markdown(f"- Made a **lower low** (₹{profile['low']:,.2f} < ₹{prev_low:,.2f})")
                else:
                    st.markdown("**Yesterday:** Corrective but held structure")
                    st.markdown(f"- Closed at ₹{prev_close:,.2f}")

            if prev_hi and profile.get("high") is not None:
                recovery = profile["high"] > prev_hi
                if recovery and profile.get("current") and profile.get("low"):
                    st.markdown("**Today:** Strong recovery / accumulation")
                    st.markdown(f"- Recovered from ₹{profile['low']:,.2f} → ₹{profile['current']:,.2f}")
                    st.markdown(f"- Broke above yesterday's high (₹{prev_hi:,.2f})")
                elif profile.get("current") and profile.get("low"):
                    st.markdown("**Today:** Consolidation / recovery ongoing")
                    st.markdown(f"- Range: ₹{profile['low']:,.2f} – ₹{profile['high']:,.2f}")

        with col_b:
            bullish = profile.get("bullish_candles", 0)
            bearish = profile.get("bearish_candles", 0)
            total = profile.get("candle_count", 1)
            candle_verdict = "Bullish dominance" if bullish > bearish else "Bearish pressure" if bearish > bullish else "Balanced"

            st.markdown(f"**Candle Analysis (15m)**")
            st.markdown(f"- Bullish candles: {bullish}/{total}")
            st.markdown(f"- Bearish candles: {bearish}/{total}")
            st.markdown(f"- Verdict: **{candle_verdict}**")

            if vol_ratio and isinstance(vol_ratio, (int, float)) and vol_ratio > 1.2:
                st.markdown(f"- Volume: **{vol_ratio:.2f}x** average — elevated participation")
            elif vol_ratio:
                st.markdown(f"- Volume: {vol_ratio:.2f}x average")

    # What changed
    with st.expander("🔄 What Changed?", expanded=True):
        col_x, col_y = st.columns(2)
        with col_x:
            st.markdown("**Yesterday**")
            st.markdown(f"- Close: ₹{prev_close:,.2f}" if prev_close else "- N/A")
            st.markdown(f"- High: ₹{prev_hi:,.2f}" if prev_hi else "")
            st.markdown(f"- Low: ₹{prev_low:,.2f}" if prev_low else "")
        with col_y:
            st.markdown("**Today**")
            st.markdown(f"- Current: ₹{profile.get('current', 0):,.2f}" if profile.get('current') else "")
            st.markdown(f"- High: ₹{profile.get('high', 0):,.2f}" if profile.get('high') else "")
            st.markdown(f"- Low: ₹{profile.get('low', 0):,.2f}" if profile.get('low') else "")
            if prev_close and profile.get("current"):
                diff = ((profile["current"] - prev_close) / prev_close) * 100
                st.markdown(f"- Change: **{diff:+.2f}%**")


def show_price_structure(tf_results, profile):
    st.subheader("Price Structure")
    cols = st.columns([1, 1, 1])
    tf_labels = {"15m": "15-Minute", "1h": "1-Hour", "1d": "Daily"}

    for i, (tf, result) in enumerate(sorted(tf_results.items())):
        with cols[i % 3]:
            label = tf_labels.get(tf, tf)
            regime = result.get("regime", "Unknown")
            close = result.get("last_close", "—")
            trades = result.get("trades", [])
            direction = trades[0]["direction"] if trades else "NONE"

            regime_icon = {"BULLISH": "🟢", "BEARISH": "🔴", "NEUTRAL": "🟡", "": "⚪"}
            icon = regime_icon.get(regime.upper(), "⚪")

            st.markdown(f"**{label}** {icon}")
            st.markdown(f"Close: {close:,.2f}" if isinstance(close, (int, float)) else f"Close: {close}")
            st.markdown(f"Regime: **{regime}**" if regime else "Regime: Detecting")
            st.markdown(f"Signal: **{direction}**" if direction != "NONE" else "Signal: None")

            vol_ratio = profile.get("vol_ratio", 1.0)
            if tf == "15m" and isinstance(vol_ratio, (int, float)) and vol_ratio > 1.2:
                st.markdown("Volume: **Elevated**")


def show_smart_money_levels(profile):
    st.subheader("Smart Money Levels")
    cp = profile.get("current") or profile.get("today_close", 0)
    if not cp:
        st.info("Price data not available")
        return

    hi = profile.get("high", cp)
    lo = profile.get("low", cp)
    prev_hi = profile.get("prev_day_high")
    prev_lo = profile.get("prev_day_low")

    # Calculate support/resistance levels
    r1 = max(hi, prev_hi or hi)
    r2 = r1 * 1.02 if r1 else None
    s1 = lo
    s2 = s1 * 0.98 if s1 else None

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Resistance**")
        st.markdown(f"🟠 ₹{r1:,.2f}" if isinstance(r1, (int, float)) else "")
        if r2:
            st.markdown(f"🔴 ₹{r2:,.2f}")
    with col2:
        st.markdown("**Support**")
        st.markdown(f"🟢 ₹{s1:,.2f}" if isinstance(s1, (int, float)) else "")
        if s2:
            st.markdown(f"🟡 ₹{s2:,.2f}")


def show_trade_setup(name, symbol, tf_results, profile, sl_mult, tp_mult, atr_period_val, min_rr_val):
    st.subheader("Trade Setup")

    # Find the most actionable timeframe (15m priority, then 1h, then 1d)
    priority = ["15m", "1h", "1d"]
    best_tf = None
    best_trade = None

    for tf in priority:
        if tf in tf_results:
            trades = tf_results[tf].get("trades", [])
            if trades and trades[0]["direction"] in ("LONG", "SHORT"):
                best_tf = tf
                best_trade = trades[0]
                break

    if best_trade is None:
        st.info("No actionable trade signal generated.")
        return

    direction = best_trade["direction"]
    entry = best_trade["entry"]
    stop = best_trade["stop"]
    target = best_trade["target"]
    rr = best_trade["rr"]
    regime = tf_results.get(best_tf, {}).get("regime", "")

    # Determine holding period
    holding = {"15m": "Intraday", "1h": "1–3 Days", "1d": "1–4 Weeks"}
    holding_period = holding.get(best_tf, "Intraday")

    # R:R tiers
    rr_tier = "Strong" if rr and rr >= 2.0 else "Moderate" if rr and rr >= 1.0 else "Low"

    # Probability score (heuristic based on confluence factors)
    prob_score = 72
    if regime.upper() == "BULLISH":
        prob_score += 8
    vol_ratio = profile.get("vol_ratio", 1.0)
    if isinstance(vol_ratio, (int, float)) and vol_ratio > 1.2:
        prob_score += 5
    pos = profile.get("day_range_pct")
    if pos and pos >= 80:
        prob_score += 5
    prob_score = min(prob_score, 96)

    signal = "BUY" if direction == "LONG" else "SELL"

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**Stock:** {name}  \n**Signal:** 🟢 **{signal}**  \n**Timeframe:** {best_tf}")
        st.markdown("---")
        st.markdown(f"**Entry Zone:** ₹{entry:,.2f}" if isinstance(entry, (int, float)) else f"Entry: {entry}")
        st.markdown(f"**Stop Loss:** ₹{stop:,.2f}" if isinstance(stop, (int, float)) else "")
        st.markdown(f"**Targets:**")
        if isinstance(target, (int, float)) and isinstance(entry, (int, float)):
            t1 = target
            t2 = entry + (target - entry) * 1.5 if direction == "LONG" else entry - (entry - target) * 1.5
            t3 = entry + (target - entry) * 2.5 if direction == "LONG" else entry - (entry - target) * 2.5
            st.markdown(f"- T1: ₹{t1:,.2f}")
            st.markdown(f"- T2: ₹{t2:,.2f}")
            st.markdown(f"- T3: ₹{t3:,.2f}")

    with col2:
        st.markdown(f"**Ideal Holding Period:** {holding_period}")
        st.markdown(f"**Risk:Reward Ratio:** 1:{rr:.2f}" if isinstance(rr, (int, float)) else "R:R: N/A")
        st.markdown(f"**Probability Score:** {prob_score}%")
        st.markdown(f"**Best Timeframe:** {best_tf}")
        st.markdown(f"**Market Regime:** {regime}" if regime else "")

    # Rationale
    st.markdown("---")
    direction_word = "upside" if direction == "LONG" else "downside"
    reason_parts = []
    if regime:
        reason_parts.append(f"{regime} market regime detected")
    if isinstance(vol_ratio, (int, float)) and vol_ratio > 1.2:
        reason_parts.append("volume-backed momentum")
    if pos and pos >= 80:
        reason_parts.append("closing near session high — momentum remains positive")
    elif pos and pos <= 20:
        reason_parts.append("closing near session low — caution warranted")
    rationale = f"ICT structure favors {direction_word}. " + ". ".join(reason_parts) if reason_parts else f"ICT structure favors {direction_word}."
    st.markdown(f"**Rationale:** {rationale}")


def show_parameters(sl_mult, tp_mult, atr_period_val, min_rr_val, tf_results):
    st.subheader("Parameters")
    cols = st.columns(4)
    with cols[0]:
        st.metric("Stop Loss Multiplier", f"{sl_mult:.1f}x ATR")
    with cols[1]:
        st.metric("Take Profit Multiplier", f"{tp_mult:.1f}x ATR")
    with cols[2]:
        st.metric("ATR Period", atr_period_val)
    with cols[3]:
        active_tfs = [tf for tf in sorted(tf_results.keys())]
        st.metric("Timeframes", ", ".join(active_tfs))


def show_strategy_info(day_type_info: dict, stock_type_info: dict, strategy_info: dict):
    st.subheader("Strategy Selector")

    dt = day_type_info.get("type", "Unknown") if day_type_info else "Unknown"
    dt_strength = day_type_info.get("strength", "") if day_type_info else ""
    st_type = stock_type_info.get("type", "Unknown") if stock_type_info else "Unknown"
    st_strength = stock_type_info.get("strength", 0) if stock_type_info else 0

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Market Day:** {dt} (strength: {dt_strength})")
        if day_type_info:
            m = day_type_info.get("metrics", {})
            if m:
                for k in ("change_pct", "vwap_distance_pct", "vwap_slope_direction", "bull_ratio", "sector_breadth_pct"):
                    v = m.get(k)
                    if v is not None:
                        st.caption(f"{k}: {v}")

    with col2:
        st.markdown(f"**Stock Type:** {st_type} (strength: {st_strength})")
        if stock_type_info:
            for k in ("relative_return_pct", "above_vwap", "vol_ratio", "near_20d_high", "bullish_ratio"):
                v = stock_type_info.get(k)
                if v is not None:
                    st.caption(f"{k}: {v}")

    if strategy_info:
        name = strategy_info.get("strategy_name", "Unknown")
        cat = strategy_info.get("strategy_category", "")
        conf = strategy_info.get("confidence", "UNKNOWN")
        rationale = strategy_info.get("rationale", "")
        tuning = strategy_info.get("tuning", {})
        core = strategy_info.get("core_concepts", [])

        st.markdown(f"**Recommended Strategy: {name}** ({cat}) — Confidence: {conf}")
        if rationale:
            st.markdown(f"*{rationale}*")
        if tuning:
            tuning_str = "; ".join(f"{k}={v}" for k, v in tuning.items())
            st.caption(f"Tuning: {tuning_str}")
        if core:
            st.caption(f"Core concepts: {', '.join(core[:3])}")


def show_what_to_avoid(profile, tf_results):
    st.subheader("What I Would Avoid")
    direction = None
    for tf in ["15m", "1h", "1d"]:
        if tf in tf_results:
            trades = tf_results[tf].get("trades", [])
            if trades:
                direction = trades[0]["direction"]
                break

    cp = profile.get("current") or 0
    hi = profile.get("high", 0)
    lo = profile.get("low", 0)

    if direction == "LONG":
        st.markdown(f"❌ Fresh shorting — strong bid support visible.")
        st.markdown(f"❌ Chasing if price opens gap-up above ₹{hi:,.0f} without consolidation — wait for pullback.")
        st.markdown(f"❌ Assuming a single red candle invalidates the bullish structure — let it develop.")
    elif direction == "SHORT":
        st.markdown(f"❌ Fresh buying at current levels — distribution visible.")
        st.markdown(f"❌ Averaging down if price breaks below ₹{lo:,.0f}.")
    else:
        st.markdown("❌ No clear directional bias — avoid forced entries.")


def show_hedge_fund_view(name, symbol, tf_results, profile, prob_score_val):
    st.subheader("Hedge Fund View")
    direction = "BUY"
    direction_word = "bullish"
    for tf in ["15m", "1h", "1d"]:
        if tf in tf_results:
            trades = tf_results[tf].get("trades", [])
            if trades and trades[0]["direction"] == "SHORT":
                direction = "SELL"
                direction_word = "bearish"
                break

    regime = ""
    for tf in ["15m", "1h", "1d"]:
        if tf in tf_results and tf_results[tf].get("regime"):
            regime = tf_results[tf]["regime"]
            break

    vol_note = ""
    vr = profile.get("vol_ratio", 1.0)
    if isinstance(vr, (int, float)) and vr > 1.2:
        vol_note = f", volume at {vr:.2f}x average suggests institutional participation"

    st.markdown(f"**Current Rating:** {direction}")
    st.markdown(f"{name} is showing a {direction_word} ICT structure"
                f"{' with ' + regime + ' regime' if regime else ''}"
                f"{vol_note}. Probability favors continuation of the current bias"
                f" with a {prob_score_val}% confidence score.")


# ── Helpers ───────────────────────────────────────────────────────

def _compute_probability(tf_results: dict, profile: dict) -> int:
    prob = 72
    for tf in ["15m", "1h", "1d"]:
        if tf in tf_results:
            r = tf_results[tf].get("regime", "")
            trades = tf_results[tf].get("trades", [])
            if r:
                pass
            if trades and trades[0]["direction"] in ("LONG", "SHORT"):
                prob += 8
                break
    vr = profile.get("vol_ratio", 1.0)
    if isinstance(vr, (int, float)) and vr > 1.2:
        prob += 5
    pos = profile.get("day_range_pct")
    if pos and pos >= 80:
        prob += 5
    return min(prob, 96)


def _get_best_trade(tf_results: dict) -> tuple:
    for tf in ["15m", "1h", "1d"]:
        if tf in tf_results:
            trades = tf_results[tf].get("trades", [])
            if trades and trades[0]["direction"] in ("LONG", "SHORT"):
                return tf, trades[0]
    return None, None


def _render_compact_card(pos, name, sym, trade_summary, prob, day_type, stock_type, strategy):
    signal, entry, stop, target, rr = trade_summary
    signal_icon = {"BUY": "🟢", "SELL": "🔴", "NONE": "⚪"}.get(signal, "⚪")

    st.markdown(
        f"**#{pos}** {signal_icon} **{name}** ({sym.split('.')[0]})  \n"
        f"*Day:* {day_type}  *Stock:* {stock_type}  *Strategy:* {strategy}"
    )
    st.markdown("---")
    cols = st.columns([1, 1, 1])
    with cols[0]:
        bg = "#d4edda" if signal == "BUY" else "#f8d7da" if signal == "SELL" else "transparent"
        fg = "#155724" if signal == "BUY" else "#721c24" if signal == "SELL" else "inherit"
        st.markdown(
            f'<span style="background:{bg};color:{fg};padding:2px 8px;border-radius:4px;font-weight:bold">{signal}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Prob:** {prob}%" if prob else "")
    with cols[1]:
        if entry:
            st.markdown(f"**Entry:** ₹{entry:,.2f}" if isinstance(entry, (int, float)) else f"**Entry:** {entry}")
        if stop:
            st.markdown(f"**Stop:** ₹{stop:,.2f}" if isinstance(stop, (int, float)) else "")
    with cols[2]:
        if target:
            st.markdown(f"**Target:** ₹{target:,.2f}" if isinstance(target, (int, float)) else "")
        if rr:
            st.markdown(f"**R:R:** 1:{rr:.2f}" if isinstance(rr, (int, float)) else "")


def _render_chart(symbol, name, best_trade, best_tf, provider_type):
    df = service.get_chart_data(symbol, best_tf or "15m", 100, provider_type)
    if df is None or df.empty:
        st.caption("Chart data not available")
        return

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
    )

    fig.add_trace(go.Candlestick(
        x=df["timestamp"],
        open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        name="OHLC",
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444",
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df["timestamp"], y=df["volume"],
        name="Volume", marker_color="#64748b", opacity=0.5,
    ), row=2, col=1)

    if best_trade:
        direction = best_trade.get("direction", "")
        entry = best_trade.get("entry")
        stop = best_trade.get("stop")
        target = best_trade.get("target")

        color = "#22c55e" if direction == "LONG" else "#ef4444"

        if entry:
            fig.add_hline(y=entry, line_color=color, line_dash="dash", annotation_text=f"Entry ₹{entry:,.0f}", row=1, col=1)
        if stop:
            fig.add_hline(y=stop, line_color="#f97316", line_dash="dot", annotation_text=f"Stop ₹{stop:,.0f}", row=1, col=1)
        if target:
            fig.add_hline(y=target, line_color="#a855f7", line_dash="dot", annotation_text=f"Target ₹{target:,.0f}", row=1, col=1)

    fig.update_layout(
        title=f"{name} — {best_tf or '15m'} Chart",
        xaxis_title="Time", yaxis_title="Price",
        template="plotly_dark", height=500, margin=dict(l=40, r=20, t=40, b=20),
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
    )
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)


# ── Main Logic ────────────────────────────────────────────────────

if analyze_btn and selected:
    st.session_state.results = {}
    progress_bar = st.progress(0, text="Initializing...")
    status_text = st.empty()

    all_results = {}
    total = len(selected)

    for idx, sym in enumerate(selected):
        entry = next((s for s in filtered if s[0] == sym), None)
        if not entry:
            continue
        _, name, provider_type, _ = entry

        status_text.text(f"Analyzing {name} ({idx + 1}/{total})...")
        progress_bar.progress((idx) / total)

        result = run_analysis(sym, name, provider_type)
        all_results[sym] = result

    progress_bar.progress(1.0)
    status_text.text("Analysis complete!")
    st.session_state.results = all_results

    if not all_results:
        st.warning("No results. Stocks might be delisted or data unavailable.")
    else:
        st.success(f"Analysis complete for {len(all_results)} symbols across {len(TIMEFRAMES)} timeframes each.")

# ── Display Results ───────────────────────────────────────────────

if st.session_state.results:
    st.divider()

    # Build a sorted list by probability (highest first)
    summaries = []
    for sym, result in st.session_state.results.items():
        entry = next((s for s in filtered if s[0] == sym), None)
        name = entry[1] if entry else sym
        provider_type = entry[2] if entry else "yfinance"
        profile = result.get("profile", {})
        history = result.get("history", {})
        tf_results = result.get("timeframes", {})

        prob = _compute_probability(tf_results, profile)
        best_tf, best_trade = _get_best_trade(tf_results)
        direction = (best_trade or {}).get("direction", "")
        signal = "BUY" if direction == "LONG" else "SELL" if direction == "SHORT" else "NONE"
        trade_summary = (
            signal,
            (best_trade or {}).get("entry"),
            (best_trade or {}).get("stop"),
            (best_trade or {}).get("target"),
            (best_trade or {}).get("rr"),
        )

        day_type = (result.get("day_type") or {}).get("type", "—")
        stock_type = (result.get("stock_type") or {}).get("type", "—")
        strategy_name = (result.get("strategy") or {}).get("strategy_name", "—")

        summaries.append({
            "sym": sym, "name": name, "entry": entry,
            "profile": profile, "history": history,
            "tf_results": tf_results,
            "prob": prob, "signal": signal,
            "best_tf": best_tf, "best_trade": best_trade,
            "trade_summary": trade_summary,
            "day_type": day_type, "stock_type": stock_type,
            "strategy_name": strategy_name,
            "result": result,
        })

    summaries.sort(key=lambda x: x["prob"], reverse=True)

    # ── Top 10 Table ───────────────────────────────────────────
    st.subheader("Top 10 Trade Setups")
    table_rows = []
    for rank, s in enumerate(summaries[:10], 1):
        bt = s["best_trade"] or {}
        direction = bt.get("direction", "")
        entry = bt.get("entry")
        stop = bt.get("stop")
        target = bt.get("target")
        rr = bt.get("rr")
        signal = "BUY" if direction == "LONG" else "SELL" if direction == "SHORT" else "—"
        t2 = None
        if isinstance(entry, (int, float)) and isinstance(target, (int, float)):
            t2 = entry + (target - entry) * 1.5 if direction == "LONG" else entry - (entry - target) * 1.5
        table_rows.append({
            "#": rank,
            "Symbol": s["name"].split(".")[0],
            "Signal": signal,
            "Entry": f"₹{entry:,.2f}" if isinstance(entry, (int, float)) else "—",
            "Stop": f"₹{stop:,.2f}" if isinstance(stop, (int, float)) else "—",
            "T1": f"₹{target:,.2f}" if isinstance(target, (int, float)) else "—",
            "T2": f"₹{t2:,.2f}" if isinstance(t2, (int, float)) else "—",
            "R:R": f"1:{rr:.2f}" if isinstance(rr, (int, float)) else "—",
            "Prob": f"{s['prob']}%",
        })
    if table_rows:
        df = pd.DataFrame(table_rows)
        styled = df.style.map(
            lambda v: "background-color: #d4edda; color: #155724" if v == "BUY"
            else "background-color: #f8d7da; color: #721c24" if v == "SELL"
            else "",
            subset=["Signal"],
        )
        st.dataframe(styled, hide_index=True, use_container_width=True)
    st.divider()

    # Compact grid: 2 cols x up to 8 rows
    st.subheader(f"Top Setups by Probability")
    display_count = min(len(summaries), 8)

    for i in range(0, display_count, 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx >= display_count:
                continue
            s = summaries[idx]
            with cols[j]:
                with st.container(border=True):
                    _render_compact_card(
                        idx + 1, s["name"], s["sym"],
                        s["trade_summary"], s["prob"],
                        s["day_type"], s["stock_type"],
                        s["strategy_name"],
                    )

                    # Expander for full detail + chart
                    with st.expander(f"📊 Full Analysis & Chart"):
                        _render_chart(
                            s["sym"], s["name"],
                            s["best_trade"], s["best_tf"],
                            s["entry"][2] if s["entry"] else "yfinance",
                        )

                        show_stock_analysis(
                            s["name"], s["sym"],
                            s["profile"], s["history"],
                            s["tf_results"],
                        )
                        show_price_structure(s["tf_results"], s["profile"])
                        show_smart_money_levels(s["profile"])
                        show_trade_setup(
                            s["name"], s["sym"],
                            s["tf_results"], s["profile"],
                            sl_mult, tp_mult, atr_period, min_rr,
                        )
                        show_parameters(sl_mult, tp_mult, atr_period, min_rr, s["tf_results"])
                        show_strategy_info(
                            s["result"].get("day_type"),
                            s["result"].get("stock_type"),
                            s["result"].get("strategy"),
                        )
                        show_what_to_avoid(s["profile"], s["tf_results"])
                        show_hedge_fund_view(
                            s["name"], s["sym"],
                            s["tf_results"], s["profile"],
                            s["prob"],
                        )

    # If more than 8 were analyzed, show count
    remaining = len(summaries) - display_count
    if remaining > 0:
        st.caption(f"+ {remaining} more setups analyzed (not shown). Select fewer stocks or run again.")

    # ── Market Bias at bottom ──────────────────────────────────
    st.divider()
    market_ctx = service.get_market_context()
    show_market_bias(market_ctx)

elif not analyze_btn:
    st.info("👈 Select stocks from the sidebar and click **Run Analysis** to generate trade recommendations.")
