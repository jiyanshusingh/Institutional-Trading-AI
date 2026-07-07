# Feature Engine

## Purpose

The Feature Engine is the deterministic computation layer of the Institutional Market Research Platform.

Its responsibility is to transform raw market observations into reusable, measurable, and theory-independent market features.

These features become the common language shared by every higher-level component of the platform.

The Feature Engine **does not** make trading decisions.

It **does not** detect opportunities.

It **does not** reason about the market.

It only computes deterministic features.

---

# Position in Platform

```
Market Reality
        │
        ▼
Observation Engine
        │
        ▼
Scientific Computing Engine
        │
        ▼
Feature Engine   ← You are here
        │
        ▼
Research Platform
        │
        ▼
Validated Knowledge
        │
        ▼
Opportunity Discovery
        │
        ▼
Strategy Engine
        │
        ▼
Execution
        │
        ▼
Learning
```

---

# Responsibilities

The Feature Engine is responsible for:

- Computing deterministic market features.
- Providing a reusable feature library.
- Standardizing feature definitions.
- Preventing duplicate feature implementations.
- Supporting research.
- Supporting opportunity discovery.
- Supporting strategy development.
- Supporting machine learning.
- Supporting future AI reasoning.

---

# Design Principles

The Feature Engine follows these principles.

## Deterministic

Same observations

+

Same algorithm

↓

Same feature values

Always.

---

## Theory Independent

The engine does not know:

- ICT
- Wyckoff
- Dow Theory
- Smart Money Concepts
- Machine Learning

It only computes measurable quantities.

---

## Reusable

Every feature is computed once.

Every higher-level engine reuses it.

---

## Stateless

Features describe market properties.

They do not remember previous trading decisions.

---

## Independent

Each feature should be independently testable.

---

## Versioned

Feature implementations may improve over time.

Versions ensure reproducibility.

---

# Feature Categories

The engine computes features from the following categories.

```
Price

Volume

Volatility

Trend

Structure

Liquidity

Market

Sector

Industry

Relative Strength

Time

Risk

Execution

Statistical

Microstructure
```

Detailed definitions are maintained in

```
FEATURE_CATALOG.md
```

---

# Folder Structure

```
feature_engine/

│── README.md
│
│── FEATURE_CATALOG.md
│
│── feature_registry.py
│
│── feature_calculator.py
│
│── feature_definitions.py
│
│── validators.py
│
└── tests/
```

---

# Workflow

Every feature follows the same lifecycle.

```
Research Idea

↓

Definition

↓

Feature Specification

↓

Implementation

↓

Testing

↓

Validation

↓

Promotion

↓

Production
```

---

# What is a Feature?

A feature is a deterministic quantitative description of the market.

Examples

```
ATR

Relative Volume

VWAP Distance

Pullback Depth

Impulse Size

Swing Density

Market Breadth

Minutes From Open
```

A feature is **not**

- Buy Signal
- Sell Signal
- Trade Setup
- Trend Opinion
- BOS Opinion

---

# Feature Metadata

Every feature must define

```yaml
Feature:

Category:

Description:

Inputs:

Output:

Units:

Dependencies:

Status:

Version:

Deterministic:

Owner:
```

---

# Research Status

Every feature belongs to one of the following states.

```
Planned

Experimental

Validated

Core

Deprecated
```

No feature skips a stage.

---

# Relationship with Research

Research asks

> Which features separate successful outcomes from failed outcomes?

The Feature Engine provides the measurements required to answer that question.

Research never computes its own features.

Research always consumes the Feature Engine.

---

# Relationship with Opportunity Discovery

Opportunity Discovery ranks stocks using deterministic features.

Example

```
Relative Strength

Volume Expansion

Market Breadth

Sector Strength

Impulse Size

Pullback Quality
```

The Opportunity Discovery Engine never recomputes features.

---

# Relationship with Strategy

Strategies consume validated features.

They never create features.

---

# Relationship with AI

AI is **not** responsible for feature computation.

AI uses computed features to

- rank hypotheses,
- optimize weights,
- explain decisions,
- discover new candidate features.

---

# Feature Promotion

A feature becomes a Core feature only if it satisfies all of the following.

- Clearly defined.
- Deterministic.
- Reproducible.
- Historically validated.
- Improves prediction.
- Explainable.
- Generalizable within its scope.

---

# Scope

Validation is always scope-specific.

Example

```
Market:
NSE

Timeframe:
5 Minute

Session:
Opening

Sample Size:
120,000 observations
```

A feature validated in one scope is not automatically valid elsewhere.

---

# What This Engine Will Never Do

The Feature Engine will never

- generate trade signals,
- rank stocks,
- place orders,
- learn weights,
- generate hypotheses,
- interpret market behaviour.

Those responsibilities belong to higher layers.

---

# Long-Term Vision

The Feature Engine will eventually contain approximately 100–300 carefully defined deterministic features covering every measurable aspect of market behaviour.

It will become the single source of truth for feature computation across the entire Institutional Market Research Platform.

Every research project, opportunity model, strategy, learning algorithm, and future AI system will consume features from this engine, ensuring consistency, reproducibility, and maintainability throughout the platform.