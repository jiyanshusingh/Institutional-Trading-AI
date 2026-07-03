# 02_MARKET_STRUCTURE_ONTOLOGY.md

**Version:** 1.0 (Draft)
**Status:** Part 1 – Ontology Framework

---

# 1. Purpose

The purpose of this document is to define the ontology of the **Market Structure Theory**.

The ontology specifies the semantic constructs required to express market structure under the theory defined in **01_SEMANTIC_FOUNDATION.md**.

This document defines:

* what semantic constructs exist;
* why they exist;
* how they are specified;
* how they relate to one another.

This document does **not** define computational algorithms, software architecture, trading strategies, or implementation details.

---

# 2. Scope

This ontology specifies only the **Semantic Construction Layer** of the Market Structure Theory.

It includes:

* semantic constructs;
* semantic relationships;
* semantic dependencies;
* semantic invariants;
* semantic representations.

It explicitly excludes:

* computational policies;
* algorithms;
* software architecture;
* implementation details;
* evaluations;
* trading decisions;
* execution;
* machine learning;
* optimization techniques.

These belong to subsequent specifications.

---

# 3. Ontology Categories

Every ontology element shall belong to exactly one Knowledge Category.

## 3.1 Observation

An **Observation** is objective market information directly available from the Observation Space defined by the Semantic Foundation.

Observations introduce no semantic interpretation.

Examples:

* OHLC
* Time

---

## 3.2 Semantic Construct

### Definition

A **Semantic Construct** is a theory-defined semantic concept that represents an irreducible semantic distinction within a semantic interpretation.

A Semantic Construct exists because the theory requires that distinction in order to express market structure.

### Properties

A Semantic Construct:

* belongs to the semantic ontology;
* is established under exactly one declared theory;
* introduces at least one semantic distinction;
* is deterministic;
* is immutable once established;
* may depend upon other semantic constructs.

### A Semantic Construct is NOT

A Semantic Construct is not:

* an algorithm;
* a policy;
* a software class;
* a representation;
* an evaluation;
* a trading decision.

---

## 3.3 Representation

### Definition

A **Representation** is an alternative expression of existing semantic knowledge that introduces no new semantic distinction.

A Representation exists solely to make existing semantic knowledge usable by downstream layers.

### Properties

A Representation:

* introduces no new semantic meaning;
* has exactly one Source of Truth;
* is deterministic;
* is immutable;
* belongs outside the semantic ontology.

---

# 4. Ontology Contract

Every Semantic Construct shall be specified using the following schema.

| Field                  | Purpose                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| Definition             | What the construct is.                                                                          |
| Purpose                | Why the construct exists.                                                                       |
| Knowledge Category     | Observation, Semantic Construct, or Representation.                                             |
| Semantic Role          | What semantic distinction the construct introduces.                                             |
| Source of Truth        | The unique semantic knowledge from which the construct is established.                          |
| Establishing Condition | The necessary and sufficient semantic condition under which the construct comes into existence. |
| Dependencies           | Semantic constructs that must already exist.                                                    |
| Invariants             | Properties that are always true.                                                                |
| Relationships          | Semantic associations with other constructs.                                                    |

Every Semantic Construct shall satisfy this contract.

---

# 5. Source of Truth

## Definition

The **Source of Truth** is the unique semantic knowledge from which the existence of a construct is established.

Every construct shall have exactly one Source of Truth.

## Purpose

The Source of Truth answers the question:

> **What existing semantic knowledge ultimately establishes the existence of this construct?**

The Source of Truth identifies semantic authority rather than computational origin.

---

# 6. Establishing Condition

## Definition

The **Establishing Condition** is the necessary and sufficient semantic condition under which a construct comes into existence.

Unlike the Source of Truth, which identifies semantic authority, the Establishing Condition specifies the condition that establishes the construct.

It answers the question:

> **When does this construct exist?**

---

# 7. Dependency

## Definition

A **Dependency** is another semantic construct whose prior existence is required before the current construct can be established.

Dependencies define semantic prerequisites rather than computational ordering.

## Properties

A Dependency:

* is semantic;
* is deterministic;
* shall not create dependency cycles;
* does not imply ownership;
* does not imply composition.

Dependencies specify semantic prerequisites and shall not be inferred from implementation order.

---

# 8. Relationship

## Definition

A **Relationship** is a theory-defined semantic association between two or more ontology elements.

Relationships describe how ontology elements are semantically connected.

Relationships do not describe implementation.

## Properties

A Relationship:

* is semantic;
* is directional where appropriate;
* is independent of implementation;
* shall not contradict construct invariants.

---

# 9. Invariant

## Definition

An **Invariant** is a property that shall always remain true for every valid instance of a semantic construct.

An invariant is intrinsic to the construct.

It is independent of implementation.

## Typical Invariants

Examples include:

* immutable;
* deterministic;
* contiguous;
* established exactly once;
* unique Source of Truth.

## Not Invariants

The following are not invariants:

* implementation details;
* algorithmic procedures;
* database storage;
* visualization;
* software architecture;
* downstream usage.

---

# 10. Representation

A Representation exists to express existing semantic knowledge without introducing additional semantic meaning.

A Representation:

* has exactly one Source of Truth;
* introduces no semantic distinction;
* depends upon an existing semantic construct;
* preserves semantic meaning;
* may support downstream analysis, visualization, or execution.

Representations belong outside the semantic ontology.

---

# 11. Ontology Principles

Every ontology element shall satisfy the following principles.

### Principle 1 — Semantic Necessity

Every Semantic Construct shall introduce at least one irreducible semantic distinction.

---

### Principle 2 — Theory Relativity

Every Semantic Construct is defined under exactly one declared theory.

---

### Principle 3 — Unique Source of Truth

Every construct shall have exactly one Source of Truth.

---

### Principle 4 — Explicit Dependencies

Every dependency shall be explicitly specified.

---

### Principle 5 — Explicit Invariants

Every construct shall declare its invariants.

---

### Principle 6 — Immutability

A Semantic Construct is immutable once established.

---

### Principle 7 — Determinism

Identical observations interpreted under the same declared theory shall establish identical semantic constructs.

---

### Principle 8 — Implementation Independence

Semantic meaning shall not depend upon computational implementation.

---

### Principle 9 — Representation Integrity

Representations may reorganize semantic knowledge but shall not introduce new semantic distinctions.

---

### Principle 10 — Ontological Closure

A Semantic Construct may depend only upon Observations or other Semantic Constructs.

It shall never depend upon evaluations, decisions, execution, or implementation artifacts.

---

# 12. Admission Checklist

Before a new concept is admitted into the ontology, it shall answer the following questions.

1. What is its Definition?
2. Why does it exist?
3. What semantic distinction does it introduce?
4. What is its Knowledge Category?
5. What is its unique Source of Truth?
6. What is its Establishing Condition?
7. What are its semantic Dependencies?
8. What Invariants must always hold?
9. What Relationships does it have with existing constructs?
10. Can its semantic meaning already be expressed by existing constructs?

If the answer to Question 10 is **Yes**, the concept shall not be admitted as a new Semantic Construct.

---

# 13. Relationship to Subsequent Sections

The remainder of this document instantiates this ontology contract for each semantic construct admitted into the Market Structure Theory.

Every construct defined in this ontology shall conform to the contract established in this specification.

# 02_MARKET_STRUCTURE_ONTOLOGY.md

## Part 2 — Semantic Constructs

---

# 14. Swing

## Definition

A **Swing** is a Semantic Construct representing a structurally significant turning point established under the Market Structure Theory.

## Purpose

To enable the theory to distinguish structurally significant turning points from ordinary market observations.

## Knowledge Category

Semantic Construct

## Semantic Role

Introduces the semantic distinction between structurally significant turning points and ordinary price movement.

## Source of Truth

Observation Space

## Establishing Condition

A Swing is established when the observation history satisfies the structural turning-point criteria defined by the Market Structure Theory.

## Dependencies

* Observation Space

## Invariants

* Immutable once established.
* Deterministically established under the declared theory.
* Established exactly once.
* Has exactly one Source of Truth.

## Relationships

* Establishes Structure Events.

---

# 15. Structure Event

## Definition

A **Structure Event** is a Semantic Construct representing a confirmed structural event established from previously established Swings.

## Purpose

To enable the theory to distinguish confirmed structural change from isolated structural turning points.

## Knowledge Category

Semantic Construct

## Semantic Role

Introduces the semantic distinction of confirmed structural change.

## Types

* Break of Structure (BOS)
* Change of Character (CHOCH)

## Source of Truth

Swing

## Establishing Condition

A Structure Event is established when previously established Swings satisfy the structural confirmation criteria defined by the Market Structure Theory.

## Dependencies

* Swing

## Invariants

* Immutable once established.
* Deterministically established.
* Established exactly once.
* Has exactly one Source of Truth.

## Relationships

* Depends upon Swing.
* Establishes Expansion.

---

# 16. Expansion

## Definition

An **Expansion** is a Semantic Construct representing confirmed structural movement established from Structure Events.

## Purpose

To enable the theory to distinguish coherent confirmed structural movement from isolated structural events.

## Knowledge Category

Semantic Construct

## Semantic Role

Introduces the semantic distinction of confirmed structural movement.

## Source of Truth

Structure Event

## Establishing Condition

An Expansion is established when confirmed Structure Events satisfy the movement-establishing criteria defined by the Market Structure Theory.

## Dependencies

* Structure Event

## Invariants

* Immutable once established.
* Deterministically established.
* Directionally consistent.
* Established exactly once.
* Has exactly one Source of Truth.

## Relationships

* Depends upon Structure Events.
* Establishes Origin Region.

---

# 17. Origin Region

## Definition

An **Origin Region** is a Semantic Construct representing the structural origin associated with confirmed structural movement.

## Purpose

To enable the theory to distinguish the structural origin of confirmed movement from the movement itself.

## Knowledge Category

Semantic Construct

## Semantic Role

Introduces the semantic distinction of structural origin.

## Source of Truth

Expansion

## Establishing Condition

An Origin Region is established when an Expansion satisfies the origin-identification criteria defined by the Market Structure Theory.

## Dependencies

* Expansion

## Invariants

* Immutable once established.
* Deterministically established.
* Established exactly once.
* Has exactly one Source of Truth.

## Relationships

* Depends upon Expansion.
* May be represented by an Order Block.

---

# 18. Fair Value Gap

## Definition

A **Fair Value Gap** is a Semantic Construct representing an objectively defined structural price imbalance established directly from the Observation Space.

## Purpose

To enable the theory to distinguish structurally imbalanced price movement from balanced price movement.

## Knowledge Category

Semantic Construct

## Semantic Role

Introduces the semantic distinction of structural imbalance.

## Source of Truth

Observation Space

## Establishing Condition

A Fair Value Gap is established when the observation history satisfies the imbalance criteria defined by the Market Structure Theory.

## Dependencies

* Observation Space

## Invariants

* Immutable once established.
* Deterministically established.
* Established exactly once.
* Has exactly one Source of Truth.

## Relationships

* Depends upon the Observation Space.
* Is semantically independent of Swing, Structure Event, Expansion, and Origin Region.
* May participate in downstream semantic analysis.

---

# 19. Order Block

## Definition

An **Order Block** is a Representation expressing an established Origin Region in a form suitable for downstream consumption.

## Purpose

To provide a deterministic representation of an Origin Region without introducing additional semantic meaning.

## Knowledge Category

Representation

## Semantic Role

Introduces no semantic distinction.

Represents existing semantic knowledge established by an Origin Region.

## Source of Truth

Origin Region

## Establishing Condition

An Order Block is established when an Origin Region is represented according to the representation rules defined by the Market Structure Theory.

## Dependencies

* Origin Region

## Invariants

* Immutable once established.
* Deterministically established.
* Has exactly one Source of Truth.
* Preserves the semantic meaning of its Origin Region.
* Introduces no new semantic distinction.

## Relationships

* Depends upon Origin Region.
* Represents Origin Region.
* Exists solely as a representation.

---

# 20. Deferred Concepts

The following concepts are intentionally excluded from Ontology Version 1.0.

They remain under semantic investigation and are **not** part of the normative specification.

---

## Segment

**Status**

Deferred to Version 1.1.

**Reason**

The semantic necessity of Segment has not yet been formally demonstrated according to the Semantic Admission Principle defined in **01_SEMANTIC_FOUNDATION.md**.

Its precise semantic role remains under investigation.

---

## Liquidity

**Status**

Deferred.

**Reason**

The semantic distinction introduced by Liquidity has not yet been formally established.

Liquidity shall not be admitted into the ontology until it satisfies the Semantic Admission Principle.

No concept shall enter the ontology solely because it is widely used in trading literature.

# 02_MARKET_STRUCTURE_ONTOLOGY.md

## Part 3 — Ontology Structure and Governance

---

# 21. Ontology Dependency Graph

The ontology dependency graph specifies the semantic dependency relationships between ontology elements.

A directed edge indicates a **semantic dependency**, meaning the target construct cannot be established until the source construct has already been established.

The dependency graph is independent of computational implementation.

```text
                    Observation Space
                     /              \
                    /                \
                   ▼                  ▼
               Swing           Fair Value Gap
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
                  ▼
             Order Block
           (Representation)
```

### Dependency Summary

| Construct       | Depends On        |
| --------------- | ----------------- |
| Swing           | Observation Space |
| Structure Event | Swing             |
| Expansion       | Structure Event   |
| Origin Region   | Expansion         |
| Fair Value Gap  | Observation Space |
| Order Block     | Origin Region     |

---

# 22. Dependency Principles

The ontology dependency graph shall satisfy the following principles.

## Principle 1 — Directed Dependencies

Every dependency shall have a well-defined semantic direction.

---

## Principle 2 — Acyclic Dependencies

The dependency graph shall not contain dependency cycles.

No construct may directly or indirectly depend upon itself.

---

## Principle 3 — Semantic Dependencies

Dependencies describe semantic prerequisites only.

They shall not imply computational execution order.

---

## Principle 4 — Minimal Dependencies

A construct shall depend only upon the semantic knowledge required for its establishment.

Unnecessary dependencies shall not be introduced.

---

## Principle 5 — Dependency Stability

Dependencies are part of the ontology specification.

Changing a dependency constitutes an ontology revision.

---

# 23. Ontology Completeness

Ontology Version 1.0 consists of the following elements.

## Observations

* Observation Space

---

## Semantic Constructs

* Swing
* Structure Event
* Expansion
* Origin Region
* Fair Value Gap

---

## Representations

* Order Block

---

## Deferred Concepts

* Segment
* Liquidity

No additional concepts belong to Ontology Version 1.0.

---

# 24. Ontology Evolution

The ontology shall evolve according to the Semantic Foundation.

New ontology concepts shall be introduced only after satisfying the Semantic Admission Principle.

Every newly admitted concept shall:

* conform to the Ontology Contract;
* introduce an irreducible semantic distinction;
* identify a unique Source of Truth;
* declare explicit Dependencies;
* declare explicit Invariants;
* specify semantic Relationships.

---

## Ontology Extension

An ontology extension introduces new semantic constructs while preserving the semantics of all existing constructs.

Extensions are backward compatible.

---

## Ontology Revision

An ontology revision changes the meaning of one or more existing semantic constructs.

Ontology revisions require a new ontology version.

---

# 25. Version History

| Version | Status | Description                                                                  |
| ------- | ------ | ---------------------------------------------------------------------------- |
| 1.0     | Draft  | Initial ontology specification based on the Semantic Foundation Version 1.0. |

Future versions shall explicitly document:

* added constructs;
* removed constructs;
* modified semantics;
* compatibility considerations.

---

# 26. Relationship to Other Specifications

This document depends upon:

* **01_SEMANTIC_FOUNDATION.md**

This document provides the semantic specification used by:

* **03_COMPUTATIONAL_ARCHITECTURE.md**
* **04_VERIFICATION.md**
* **05_PROJECT_PHILOSOPHY.md**

The ontology defines **what exists** within the Market Structure Theory.

It does not define:

* how constructs are computed;
* how constructs are stored;
* how constructs are evaluated;
* how trading decisions are made.

Those responsibilities belong to subsequent specifications.

---

# 27. Conformance

A computational implementation conforms to this ontology if and only if:

1. Every implemented ontology concept corresponds to a construct defined in this specification.
2. Every construct satisfies its Ontology Contract.
3. Every dependency conforms to the ontology dependency graph.
4. No implementation introduces semantic constructs that are absent from this specification without an explicit ontology extension.
5. Representations introduce no new semantic distinctions.
6. Computational implementation does not alter the semantics defined by this ontology.

Conformance to this ontology does not require a specific programming language, software architecture, algorithm, or data structure.

---

# 28. Conclusion

This specification defines the normative ontology for the Market Structure Theory Version 1.0.

It establishes the semantic vocabulary through which market structure is expressed under the declared theory.

The ontology is intentionally minimal.

Only semantic constructs whose necessity has been established according to the Semantic Foundation are admitted.

Representations remain distinct from semantic constructs, and implementation concerns remain outside the ontology.

Future extensions shall preserve the integrity, determinism, and semantic consistency established by this specification.
