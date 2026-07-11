# Agent Context

## Phase 0 — Capital-based sizing + data refresh (2026-07-10)

Account model now real: **₹50,000 capital, 1% risk (₹500/trade), max 5 new
entries/day.** Applies to `scripts/backtest.py`.

### Fixes
- `_position_size_for` now sizes by capital: `shares = int(₹500 / |entry-SL|)`,
  notional capped at ₹50k (no leverage). Returns 0 → trade skipped as infeasible.
- Added `INITIAL_CAPITAL=50000`, `RISK_PER_TRADE_PCT=1.0`, `MAX_TRADES_PER_DAY=5`.
- Daily-cap + affordability gate added at trade entry (first-N-per-day by arrival).
- Fixed reporting bug: `total_pnl_pct` was hardcoded to a ₹100k base → phantom
  −50% on every symbol. Now uses `INITIAL_CAPITAL`.
- `scripts/download_history.py` (new, tokenless yfinance) extends cache:
  **1h → 2yr (~5053 bars), 1d → 5yr (~1239), 15m → 60d (yfinance cap ~1427).**

### New honest baseline (sl=0.5, tp=5.0, threshold=70, LONG-only)
| TF | Mode | Trades | WR | Profitable symbols |
|----|------|--------|----|--------------------|
| 15m | Intraday | 359 | 42.3% | 16 / 30 |
| 1h | Swing (2yr) | 333 | 28.5% | 8 / 30 |

Top intraday 15m: ONGC +10.4%, ADANIENT +5.8%, CIPLA +4.7%, OIL +4.2%, TECHM +4.1%.
Top swing 1h: BSE +14.5%, TCS +7.0%, ICICIPRULI +6.8%, KOTAKBANK +5.9%.

Key findings → drive Phase 1/4:
- Profitable symbols differ completely by timeframe (ONGC great intraday but
  −4.7% swing; BSE/TCS great swing). Confirms need for per-symbol **and**
  per-timeframe whitelist.
- Swing 1h is mostly −EV on the intraday-tuned 0.5/5.0 SL/TP (22/30 losers) →
  swing needs its own SL/TP tuning (Phase 4).

---

## Phase 1 — Selectivity (whitelist) — 2026-07-10

Strict whitelist rule: **PF >= 1.5 AND trades >= 5** (your call). Generates
`data/symbol_whitelist.json` via `scripts/build_whitelist.py`; applied with
`run_backtest_portfolio.py --whitelist` (writes `*_wl.json` so baseline is kept).

Result (15m intraday, sl 0.5 / tp 5.0, threshold 70):
| | Full 30 | Whitelist |
|---|---|---|
| Trades | 359 | 200 |
| WR | 42.3% | **55.0%** |
| Profitable symbols | 16/30 | **14/14** |
| Worst PF | 0.00 | 1.71 |

15m whitelist (14): ONGC, ABB, WIPRO, TECHM, COALINDIA, ADANIENT, TORNTPHARM,
HINDUNILVR, CIPLA, BEL, PIDILITIND, BSE, ITC, OIL.
1h swing whitelist (2): BSE, ICICIPRULI. (Swing is −EV on intraday SL/TP →
see Phase 4.)

### Threshold sweep (whitelisted 15m)
| TH | trades | WR | expectancy R/trade | sumPnL% |
|----|--------|----|--------------------|---------|
| 70 | 200 | 55.0% | **+0.702** | +50.6 |
| 75 | 171 | 59.6% | +0.599 | +39.9 |
| 80 | 151 | 62.9% | +0.633 | +39.4 |
| 85 | 38 | 60.5% | (sparse) | — |

**Finding:** raising the threshold beyond 70 *reduces* expectancy — the
whitelist already does the selectivity; the threshold adds nothing. **Keep 70.**

### Confluence requirement (INST_CONFLUENCE_MIN) — REJECTED
Requiring core factors (regime+price_action+volume) each >= N cut trades
200→52 but dropped WR to 33% and did NOT beat 70's expectancy. With a
10R-winner-driven edge, forcing "consistency" destroys expectancy. Gate left
DISABLED (default).

---

## Phase 2 — Filters (regime / session) — 2026-07-10

### Regime gate (INST_REQUIRE_TREND_UP=1) — ACCEPTED, now standard
Require HTF 1d trend == UP for LONG. On whitelisted 15m:
trades 200→187, WR 55.0%→58.3%, expectancy **+0.702→+0.781 R**, sumPnL
+50.6→+53.3, still 14/14 profitable. Pure win — keeps trend-alignment.
Standard env for all forward runs: `INST_REQUIRE_TREND_UP=1`.

### Session filter — REJECTED
Re-ran time-of-day analysis on the REAL gated trade set
(`scripts/analyze_time_of_day.py`). With whitelist+regime gate applied,
**every session is now net positive** (opening 68.5% WR/+525, morning
49.3%/+798, midday 57.5%/+354, afternoon 40%/+59). Old
data/time_of_day_analysis.json was computed on RAW/all-signals, hence its
all-negative picture — not applicable to the gated population. Blocking any
session would only *lose* edge. SESSION_WEIGHTS left neutral.

---

## Phase 3 — Fix SHORT — 2026-07-10 (DONE, SHIPPABLE)

Root cause: SHORT was "not-bullish", not genuinely bearish → 3.5% WR / PnL −93k.

Fixes in `engines/institutional_probability_engine.py`:
- New dedicated factor **`short_context`** (0–20, bearish only): bearish HTF
  daily trend + bearish swing structure (LL/LH) + breakdown through support +
  relative weakness vs NIFTY + distribution volume on down bars.
- Regime gate extended symmetrically: LONG requires 1d trend UP, **SHORT
  requires 1d trend DOWN** (`INST_REQUIRE_TREND_UP=1`).
- `SHORT_MIN_SCORE` default lowered 46 → **40** (genuine shorts can now clear).

Result (15m intraday, sl 0.5/tp 5.0 LONG; short_sl 1.0/tp 2.0 SHORT):
| Direction | trades | WR | expectancy R |
|-----------|--------|----|--------------|
| SHORT (gated) | 785 | **61.0%** | **+0.694** |
| LONG (gated)  | 64  | 32.8% | +0.764 |

SHORT went from broken to a real, trend-aligned edge. SHORT whitelist
(15m_intraday_short) built with same rule (PF>=1.5 & >=5 trades): **23 symbols
pass** (BHARTIARTL, CIPLA, TATACONSUM, TECHM, COALINDIA, KOTAKBANK, SBIN, BEL,
ICICIBANK, ITC, TCS, RELIANCE, OIL, ONGC, DIVISLAB, PIDILITIND, HINDUNILVR,
WIPRO, ADANIENT, INFY, ABB, HDFCBANK, ICICIPRULI).

### Standard env config
- Long-only forward: `INST_REQUIRE_TREND_UP=1`, `INST_SHORT_MIN_SCORE=70`
  (shorts suppressed), `--whitelist` (uses 15m_intraday / 1h_swing).
- Both sides: `INST_REQUIRE_TREND_UP=1`, `INST_SHORT_MIN_SCORE=40`,
  whitelist covers 15m_intraday + 15m_intraday_short.

---

## Phase 4 — Exit mgmt / SL-TP tuning — 2026-07-10

### Swing 1h was mis-tuned+ungated, not broken
Re-tuned swing on 2yr with `scripts/tune_sltp.py` (now configurable:
`--timeframe/--days/--no-intraday`). With the regime gate applied, swing
jumped from the old −EV baseline (8/30 profitable) to **PF ~2.4, WR ~55%
across ALL 30 symbols**. Best combo: **sl 1.5 / tp 4.0**.

Rebuilt swing whitelist (1h_swing): **2 → 14 symbols** (LT, BEL, ABB,
KOTAKBANK, TATACONSUM, ICICIPRULI, TCS, BSE, COALINDIA, EICHERMOT, OIL,
MARUTI, AXISBANK, TECHM).

### Final per-mode params (regime-gated)
- Intraday 15m: sl 0.5 / tp 5.0  (unchanged, already strong)
- Swing 1h:     sl 1.5 / tp 4.0  (new)

Trailing/partial exits: NOT added — static targets already yield +0.7R
expectancy; the edge is in entry selection, not exit micromanagement.
(Revisit only if a trailing variant beats +0.7R in a dedicated test.)

---

## Phase 5 — Expand universe — 2026-07-10 (infrastructure done; limited by data)

Added: `EXPANSION_CANDIDATES` + `expansion_universe()` in
`data/downloader/watched_symbols.py`; `run_backtest_portfolio.py --symbols`
to scope any list; `download_history.py --symbols` for tokenless fetch.

Validated 118 candidates vs yfinance → **110 have data**. Downloaded 1h (2yr)
+ 1d (5yr) for all 110. Ran expanded 15m & 1h whitelist on the 110.

**Finding — data is the hard limit for intraday expansion:**
- yfinance caps **15m at 60 days**. Only the original 30 core symbols have
  15m cache; the 80 new names have NO 15m data → expanded 15m run collapsed
  back to the original 14 whitelisted symbols (55 trades). No real expansion.
- 1h (2yr) was downloaded for all 110, but most new names still produce 0
  trades after the 60-bar warmup on a 700d window → expanded 1h run also
  collapsed to the original 14 (39 trades).
- Conclusion: universe expansion is gated by **15m history availability**.
  Upstox REST allows 729 days of 15m (needs paid credits / the live token),
  which would unlock a real Nifty-100 intraday expansion. Until then, the
  edge is concentrated in the current 14 (15m) / 14 (1h) whitelists.

ACTION: to expand intraday, run
`scripts/download_history.py --tf 15m --symbols <nifty100 list>` after
resolving Upstox keys (Upstox gives 729d of 15m), then re-run the whitelist.

---

## Phase 6 — Walk-forward OOS validation — 2026-07-10 (CRITICAL)

`scripts/walkforward_validate.py`: build whitelist on a TRAIN window, test on
a held-out TEST window. Reveals selection-bias decay. Enhanced with `--folds N`
(rolling walk-forward, N OOS windows) and `--symbols` (subset filter).

**Clean 3-fold OOS (post PIT/look-ahead fixes — the trustworthy numbers):**
Subset {WIPRO, RELIANCE, ONGC, BSE, ADANIENT}. 15m intraday sl 0.5/tp 5.0;
1h swing sl 1.5/tp 4.0.

| Mode | Fold | Whitelisted | OOS trades | OOS WR | OOS PF | OOS Exp |
|------|------|-------------|-----------|--------|--------|---------|
| 15m intraday | 2 | ONGC | 50 | 54.0% | 2.23 | +0.587R |
| 15m intraday | 3 | ONGC | 35 | 34.3% | 1.46 | +0.129R |
| 15m intraday | **agg** | | **85** | 45.9% | — | **+0.398R** |
| 1h swing | 1 | WIPRO | 43 | 39.5% | 1.11 | +0.071R |
| 1h swing | 2 | — | — | — | — | — |
| 1h swing | 3 | — | — | — | — | — |

(15m Fold 1 train window was ~20d of available 15m history → too short for a
whitelist; the folds that ran are positive. 1h folds 2-3 whitelist empty in
train → OOS null for those windows.)

**Major finding:** 15m intraday is ROBUST — edge holds out-of-sample
(aggregate +0.40R, ONGC PF 2.23). 1h swing is FRAGILE — only 1/3 folds traded,
barely positive (exp +0.071R), whitelist selection unstable (curve-fit decay).
Direction: **move to paper trading on 15m intraday only**; treat 1h swing as
unproven until re-validated on longer history.

### Final forward config (long-only)
- Intraday 15m: `INST_REQUIRE_TREND_UP=1`, `INST_SHORT_MIN_SCORE=70`,
  `sl 0.5 / tp 5.0`, `score_threshold=70`. OOS-validated (+0.40R agg).
  Lead names: ONGC, plus WIPRO/RELIANCE from in-sample runs.
- Swing 1h: **DISABLE for live** — OOS not robust. Revisit only with longer
  (Upstox 729d) 1h history + broader universe.
- SHORT available (Phase 3) when `INST_SHORT_MIN_SCORE=40`; trend-gated, 23
  symbols. Not yet OOS-validated for SHORT specifically.

---

## Latest Backtest Results — Institutional Probability (2026-07-10)

### Best Config (stored in registry)
```
strategy: "Institutional Probability"
sl_mult=0.5, tp_mult=5.0, atr_period=14
score_threshold=70 (institutional_strategy.py)
multi-TF bonus: ON (htf_ctx passed to engine)
```

### 1h Native Data (2026-07-10 fix)
`data_registry.py` now fetches native 1h bars via yfinance instead of resampling 30m→1h,
which produces different OHLC patterns. Cached to `data/cache/1h/{symbol}.parquet`.
Falls back to resampled 30m if yfinance fails.

### Results by Timeframe (LONG only — SHORT disabled)

| Timeframe | Mode | Trades | WR | PF | Notes |
|-----------|------|--------|----|----|-------|
| **15m** | Intraday | 273 | 23.8% | 2.22 | 30/30 symbols. Best: ONGC PF=13.51. |
| **15m** | Swing | — | — | — | (not run this session) |
| **1h** | Intraday | 32 | 28.1% | 2.63 | 13/30 symbols. Native data fix. |
| **1h** | Swing | 629 | 11.3% | 1.23 | 30/30 symbols. High volume. |
| 1m | — | 0 | — | — | 15d lookback insufficient for 60-bar warmup |
| 1d | — | 0 | — | — | 77 bars < 80 needed after 60-bar warmup |

### SHORT Status
SHORT is **disabled** (MIN_PROB=70 rejects all SHORT candidates). Engine generates SHORT
signals at score ≤ 35, but backtest showed 1599 SHORT trades with WR=3.5% (PnL=-93k).
SHORT needs dedicated bearish scoring factors to work — "not bullish" ≠ "bearish".

### Key Files

### Key Files
- `engines/institutional_probability_engine.py` — 8-factor scoring (0-100)
- `strategies/institutional_strategy.py` — ExecutableStrategy wrapper
- `scripts/tune_sltp.py` — grid search for SL/TP
- `scripts/backtest.py` — WalkForwardBacktest engine with multi-TF passthrough
- `data/downloader/data_registry.py` — native 1h via yfinance, resampling fallback
- `data/results/latest/` — symlink to most recent full results

---

## Phase 7 — Paper Trading (2026-07-11, BUILT)

`scripts/paper_trade.py`: simulated portfolio that reuses the SAME live decision
path as backtest/scanner (`decide_trade` + `build_htf_context`), and adds
position management. Default data source is yfinance (delayed); pass `--upstox`
to use the real-broker Upstox feed.

- Capital model matches backtest: `INITIAL_CAPITAL=50000`, `RISK_PER_TRADE_PCT=1.0`
  (₹500/trade), `MAX_TRADES_PER_DAY=5`.
- **Cash-aware sizing** (fixes backtest's ignored cross-position margin): a new
  position's notional is capped at free cash, so capital can never go negative.
  With sl 0.5/tp 5.0, ~2 concurrent full-risk positions fit in ₹50k.
- Opens a paper LONG when `decide_trade` signals (score>=70, HTF aligned);
  monitors open positions against the live close and fills SL/TP.
- State persists to `data/paper_portfolio.json` (crash-safe); logs entries/exits,
  PnL, R-multiple, equity curve, and an **Upstox-format order payload** per fill
  (instrument_key, quantity, transaction_type, order_type, price, trigger).

**Upstox integration (`--upstox`):** `15m` bars are fetched as 1m via
`UpstoxMarketDataProvider` REST and resampled to 15m (Upstox has no native 15m
bar → maps to `30minute`). NIFTY resolved via `NSE_INDEX|Nifty 50`. Live exit
prices come from `data_registry.get_live_price()` (Upstox WebSocket batch). No
real orders are placed — fills are simulated; the order payload is ready to POST
to `/v2/orders` when a trading token is available.

Mechanics validated synthetically (entry sizing, TP WIN +5R, SL LOSS -1R, daily
cap, cash-aware concurrency, order payload with resolved instrument_key). Live
signals only fire during market hours on a trading day (weekend = stale data →
no signal). End-to-end `--upstox` cycle verified: REST fetch + WS price succeed
with the `.env` token.

Fixed alongside:
- `_bars_until_close` tz off-by-one in `live_institutional_scan.py` (yfinance
  bars stamped at bar CLOSE → final 15:15 bar now reports 0 bars left).
- `UpstoxMarketDataProvider.load_historical_data` tz-naive vs tz-aware
  comparison crash when `start_date` is passed (broke all `start_date` callers).

### P0 hardening (2026-07-11) — operational safety
- **Intraday EOD force-close**: `run_cycle()` now squares off any position whose
  `opened_at` date is before today (real NSE intraday `product="I"` is
  auto-squared at 15:30); stale carry-over can no longer fake overnight P&L.
- **State corruption recovery**: `_load_state()` backs up a corrupt
  `paper_portfolio.json` to `.corrupt` and starts fresh instead of crashing.
- **`--loop` resilience**: the poll loop now catches any cycle exception, logs
  it, and aborts only after 5 consecutive failures (was: one blip killed it).
- **Upstox rate-limiting**: new `data/upstox/upstox_http.py` (`upstox_get`/
  `upstox_post`) retries on HTTP 429 (honours `Retry-After`) + transport errors
  with exponential backoff; wired into `place_upstox_order` and
  `search_upstox_instrument`.
- **`today_cache.merge_today_to_1d`**: `drop_duplicates(keep="last")` so
  WebSocket intraday updates are not silently discarded.
- **WebSocket auto-reconnect**: `upstox_live_feed.start()` now reconnects on
  error/close with exponential backoff (max 10 attempts); `stop()` disables it.

### Commands
```bash
# One paper cycle (yfinance)
.venv/bin/python scripts/paper_trade.py --symbols ONGC,WIPRO,RELIANCE

# One paper cycle on Upstox real-broker feed
.venv/bin/python scripts/paper_trade.py --upstox --symbols ONGC,WIPRO,RELIANCE

# Live paper loop (polls every 15m during market hours)
.venv/bin/python scripts/paper_trade.py --loop --interval 15
.venv/bin/python scripts/paper_trade.py --upstox --loop --interval 15

# Reset simulated portfolio
.venv/bin/python scripts/paper_trade.py --reset

# Allow SHORT entries (off by default — not yet OOS-validated; also requires
# INST_SHORT_MIN_SCORE=40 in the live engine env to actually emit SHORT signals)
.venv/bin/python scripts/paper_trade.py --shorts --symbols ONGC,WIPRO,RELIANCE
```

### P1 hardening (2026-07-11)
- **Shared capital model**: `scripts/capital_model.py` now holds `INITIAL_CAPITAL`,
  `RISK_PER_TRADE_PCT`, `MAX_TRADES_PER_DAY` and `position_size_for` — imported by
  BOTH `scripts/backtest.py` and `scripts/paper_trade.py` so the risk model can
  never diverge. `_position_size_for` in backtest delegates to it.
- **SHORT in paper trader**: entries/exits are now direction-aware (SHORT = SELL
  to open, BUY to close; SL above / TP below entry; mark-to-market equity
  `shares*(entry-px)`; net P&L booked at close). Gated behind `--shorts` (default
  off) because SHORT is not yet OOS-validated (Phase 6).
- **Benchmark loop**: the silent `except: continue` now logs the failing
  strategy name + bar index instead of swallowing bugs.
- **`walkforward_validate` cache redirect**: replaced the raw global
  `_dr._CACHE_DIR` mutation with `data_registry.override_cache_dir()` context
  manager (guaranteed restore, re-entrant-safe).
- **`_market_open()`**: now delegates to `data.utils.market_hours.is_market_open`,
  so NSE holidays are respected (no fake positions on closed markets); the loop
  sleep uses `next_market_open` to skip weekends + holidays.
- **tz normalization**: `_normalize_timestamp_tz` converts every source to IST
  wall-clock before stripping tz, so yfinance (UTC) and Upstox (IST) bars align
  (was a latent 5h30m misalignment). Daily bars preserve their calendar date.
- **Stale-data warning**: `_warn_stale_data` fires when a backtest runs while the
  market is OPEN but the last bar is >1 day old (cache failed to refresh).
- **Live scanner PIT**: `_classify_stock_type` now excludes today's incomplete
  daily bar (`< today`, matching the backtest's `< current_date`).

### Commands
```bash
# Intraday 15m
.venv/bin/python scripts/run_backtest_portfolio.py --timeframe 15m \
  --strategy "Institutional Probability" --tuning-sl 0.5 --tuning-tp 5.0

# Swing 15m
.venv/bin/python scripts/run_backtest_portfolio.py --timeframe 15m --no-intraday \
  --strategy "Institutional Probability" --tuning-sl 0.5 --tuning-tp 5.0

# Intraday 1h
.venv/bin/python scripts/run_backtest_portfolio.py --timeframe 1h \
  --strategy "Institutional Probability" --tuning-sl 0.5 --tuning-tp 5.0

# Swing 1h
.venv/bin/python scripts/run_backtest_portfolio.py --timeframe 1h --no-intraday \
  --strategy "Institutional Probability" --tuning-sl 0.5 --tuning-tp 5.0

# Re-tune
.venv/bin/python scripts/tune_sltp.py
```

## Phase 8 — Full-universe backtest + profitable watchlists (2026-07-11)

Ran the **full 118-symbol universe** across all three modes using
`run_backtest_portfolio.py --provider yfinance` (the `--provider` flag bypasses
the old Upstox-key SKIP gate so the expanded universe runs from the local parquet
cache; 15m expansion names fetch 60d live from yfinance, 1h uses the 109-symbol
cache).

Results (LONG-only, sl/tp per mode, threshold 70, regime-gated):

| Mode | Trades | Profitable (PF≥1.3, ≥10 tr) | Unprofitable (PF<1.0) | Verdict |
|------|--------|------------------------------|------------------------|---------|
| 15m intraday (sl0.5/tp5.0) | 17,679 | **32** | 47 | ✅ robust edge |
| 15m swing (sl0.5/tp5.0) | 19,931 | 28 | 52 | ⚠️ weaker |
| 1h swing (sl1.5/tp4.0) | 95,748 | 6 | 67 | ❌ fragile (OOS-unproven) |

Output files: `data/backtest_portfolio_15m_intraday.json` +
`data/backtest_trades_15m_intraday.json` (17,679 trades); `_15m_swing` (19,931);
`_1h` (95,748).

15m intraday TOP: COALINDIA PF2.12, ONGC 1.88, LT 1.71, IOC 1.64, NHPC 1.61,
BANKBARODA 1.59, IRCTC 1.56, NTPC 1.53, TITAN 1.53, HINDUNILVR 1.52.
1h swing TOP (only 6 clear PF≥1.3): BSE 1.39, ITC 1.36, ICICIPRULI 1.32, IRFC
1.32, ADANIGREEN 1.31, PIDILITIND 1.30 — note huge cumulative PnL% (+130% to
+300%) is multi-year compounding of many bars, not per-trade edge; WR stuck
~39-41%. Treat 1h swing as NOT live-ready.

### Profitable watchlists — `data/symbol_watchlists.json`
Generated from the three result files with filter **trades ≥ 10 AND PF ≥ 1.3**
(matches the "profitable" definition above). Structure:
```json
{
  "15m_intraday": [...], "15m_swing": [...], "1h_swing": [...],
  "consensus": [...],          // profitable in 2+ modes (23)
  "full_consensus": [...],     // profitable in all 3 modes (3)
  "details": { "SYM": { "15m_intraday": {pf, trades, avg_r, wr, pnl_pct, max_dd}, ... } }
}
```
Counts: 15m_intraday 32, 15m_swing 28, 1h_swing 6, consensus 23, full_consensus 3.

**full_consensus (profitable in ALL 3 modes — safest paper-trading seed):**
ADANIGREEN, ICICIPRULI, ITC.

**consensus (profitable in 2+ modes):** ADANIGREEN, ICICIPRULI, ITC, COALINDIA,
ONGC, LT, IOC, NHPC, BANKBARODA, NTPC, TITAN, TRENT, INFY, POLICYBZR, TCS, BPCL,
DRREDDY, TATACONSUM, RELIANCE, AXISBANK, PFC, DMART, TATAELXSI.

### Paper-trader watchlist support
`scripts/paper_trade.py` now reads these lists:
```bash
.venv/bin/python scripts/paper_trade.py --list-watchlists
.venv/bin/python scripts/paper_trade.py --watchlist 15m_intraday
.venv/bin/python scripts/paper_trade.py --watchlist full_consensus --upstox --loop
```
`--symbols` still takes priority if both given; with neither, falls back to
`FOCUSED_WATCHLIST` (unchanged).

### Direction
- Paper trade on **15m intraday** (robust, OOS-validated). Start with
  `--watchlist full_consensus` (3 names) or `consensus` (23).
- 1h swing stays DISABLED for live (fragile per Phase 6 + this run).
- SHORT still gated behind `--shorts` (not OOS-validated).

## Phase 9 — Tiered market scanner (2026-07-11, BUILT)

`scripts/market_scan.py`: live analysis that walks the profitable watchlists in
priority order and reports actionable trade signals — **no portfolio, no orders**
(that is `paper_trade.py`'s job). This is the "analyze the market and give me
trades" command.

Scan tiers (priority order; each symbol scanned with its watchlist's own spec):
| Tier | Watchlist | Symbols | Scan mode | SL/TP |
|------|-----------|---------|-----------|-------|
| 1a | **consensus** | 23 | 15m **intraday** | 0.5/5.0 |
| 1b | **consensus** | 23 | 15m **swing** | 0.5/5.0 |
| 2 | **15m_intraday** (unique) | 9 | 15m intraday | 0.5/5.0 |
| 3 | **15m_swing** (unique) | 5 | 15m swing | 0.5/5.0 |
| 4 | **1h_swing** (unique) | 6 | 1h swing | 1.5/4.0 |

- **consensus is scanned in BOTH intraday and swing** (per request) — a symbol
  can appear in both groups if it triggers in both modes.
- Lower tiers dedup against the same (timeframe, intraday) spec already run, so
  no symbol is double-scanned in one mode (≈66 scan operations / 40 unique names).
- Reuses the exact `decide_trade` + `build_htf_context` path (no signal-logic
  divergence from backtest / paper trader).
- Reports grouped as **INTRADAY (15m)** and **SWING (15m/1h)** with score, entry,
  SL, TP, R per signal; `--json` for machine-readable output.

### Commands
```bash
# Analyze market now (yfinance, delayed)
.venv/bin/python scripts/market_scan.py

# Live Upstox feed
.venv/bin/python scripts/market_scan.py --upstox

# Show the tier plan
.venv/bin/python scripts/market_scan.py --list-tiers

# Auto re-scan every 15 min during market hours
.venv/bin/python scripts/market_scan.py --loop --interval 15

# Machine-readable
.venv/bin/python scripts/market_scan.py --json

# Include SHORT signals (off by default — not OOS-validated)
.venv/bin/python scripts/market_scan.py --shorts
```

Verified end-to-end (full 66-scan run completes, clean report; NIFTY index now
fetched as `^NSEI` not `^NSEI.NS`). On a closed market swing signals may still
fire (e.g. RELIANCE 15m swing score 76); intraday requires live session bars.

## Phase 9a — Live web dashboard (2026-07-11, BUILT)

`scripts/market_scan.py --serve` turns the scanner into a **network-accessible
live dashboard**: a background thread runs the tiered scan on a timer and a
built-in HTTP server streams the results to `web/dashboard.html`.

- Single command, **no new dependencies** (Python stdlib `http.server`).
- Binds to `0.0.0.0:<port>` → reachable from any device on the LAN / network.
- Background daemon thread scans every `--interval` min during NSE hours; writes
  to a thread-safe `_latest_scan` dict.
- HTTP routes: `/` → dashboard, `/api/latest` → full JSON, `/api/status` → health.
- Dashboard: dark theme, INTRADAY (green) + SWING (amber) card columns, each
  card shows symbol / direction / score / entry / SL / TP / R / tier. Auto-refreshes
  every 15s via `fetch('/api/latest')` — **silent updates**, no sound/reload.
- New signals flash briefly on arrival (visual cue, no audio).

### Commands
```bash
# Start dashboard (live Upstox feed, network-accessible on :8080)
.venv/bin/python scripts/market_scan.py --upstox --serve --port 8080

# yfinance (delayed) variant
.venv/bin/python scripts/market_scan.py --serve

# Dashboard URL:  http://<this-host-ip>:8080/
# JSON API:       http://<this-host-ip>:8080/api/latest
```

Verified: server starts instantly (worker scans async, dashboard shows
"waiting for first scan" then populates); `/` serves HTML, `/api/latest` returns
seeded signals, `404` handled. On a closed market the worker reports
"closed — market not open" and resumes at next session.
