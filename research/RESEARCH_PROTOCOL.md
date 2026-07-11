# RESEARCH_PROTOCOL.md

# ==========================================================
# Institutional Trading AI
# Feature Research Protocol
# Version 1.0
# ==========================================================

## Purpose

This document defines the official methodology for validating every
deterministic feature computed by the Feature Engine.

The objective is to determine, through statistical evidence and
historical market data, whether a feature contains predictive
information about future market behavior.

This protocol is independent of:

- Trading strategy
- Machine Learning models
- Portfolio management
- Position sizing
- Risk management

The Feature Engine computes observations.

The Research Engine evaluates whether those observations have
predictive value.

---

# Research Philosophy

Every feature begins as an engineering implementation.

Implementation correctness DOES NOT imply predictive usefulness.

Every feature must pass objective statistical validation before being
considered a Core feature.

No feature is accepted based on:

- Opinion
- Internet articles
- Traditional Technical Analysis
- Popularity
- Books
- YouTube
- Prior assumptions

Evidence is the only acceptance criterion.

---

# Research Pipeline

```
Market Data
        │
        ▼
Market Structure
        │
        ▼
Feature Engine
        │
        ▼
Deterministic Features
        │
        ▼
Research Dataset
        │
        ▼
Statistical Analysis
        │
        ▼
Hypothesis Testing
        │
        ▼
Validation
        │
        ▼
Knowledge Base
```

---

# Research Units

Research is organized around three independent concepts.

## 1. Feature

A deterministic numerical measurement.

Examples

- ATR14
- Relative Volume
- EMA20
- EMA20 Slope
- Pullback Depth
- RSI14

A feature NEVER contains trading logic.

---

## 2. Event

A structural occurrence in the market.

Examples

- BOS
- CHOCH
- Liquidity Sweep
- Expansion Start
- Expansion End
- Pullback Start
- Pullback End
- Segment Start
- Segment End

Research is always performed relative to an Event.

---

## 3. Target

The future outcome being predicted.

Examples

- BOS Continuation
- BOS Failure
- Reversal
- Expansion
- Pullback Completion
- Trend Continuation
- Trend Failure

Features predict Targets.

Events define the research context.

---

# Research Principle

Every experiment is defined by

Feature

+

Event

+

Target

Example

Feature

ATR14

Event

Confirmed BOS

Target

Continuation larger than 2 ATR

This is the smallest valid research unit.

---

# Dataset Construction

Every row in the research dataset represents ONE event.

Example

| Event | Symbol | Timeframe | Timestamp | Outcome | ATR | RSI | EMA20 Distance | Relative Volume |
|-------|---------|-----------|-----------|----------|------|------|----------------|----------------|

The dataset must NEVER contain subjective labels.

All labels must be reproducible.

---

# Event Definition Rules

Events must satisfy:

- Objective
- Deterministic
- Repeatable
- Independent

Every event must have:

- Start
- End
- Timestamp
- Context
- Market Structure State

---

# Target Definition Rules

Targets must satisfy:

- Objective
- Binary or measurable
- Future only
- No look-ahead bias

Examples

Successful BOS

Definition

Price continues at least 2 ATR before violating the protected swing.

NOT

"The trend looked strong."

---

# Feature Extraction Rules

Features are extracted ONLY from information available at the event time.

Future candles must NEVER influence feature values.

No look-ahead bias is permitted.

---

# Statistical Analysis

Every feature is evaluated using multiple statistical techniques.

Minimum required analyses

- Descriptive Statistics
- Distribution Analysis
- Correlation
- Mutual Information
- Effect Size
- Statistical Significance
- Predictive Performance

Optional analyses

- SHAP
- Permutation Importance
- Random Forest Importance
- Logistic Regression
- XGBoost Importance

No single statistical metric is sufficient.

---

# Performance Metrics

Possible metrics include

Classification

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- PR-AUC

Regression

- MAE
- RMSE
- R²

Ranking

- Information Gain
- Mutual Information
- Feature Importance

---

# Robustness Testing

Every experiment must be repeated across

Symbols

- Large Cap
- Mid Cap
- Small Cap
- Index

Timeframes

- 1m
- 5m
- 15m
- 1h
- 4h
- Daily

Market Regimes

- Trending
- Ranging
- High Volatility
- Low Volatility

Time Periods

- Bull Market
- Bear Market
- Sideways Market

A feature is considered validated only if it demonstrates stable
performance across multiple conditions.

---

# Research Status

Every feature has an independent research status.

UNTESTED

↓

UNDER_RESEARCH

↓

WEAK

↓

PROMISING

↓

VALIDATED

↓

CORE

↓

DEPRECATED

Research status is independent of implementation status.

---

# Implementation Status

Engineering maturity is tracked separately.

PLANNED

↓

IMPLEMENTED

↓

UNIT_TESTED

Implementation status indicates software quality.

Research status indicates predictive usefulness.

---

# Promotion Rules

A feature may be promoted only if

✓ Statistically significant

✓ Predictive

✓ Stable

✓ Reproducible

✓ Adds information beyond existing Core features

---

# Demotion Rules

A feature may be deprecated if

- No predictive value
- Unstable across datasets
- Redundant
- High variance
- Not reproducible

---

# Research Reports

Every completed experiment produces a report containing

Experiment ID

Feature

Event

Target

Dataset

Sample Size

Market

Timeframe

Statistical Tests

Performance Metrics

Confidence Intervals

Visualizations

Final Recommendation

---

# Knowledge Base

Validated research becomes permanent knowledge.

Example

Feature

ATR14

Context

Confirmed BOS

Target

Continuation

Dataset

2,800,000 events

Best Timeframe

15m

Best Market

NIFTY

Importance Rank

3

Confidence

96%

Status

CORE

---

# Guiding Principles

1. Features are observations, not signals.

2. Events define context.

3. Targets define prediction.

4. Research is evidence-driven.

5. All experiments must be reproducible.

6. No feature is promoted without statistical validation.

7. No strategy may rely on unvalidated features.

8. The Knowledge Base is the primary output of the Research Engine.

9. Engineering correctness and predictive usefulness are independent.

10. Objective evidence overrides assumptions.

---

# End of Protocol