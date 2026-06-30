# Institutional Trading AI

Version: 2.1.0

Status: Active Development

---

# Vision

Build an institutional-grade trading research platform capable of identifying
high-probability trading opportunities using objective, testable and
backtestable trading rules.

This project is designed for personal trading with long-term profitability
as the primary objective.

---

# Project Goals

Primary Goals

- Maximize expectancy
- Improve trade quality
- Reduce false signals
- Reduce drawdown
- Maintain disciplined risk management

Secondary Goals

- Modular architecture
- Easy strategy optimization
- Easy backtesting
- Professional codebase

---

# Development Philosophy

Every feature must satisfy:

✓ Logical

✓ Objective

✓ Programmable

✓ Testable

✓ Measurable

If a feature cannot improve trading quality or be measured,
it will not be implemented.

---

# Development Cycle

Research

↓

Design

↓

Implement

↓

Backtest

↓

Measure

↓

Accept / Reject

No feature is accepted without validation.

---

# Architecture

app.py

↓

Dashboard

↓

DashboardService

↓

AnalysisService

↓

------------------------------------

Data Layer

DataEngine

IndicatorEngine

MarketStructure

SMCEngine

LiquidityEngine

PremiumDiscountEngine

OrderBlockEngine

FVGEngine

------------------------------------

Decision Layer

ProbabilityEngine

ConfluenceEngine

SignalEngine

RiskEngine

RatingEngine

------------------------------------

Scanner

ScannerEngine

---

# Engine Responsibilities

## DataEngine

Responsible for

- Downloading market data
- Cleaning data
- Returning OHLCV dataframe

Never performs analysis.

---

## IndicatorEngine

Responsible for

- EMA
- RSI
- MACD
- ATR

Never generates trading decisions.

---

## MarketStructure

Responsible for

- Swing High
- Swing Low
- HH HL LH LL
- BOS
- CHOCH
- Trend State
- Market State

Never generates BUY or SELL signals.

---

## LiquidityEngine

Responsible for

- Buy Side Liquidity
- Sell Side Liquidity
- Liquidity Sweeps

---

## PremiumDiscountEngine

Responsible for

- Premium Zone
- Discount Zone
- Equilibrium

---

## OrderBlockEngine

Responsible for

- Bullish Order Blocks
- Bearish Order Blocks

---

## FVGEngine

Responsible for

- Bullish FVG
- Bearish FVG

---

## ProbabilityEngine

Responsible for

Estimating probability using market evidence.

Does NOT generate BUY or SELL signals.

---

## ConfluenceEngine

Responsible for

Combining institutional evidence into one score.

---

## SignalEngine

Responsible for

Final trade validation.

Produces

- STRONG BUY
- BUY
- WATCH
- NO TRADE

---

## RiskEngine

Responsible for

- Entry
- Stop Loss
- Targets
- Risk Reward

Never generates BUY or SELL.

---

## RatingEngine

Responsible for

Converting technical results into a user-friendly rating.

---

## ScannerEngine

Responsible for

Ranking stocks.

---

# Coding Standards

One engine

=

One responsibility

One file

=

One engine

No duplicated logic.

No circular imports.

No magic numbers.

Configuration belongs inside

config/trading_config.py

---

# Market Structure Specification

Future Version

Market Structure will include

- Dynamic Swings
- Swing Strength
- Trend State
- Market State
- Institutional BOS
- Institutional CHOCH

---

# Version Roadmap

## Version 2.1

✓ Modular Architecture

✓ Dashboard

✓ Scanner

✓ Components

✓ Configuration System

✓ Probability V2

---

## Version 2.2

Institutional Market Structure

---

## Version 2.3

Order Blocks V2

Liquidity V2

Fair Value Gap V2

---

## Version 2.4

Probability V3

Signal V2

Scanner V2

---

## Version 2.5

Backtesting

Strategy Optimization

Performance Analytics

---

## Version 3

Portfolio

Paper Trading

Alerts

Broker Integration

Automation

---

# Project Rules

Rule 1

Never sacrifice architecture for speed.

Rule 2

Every improvement must improve at least one

- Win Rate
- Profit Factor
- Expectancy
- Drawdown

Rule 3

No feature is added because it looks impressive.

Rule 4

Every strategy improvement must be measurable.

Rule 5

Backtesting precedes live trading.

Rule 6

Paper trading precedes broker integration.

Rule 7

Long-term profitability is more important than trade frequency.

Rule 8

Shared calculations belong in utils/.

Never duplicate mathematical logic across engines.

---

# Success Definition

This project is considered successful when it can

- Identify high-quality institutional trade setups
- Reject poor-quality trades
- Produce consistent positive expectancy
- Be validated through backtesting
- Be reliable enough for paper trading
- Eventually support disciplined live trading

---

END OF DOCUMENT
