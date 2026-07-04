# Indicator Architecture

Version 1.0

---

# Purpose

This document defines the role of indicators within the Institutional Trading AI semantic architecture.

Indicators are derived quantitative measurements computed from the Observation History.

Indicators are **not** semantic constructs.

Indicators provide numerical evidence that may be consumed by semantic construction policies.

---

# Architectural Position

```
Observation History

↓

Indicator Pipeline

↓

Indicator Context

↓

Semantic Construction Pipeline

↓

Canonical Market Model
```

Indicators are computed before semantic interpretation begins.

Semantic construction may consume indicators but shall never compute them.

---

# Observation vs Indicator

Observation

Represents raw market data.

Examples

- Open
- High
- Low
- Close
- Volume
- Timestamp

Observation data is directly observed from the market.

---

Indicator

Represents a derived numerical measurement.

Examples

- ATR
- EMA
- SMA
- VWAP
- RSI
- ADX

Indicators are computed from Observation History.

Indicators do not represent semantic meaning.

---

# Semantic Construct vs Indicator

Indicator

Answers

> What numerical property exists?

Examples

- ATR = 2.14
- EMA20 = 104.2

Indicators contain measurements.

---

Semantic Construct

Answers

> What does the market mean?

Examples

- Swing
- BOS
- CHOCH
- Expansion
- Order Block

Semantic constructs contain interpretation.

---

# Indicator Pipeline

The Indicator Pipeline computes every required indicator exactly once.

Input

ObservationHistory

Output

IndicatorContext

The pipeline shall perform no semantic reasoning.

Responsibilities

- compute indicators
- validate indicator values
- cache indicator series
- expose indicator lookup

The pipeline shall never:

- detect market structure
- detect swings
- classify trends
- produce ontology objects

---

# Indicator Context

IndicatorContext represents the immutable collection of computed indicators.

Example

IndicatorContext

contains

- ATR
- EMA20
- EMA50
- VWAP
- RSI
- ADX

IndicatorContext is a value object.

It performs no calculations.

---

# Indicator Consumers

Indicators may be consumed by semantic construction.

Examples

Swing Confirmation Policy

uses

ATR

---

Order Block Policy

may use

ATR
EMA

---

Liquidity Policy

may use

ATR
VWAP

---

Risk Engine

may use

ATR

---

Position Engine

may use

ATR

---

# Architectural Dependency

Allowed

Observation History

↓

Indicator Pipeline

↓

Indicator Context

↓

Semantic Construction

Not Allowed

Semantic Construction

↓

Indicator Calculation

Semantic construction shall never calculate indicators.

---

# Lifetime

ObservationHistory

Immutable

↓

IndicatorContext

Immutable

↓

CanonicalMarketModel

Immutable

Each object represents a completed stage of construction.

---

# Construction Order

Stage 1

Observation History

↓

Stage 2

Indicator Pipeline

↓

Stage 3

Indicator Context

↓

Stage 4

Semantic Construction Pipeline

↓

Stage 5

Canonical Market Model

---

# Source of Truth

Indicators derive their authority solely from the Observation History.

Indicator values are deterministic.

The same Observation History shall always produce the same Indicator Context.

---

# Invariants

IndicatorContext is immutable.

Indicator calculations are deterministic.

Indicators never mutate Observation History.

Indicators never contain semantic interpretation.

Indicators are computed exactly once.

Semantic construction consumes IndicatorContext.

Semantic construction never computes indicators.

---

# Future Indicators

Version 1

- ATR

Version 2

- EMA
- SMA

Version 3

- VWAP
- RSI

Version 4

- ADX
- MACD

Future indicators shall follow the same architecture.

---

# Public Contract

The Indicator Layer guarantees:

- deterministic computation
- immutable results
- complete indicator availability
- independence from semantic interpretation

The Indicator Layer makes no trading decisions.

The Indicator Layer performs no market interpretation.

Its sole responsibility is to provide derived quantitative measurements to the semantic construction process.