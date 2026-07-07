# FEATURE_CATALOG.md

> **Purpose**
>
> This document defines the complete catalog of deterministic features used throughout the Institutional Market Research Platform.
>
> A feature is a measurable property computed from market observations or deterministic structural objects.
>
> Features are the common language shared by:
>
> - Observation Engine
> - Scientific Computing Engine
> - Research Platform
> - Opportunity Discovery Engine
> - Strategy Engine
> - Learning Engine
>
> This document defines **what features exist**, **their status**, and **their ownership**.
>
> ---
>
> ## Important Rules
>
> 1. Features are deterministic.
> 2. Features never contain opinions.
> 3. Features never make trading decisions.
> 4. Features may be promoted, improved or deprecated.
> 5. Every feature belongs to exactly one category.
> 6. Every feature must have an implementation owner.
> 7. Every feature must have validation status.

---

# Feature Status

| Status | Meaning |
|----------|---------|
| Planned | Defined but not implemented |
| Experimental | Implemented but under research |
| Validated | Research shows predictive value |
| Core | Stable production feature |
| Deprecated | No longer recommended |

---

# Feature Categories

The platform currently recognizes the following feature groups.

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

---

# 1. PRICE FEATURES

Purpose

Describe raw price behaviour.

Examples

- Candle Range
- Candle Body Size
- Body Ratio
- Upper Wick %
- Lower Wick %
- Gap %
- Close Position
- Open Position
- High-Low Distance
- Typical Price
- Median Price
- Weighted Price
- Price Velocity
- Price Acceleration
- Momentum
- Rate of Change

Status

Planned

---

# 2. VOLUME FEATURES

Purpose

Describe participation.

Examples

- Volume
- Relative Volume
- Volume Moving Average
- Volume Expansion
- Volume Contraction
- Volume Spike
- Volume Trend
- Cumulative Volume
- Volume Ratio
- Buy/Sell Volume (future)

Status

Planned

---

# 3. VOLATILITY FEATURES

Purpose

Describe price variability.

Examples

- ATR
- ATR %
- ATR Expansion
- ATR Compression
- Historical Volatility
- Rolling Volatility
- Standard Deviation
- True Range
- Average Candle Size
- Volatility Regime

Status

Planned

---

# 4. TREND FEATURES

Purpose

Describe directional behaviour.

Examples

- EMA20
- EMA50
- EMA200
- EMA Alignment
- Slope
- Trend Strength
- Trend Duration
- Trend Persistence
- Trend Efficiency
- ADX (optional)

Status

Planned

---

# 5. STRUCTURE FEATURES

Purpose

Describe market structure.

Examples

- Swing Size
- Swing Duration
- Swing Strength
- Swing Density
- Swing Direction

- Impulse Size
- Impulse Duration
- Impulse Strength

- Pullback Depth
- Pullback Duration
- Pullback Complexity

- Segment Length
- Segment Direction

- Expansion Length
- Expansion Strength

- BOS Distance
- CHOCH Distance

- Continuation Score
- Breakout Distance

Status

Research

---

# 6. LIQUIDITY FEATURES

Purpose

Describe nearby liquidity.

Examples

- Equal Highs
- Equal Lows
- Liquidity Pool Size
- Liquidity Distance
- Sweep Distance
- Stop Cluster Density
- High Liquidity Zone
- Low Liquidity Zone
- FVG Size
- Gap Fill %
- Untested Liquidity

Status

Research

---

# 7. MARKET FEATURES

Purpose

Describe overall market context.

Examples

- Index Trend
- Index Strength
- Breadth
- Advance Decline Ratio
- Market Momentum
- VIX
- Gap Direction
- Market Volatility
- Market Regime

Status

Planned

---

# 8. SECTOR FEATURES

Purpose

Describe sector behaviour.

Examples

- Sector Rank
- Sector Strength
- Sector Momentum
- Sector Volume
- Sector Breadth
- Sector Rotation
- Sector Relative Strength

Status

Planned

---

# 9. INDUSTRY FEATURES

Purpose

Describe industry behaviour.

Examples

- Industry Rank
- Industry Strength
- Industry Momentum
- Industry Rotation
- Industry Volume

Status

Planned

---

# 10. RELATIVE STRENGTH FEATURES

Purpose

Compare stock performance.

Examples

- Relative Strength vs Index
- Relative Strength vs Sector
- Relative Strength Score
- Relative Momentum
- Outperformance %
- Relative Trend

Status

Planned

---

# 11. TIME FEATURES

Purpose

Capture session behaviour.

Examples

- Minute of Day
- Minutes From Open
- Session
- Opening Range
- Closing Window
- Lunch Session
- Expiry Day
- Monthly Expiry
- Weekly Expiry
- Earnings Day
- Event Day
- Holiday Session

Status

Planned

---

# 12. RISK FEATURES

Purpose

Support risk management.

Examples

- Risk Reward Ratio
- ATR Stop
- Position Risk
- Expected Volatility
- Drawdown Risk
- Distance to Stop
- Position Size
- Portfolio Exposure

Status

Planned

---

# 13. EXECUTION FEATURES

Purpose

Support execution quality.

Examples

- Spread
- Slippage
- Fill Quality
- Order Queue
- Execution Delay
- VWAP Distance
- Participation Rate

Status

Future

---

# 14. STATISTICAL FEATURES

Purpose

Support research.

Examples

- Mean
- Variance
- Standard Deviation
- Skewness
- Kurtosis
- Correlation
- Autocorrelation
- Entropy
- Mutual Information
- Z Score

Status

Future

---

# 15. MICROSTRUCTURE FEATURES

Purpose

Order book analysis.

Examples

- Bid Ask Spread
- Order Book Imbalance
- Queue Size
- Depth Ratio
- Trade Imbalance
- Aggressive Buyers
- Aggressive Sellers
- Tick Direction

Status

Future

---

# Feature Metadata Standard

Every feature must define the following metadata.

```yaml
Feature:

Category:

Description:

Purpose:

Inputs:

Output:

Units:

Dependencies:

Engine:

Status:

Deterministic:

Version:

Owner:
```

---

# Feature Lifecycle

Every feature follows the same lifecycle.

```
Idea

↓

Definition

↓

Implementation

↓

Experimental

↓

Validation

↓

Core

↓

Deprecated
```

No feature skips a stage.

---

# Promotion Criteria

A feature becomes **Validated** only if it satisfies:

- Clearly defined.
- Deterministic implementation.
- Tested on historical data.
- Improves prediction.
- Reproducible.
- Explainable.

---

# Design Principles

- Features are reusable.
- Features never contain business logic.
- Features never trigger trades.
- Features are independent.
- Features are composable.
- Features are versioned.
- Features remain deterministic.

---

# Relationship to the Platform

```
Observation Engine
        │
        ▼
Scientific Computing Engine
        │
        ▼
Feature Library
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
Learning Engine
```

The Feature Library is the common foundation shared by every higher-level engine.

---

# Long-Term Vision

The Feature Library should eventually contain **100–300 carefully defined deterministic features** covering:

- Price
- Volume
- Volatility
- Structure
- Liquidity
- Market Context
- Sector Context
- Time Context
- Risk
- Execution
- Statistical Analysis
- Microstructure

Every future research project, trading strategy, AI model, and decision engine must consume features from this catalog rather than creating ad hoc calculations.