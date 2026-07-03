# 06_CANONICAL_MARKET_MODEL.md

**Version:** 1.0 (Draft)
**Status:** Normative Specification

---

# 1. Purpose

The purpose of the Canonical Market Model is to provide the unique, deterministic output of the Semantic Construction Layer.

It serves as the canonical semantic interpretation of a market observation history under a declared theory.

The Canonical Market Model is the only semantic artifact consumed by downstream computational layers.

It establishes a stable architectural boundary between:

* Semantic Construction
* Evaluation
* Decision
* Execution

The Canonical Market Model does not perform reasoning, evaluation, prediction, or trading.

It represents only established semantic knowledge.

---

# 2. Scope

This specification defines:

* the purpose of the Canonical Market Model;
* its responsibilities;
* its contents;
* its invariants;
* its lifecycle;
* its consumers.

It does **not** define:

* semantic meaning;
* ontology;
* algorithms;
* policies;
* evaluations;
* trading decisions;
* execution logic.

Those are specified in other documents.

---

# 3. Definition

The **Canonical Market Model** is the immutable semantic representation of a market history produced by deterministic semantic construction under a declared theory.

It contains every established semantic construct required by the theory and nothing beyond that.

It is the unique semantic interpretation produced for a given:

* Observation History;
* Declared Theory;
* Computational Model.

---

# 4. Architectural Role

Within the computational architecture, the Canonical Market Model acts as the semantic boundary between construction and reasoning.

```text
Observation Space
        │
        ▼
Semantic Construction
        │
        ▼
Canonical Market Model
        │
        ▼
Evaluation
        │
        ▼
Decision
        │
        ▼
Execution
```

No downstream layer shall establish new semantic constructs.

---

# 5. Responsibilities

The Canonical Market Model is responsible for:

* representing the complete semantic interpretation;
* exposing semantic constructs through a stable interface;
* preserving semantic consistency;
* ensuring deterministic reproducibility;
* providing a single source of semantic knowledge.

It is **not** responsible for:

* computing semantic constructs;
* evaluating market conditions;
* generating trade setups;
* placing orders;
* storing historical data.

---

# 6. Contents

Version 1.0 shall contain the following semantic constructs.

## Observation Metadata

Metadata describing the observation history.

Examples:

* symbol;
* timeframe;
* observation range;
* theory identifier;
* model version.

---

## Semantic Constructs

### Swings

Structural turning points established directly from observations.

---

### Structure Events

Confirmed BOS and CHOCH events.

---

### Expansions

Confirmed structural movements.

---

### Origin Regions

Structural origins of confirmed expansions.

---

### Fair Value Gaps

Price imbalance constructs established directly from observations.

---

## Representations

### Order Blocks

Deterministic representations of Origin Regions.

Order Blocks are included because they are required by downstream evaluation and execution layers.

They do not introduce new semantic distinctions.

---

# 7. Excluded Concepts

The following shall **not** belong to the Canonical Market Model.

## Evaluations

* Market State
* Continuation
* Transition
* Confluence
* Liquidity Assessment
* Volatility Assessment
* Confidence

---

## Decisions

* Trade Setup
* Buy
* Sell
* Wait
* Position Size

---

## Execution

* Orders
* Stop Loss
* Target
* Portfolio
* Risk

---

## Machine Learning

* Predictions
* Classifications
* Scores
* Embeddings

---

## Infrastructure

* Repositories
* Services
* Databases
* Caches
* UI Components

---

# 8. Invariants

Every valid Canonical Market Model shall satisfy the following invariants.

## Immutable

The model shall never be modified after construction.

---

## Deterministic

Identical observations under the same theory and computational model shall produce identical models.

---

## Complete

Every semantic construct established by the declared theory shall be present.

---

## Consistent

All semantic relationships shall satisfy the ontology.

---

## Traceable

Every construct shall be traceable to its Source of Truth.

---

## Self-Contained

Downstream consumers shall not require direct access to semantic engines.

---

# 9. Construction

The Canonical Market Model shall be constructed in dependency order.

```text
Observation Space
        │
        ▼
Swing
        │
        ▼
Structure Event
        │
        ▼
Expansion
        │
        ▼
Origin Region
        │
        ├──────────────┐
        ▼              ▼
Order Block     Fair Value Gap
        │              │
        └──────┬───────┘
               ▼
Canonical Market Model
```

Each construct shall be established only after its dependencies have been satisfied.

---

# 10. Public Interface

The Canonical Market Model shall expose semantic knowledge through a stable interface.

Conceptually, it provides access to:

* observation metadata;
* swings;
* structure events;
* expansions;
* origin regions;
* fair value gaps;
* order blocks.

Consumers shall interact only with this interface.

They shall not depend directly upon individual semantic engines.

---

# 11. Consumers

The following layers consume the Canonical Market Model.

## Evaluation Layer

Uses semantic constructs to derive:

* continuation;
* transition;
* confluence;
* structural assessments;
* contextual assessments.

---

## Decision Layer

Uses evaluation outputs to generate:

* trade candidates;
* opportunity rankings;
* execution intent.

---

## Execution Layer

Uses approved trade decisions to perform market execution.

---

## Monitoring Layer

Tracks changes between successive Canonical Market Models.

---

## Learning Layer

Extracts semantic features for:

* statistical analysis;
* machine learning;
* historical research.

---

# 12. Versioning

Every Canonical Market Model shall record:

* Theory Version;
* Ontology Version;
* Computational Model Version;
* Observation History Identifier.

This ensures complete reproducibility.

---

# 13. Lifecycle

The lifecycle of the Canonical Market Model is:

```text
Observation History
        │
        ▼
Semantic Construction
        │
        ▼
Canonical Market Model
        │
        ├── Evaluation
        ├── Decision
        ├── Execution
        ├── Monitoring
        └── Learning
```

The model is created once per observation history and remains immutable throughout its lifetime.

---

# 14. Relationship to Other Specifications

This specification depends upon:

* 01_SEMANTIC_FOUNDATION.md
* 02_MARKET_STRUCTURE_ONTOLOGY.md
* 03_COMPUTATIONAL_MODEL.md
* 04_VERIFICATION.md
* 05_PROJECT_PHILOSOPHY.md

It provides the formal bridge between Semantic Construction and all downstream computational layers.

---

# 15. Future Extensions

Future versions may extend the Canonical Market Model with additional semantic constructs admitted into the ontology.

Examples may include:

* Liquidity (if formally admitted);
* Future theory-specific semantic constructs;
* Cross-theory semantic projections.

Such extensions shall preserve backward compatibility whenever possible and shall not alter the semantic meaning of existing constructs.

---

# 16. Conclusion

The Canonical Market Model is the central semantic artifact of the Institutional Trading AI framework.

It represents the complete, deterministic, immutable semantic interpretation of market observations under a declared theory.

It establishes a stable contract between Semantic Construction and every downstream layer.

All evaluation, decision-making, execution, monitoring, and learning components shall consume the Canonical Market Model rather than individual semantic engines.

By making the Canonical Market Model the single semantic interface, the framework achieves deterministic behavior, architectural isolation, explainability, extensibility, and long-term maintainability.
