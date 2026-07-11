# Institutional Probability v1

8-factor scoring engine (0–100) for NSE equity intraday/swing trading.

## Files

| File | Description |
|------|-------------|
| `config.json` | Factor weights, tuning, multi-TF settings, backtest results |
| `engine.py` | `InstitutionalProbabilityEngine` — 8-factor scoring |
| `strategy.py` | `InstitutionalStrategy` — ExecutableStrategy wrapper |
| `requirements.txt` | Python dependencies |

## Factors

| # | Factor | Weight | Description |
|---|--------|--------|-------------|
| 1 | Market Regime | 15 | NIFTY EMA alignment, HH/HL, breadth, 1d HTF bonus |
| 2 | Sector Strength | 15 | Relative performance vs NIFTY, volume ratio |
| 3 | Price Action | 20 | HH/HL structure, resistance break, support quality |
| 4 | Volume | 15 | RVOL tiers (3x/1.5x/1x) |
| 5 | Breakout Quality | 15 | Resistance break, close above, volume confirm, retest, market alignment, 30m HTF bonus |
| 6 | Risk/Reward | 10 | ATR-based RR ratio tiers |
| 7 | Indicators | 5 | EMA alignment, RSI zone, MACD, VWAP |
| 8 | Catalyst | 5 | Accumulation, dips absorbed |

## Usage

```python
from engines.institutional_probability_engine import InstitutionalProbabilityEngine

engine = InstitutionalProbabilityEngine(sl_mult=0.5, tp_mult=5.0)
result = engine.compute(df, nifty_df=nifty, day_type=day_type, stock_type=stock_type)
score = result["total_score"]  # 0-100
# score >= 70 → LONG
# score <= 35 → SHORT
```

## Tuned Parameters

```
sl_mult=0.5, tp_mult=5.0, atr_period=14
score_threshold=70, short_threshold=35
multi-TF bonus: +1 for 1d trend (market regime), +1 for 30m trend (breakout quality)
```

## Backtest Results (30 NSE Symbols, 15m, Jun–Jul 2026)

| Mode | Trades | WR | PF | PnL% | MaxDD |
|------|--------|----|----|------|-------|
| Intraday | 70 | 24.3% | 2.30 | +3.09% | 0.18% |
| Swing | 111 | 20.7% | — | — | — |

## Limitations

- LOW WIN RATE (~24%) — tight SL exits on noise; wide 5×ATR TP compensates
- LONG-only bias; SHORT logic added but untuned
- Best on 15m; 1m/1h/1d have data constraints
- Tuned on 1 month only — needs out-of-sample validation
