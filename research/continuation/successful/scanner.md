# Successful Continuation Scanner

## Purpose

The Successful Continuation Scanner is responsible for automatically discovering **candidate successful continuation events** from historical market data.

The scanner does **not** determine whether an event is truly a successful continuation.

Its purpose is to reduce hundreds of thousands of candles into a manageable set of candidate events for manual semantic review.

The scanner is therefore an **evidence collection tool**, not a market interpretation engine.

---

# Research Principle

The scanner intentionally performs **high recall rather than high precision**.

This means it is acceptable for the scanner to produce false positives.

Missing genuine continuation events is considered more harmful than proposing extra candidates.

Manual review is responsible for final classification.

---

# Position in Research Pipeline

Historical Data

↓

Candidate Scanner

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

Timeframe:

- Any normalized timeframe
- Current research uses 1-minute data

---

# Scanner Outputs

The scanner produces a dataset containing candidate continuation windows.

Each record includes:

- Example identifier
- Impulse start
- Impulse end
- Pullback end
- Continuation candle
- Direction
- Impulse size
- Pullback depth

The scanner does **not** assign semantic meaning.

It records observable price events only.

---

# Current Detection Logic

The current implementation identifies continuation candidates using the following sequence.

## Step 1 — Detect Directional Impulse

Search for a significant directional move.

Current threshold:

- Minimum impulse movement:
  - 2%

The impulse establishes a candidate directional move.

---

## Step 2 — Detect Pullback

After the impulse:

Search for a controlled retracement.

Current thresholds:

Minimum pullback:

- 10%

Maximum pullback:

- 60%

Retracement is measured relative to the impulse range.

---

## Step 3 — Detect Continuation

Following the pullback:

Search for price continuation beyond the impulse extreme.

Current search window:

- within 20 candles

If continuation is observed,
the window becomes a candidate example.

---

# Current Parameters

Current research parameters:

| Parameter | Value |
|-----------|------:|
| Minimum Impulse | 2% |
| Minimum Pullback | 10% |
| Maximum Pullback | 60% |
| Continuation Search | 20 candles |
| Review Window | 135 candles before / 45 candles after |

These values are experimental and may change during future research.

---

# Scanner Limitations

The scanner intentionally ignores many structural concepts.

It does not identify:

- BOS
- CHOCH
- Protected Swings
- Order Blocks
- Liquidity
- Institutional Activity
- Trend State
- Expansion
- Compression

These concepts are evaluated separately by later stages of the research process.

---

# Why Manual Review Is Required

Price satisfies numerical conditions more often than it satisfies structural conditions.

Therefore the scanner is expected to generate:

- valid continuations
- weak continuations
- noisy examples
- ambiguous examples

Manual review determines whether an example should remain in the research dataset.

---

# Inclusion Criteria

Examples are retained if they demonstrate:

- Clear directional impulse
- Controlled pullback
- Observable continuation
- Sufficient chart context
- Clean market structure

---

# Exclusion Criteria

Examples may be removed if they contain:

- Missing data
- Poor chart quality
- Multiple overlapping events
- Illiquid price action
- Structural ambiguity
- Scanner artifacts

---

# Design Philosophy

The scanner intentionally separates:

**Detection**

from

**Interpretation**

Detection answers:

> "Could this be a continuation?"

Interpretation answers:

> "Why did continuation occur?"

Only interpretation contributes to ontology development.

---

# Relationship to Ontology

The scanner does **not** create ontology objects.

It only generates candidate evidence.

Ontology objects must emerge from repeated observations across manually reviewed examples.

The relationship is therefore:

Scanner

↓

Candidate Events

↓

Manual Review

↓

Repeated Evidence

↓

Semantic Primitive

↓

Ontology Object

---

# Future Improvements

Future versions of the scanner may include:

- Multi-timeframe filtering
- Adaptive impulse thresholds
- Swing-aware continuation detection
- Active Structure integration
- BOS Candidate filtering
- Volatility normalization
- Market regime filtering

These enhancements will only be introduced if supported by research evidence.

---

# Version History

## Version 1.0

Features:

- Directional impulse detection
- Pullback detection
- Continuation detection
- Automatic dataset generation
- Automatic review sampling
- Automatic chart generation

Status:

Experimental

---

# Current Status

Version: 1.0

Research Phase:

Comparative Structural Research

Dataset:

Successful Continuation Candidates

Status:

Active