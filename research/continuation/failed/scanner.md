# Failed Continuation Scanner

## Purpose

The Failed Continuation Scanner automatically discovers **candidate failed continuation events** from historical market data.

Its purpose is **not** to determine why continuation failed.

Its purpose is to identify market sequences that **appear to develop into continuation but ultimately fail**, producing a dataset for manual semantic research.

The scanner is therefore an **evidence collection tool**, not a market interpretation engine.

---

# Research Principle

The scanner is designed for **high recall** rather than high precision.

It is acceptable to produce false positives if it reduces the probability of missing genuine failed continuations.

Human review determines whether a candidate belongs in the research dataset.

---

# Position in Research Pipeline

Historical Data

↓

Failed Continuation Scanner

↓

Candidate Dataset

↓

Review Sampling

↓

Chart Generation

↓

Manual Review

↓

Pattern Discovery

↓

Comparative Analysis

↓

Ontology Development

---

# Scanner Inputs

The scanner consumes normalized OHLCV historical data.

Required columns:

- timestamp
- open
- high
- low
- close
- volume

Current research timeframe:

- 1 Minute

Future versions should support any normalized timeframe.

---

# Scanner Outputs

The scanner produces candidate failed continuation events.

Each record includes:

- Example identifier
- Impulse start
- Impulse end
- Pullback end
- Continuation attempt
- Failure confirmation
- Direction
- Impulse size
- Pullback depth

The scanner records only observable price events.

It does **not** classify market structure.

---

# Current Detection Logic

The current scanner searches for the following sequence.

---

## Step 1 — Detect Directional Impulse

Identify a significant directional move.

Current threshold:

Minimum impulse:

- 2%

The impulse establishes the candidate trend.

---

## Step 2 — Detect Controlled Pullback

After the impulse:

Search for a controlled retracement.

Current thresholds:

Minimum retracement:

- 10%

Maximum retracement:

- 60%

Retracement is measured relative to the impulse range.

---

## Step 3 — Detect Continuation Attempt

After the pullback:

Search for evidence that the market attempts to continue.

Examples:

- Small bullish continuation
- Weak higher high
- Weak lower low
- Momentum recovery

The continuation attempt should resemble the beginning of a successful continuation.

---

## Step 4 — Detect Failure

Instead of continuation succeeding:

Search for objective failure.

Examples include:

- Loss of directional control
- Opposite-side expansion
- Pullback invalidation
- Break of pullback extreme
- Strong opposite impulse

Failure should occur within a predefined search window.

---

# Current Parameters

Current research parameters:

| Parameter | Value |
|-----------|------:|
| Minimum Impulse | 2% |
| Minimum Pullback | 10% |
| Maximum Pullback | 60% |
| Failure Search Window | 20 candles |
| Review Window | 135 candles before / 45 candles after |

These parameters are experimental and subject to future revision.

---

# Scanner Limitations

The scanner intentionally ignores many higher-level market concepts.

It does **not** identify:

- BOS
- CHOCH
- Order Blocks
- Liquidity
- Protected Swings
- Institutional Activity
- Trend State
- Expansion
- Compression

These concepts belong to later stages of research.

---

# Why Manual Review Is Required

Price may satisfy numerical conditions without representing a meaningful failed continuation.

The scanner is therefore expected to produce:

- genuine failures
- weak failures
- noisy candidates
- ambiguous structures

Manual review determines whether the example remains in the research dataset.

---

# Inclusion Criteria

Examples are retained when they exhibit:

- Clear directional impulse
- Controlled pullback
- Observable continuation attempt
- Objective continuation failure
- Sufficient chart context
- Clean structural behavior

---

# Exclusion Criteria

Examples may be removed if they contain:

- Poor chart quality
- Missing market data
- Multiple overlapping events
- Illiquid trading
- Structural ambiguity
- Scanner artifacts

---

# Design Philosophy

The scanner separates:

Detection

from

Interpretation

Detection asks:

> Could this be a failed continuation?

Interpretation asks:

> Why did continuation fail?

Only interpretation contributes to ontology development.

---

# Relationship to Successful Continuation Research

The successful continuation scanner and failed continuation scanner share the same philosophy.

Successful Scanner

↓

Candidate Successes

↓

Manual Review

Failed Scanner

↓

Candidate Failures

↓

Manual Review

Only after both datasets have been reviewed should comparisons be made.

---

# Relationship to Ontology

The scanner does not generate ontology objects.

Instead:

Scanner

↓

Candidate Events

↓

Manual Review

↓

Repeated Evidence

↓

Comparative Analysis

↓

Semantic Primitive

↓

Ontology Object

Ontology concepts must emerge from comparison rather than isolated examples.

---

# Future Improvements

Future scanner versions may include:

- Multi-timeframe confirmation
- Swing-aware failure detection
- Active Structure integration
- BOS candidate filtering
- Volatility normalization
- Adaptive thresholds
- Market regime classification
- Continuation strength scoring

These enhancements should only be introduced if supported by research evidence.

---

# Version History

## Version 1.0

Features:

- Directional impulse detection
- Controlled pullback detection
- Continuation attempt detection
- Failure detection
- Dataset generation
- Review sampling
- Chart generation

Status:

Experimental

---

# Current Status

Version:

1.0

Research Phase:

Comparative Structural Research

Dataset:

Failed Continuation Candidates

Status:

Active
