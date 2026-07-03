# 01_SEMANTIC_FOUNDATION.md

**Version:** 1.0 (Draft)
**Status:** Draft – Intended to be frozen after final review

---

# 1. Purpose

The purpose of this document is to define the semantic foundation of the Institutional Trading AI project.

This document establishes the fundamental principles governing how market observations are interpreted into deterministic, canonical, and explainable semantic meaning.

It does **not** define market concepts, trading strategies, algorithms, or software implementation.

Its purpose is to provide a stable theoretical foundation from which all future theories, ontologies, computational architectures, and implementations are derived.

---

# 2. Scope

This document defines:

* the observation space;
* the concept of a theory;
* semantic interpretation;
* canonical interpretation;
* semantic distinctions;
* semantic admission principles;
* theory evolution principles;
* separation of concerns;
* foundational axioms.

This document deliberately excludes:

* market concepts;
* trading concepts;
* implementation details;
* software architecture;
* algorithms;
* optimization techniques.

These are specified in subsequent documents.

---

# 3. Observation Space

## Definition

The **Observation Space** is the complete set of information directly observed from the market.

For Version 1.0, the Observation Space consists of:

* Open
* High
* Low
* Close
* Time

Future versions may extend the Observation Space with additional observable information such as volume, order flow, market depth, options data, or other objective market observations.

## Principles

* Observations are objective.
* Observations are immutable.
* Observations are the only source of external information available to a theory.
* The theory never modifies observations.

---

# 4. Theory

## Definition

A **Theory** is a formal specification that defines how observations are interpreted into semantic meaning.

A theory specifies:

* the semantic vocabulary;
* the semantic constructs;
* the relationships between semantic constructs;
* the rules by which semantic constructs are established.

A theory defines **what distinctions are meaningful** within its domain.

Different theories may legitimately assign different semantic interpretations to the same observation history.

Semantic meaning therefore exists only relative to a declared theory.

---

# 5. Semantic Interpretation

## Definition

A **Semantic Interpretation** is the deterministic assignment of semantic meaning to an observation history under a declared theory.

Formally,

**Observation History + Theory → Semantic Interpretation**

The interpretation does not modify observations.

It assigns semantic meaning to them according to the declared theory.

Different theories may produce different semantic interpretations from identical observations.

---

# 6. Canonical Interpretation

## Definition

A semantic interpretation is **canonical** if identical inputs always produce exactly one semantic interpretation.

Identical inputs consist of:

* identical observation histories;
* the same declared theory.

Canonical interpretation guarantees:

* determinism;
* reproducibility;
* consistency;
* explainability.

Canonicality is a property of the semantic interpretation, not of any particular implementation.

---

# 7. Semantic Distinction

## Definition

A **Semantic Distinction** exists when a theory assigns different semantic meanings to observation histories that would otherwise be considered equivalent under that theory.

Semantic distinctions define the expressive power of a theory.

Every semantic construct exists because it realizes one or more semantic distinctions established by the theory.

---

# 8. Semantic Admission Principle

A semantic construct belongs in the ontology if and only if all of the following conditions are satisfied.

## Necessity

The construct introduces at least one semantic distinction that cannot already be expressed.

## Independence

The distinction is not merely another representation of an existing distinction.

## Determinism

The distinction is uniquely determined by the observation history and the declared theory.

## Reproducibility

Independent implementations of the same theory shall derive the same semantic construct from identical observations.

## Theory Definition

The distinction is defined by the theory rather than by implementation choices.

Only constructs satisfying these conditions belong in the semantic ontology.

---

# 9. Theory Extension and Theory Revision

## Theory Extension

A theory extension introduces additional semantic constructs while preserving the meaning of all previously established semantic constructs.

Theory extensions increase the expressive power of the theory without changing its existing semantics.

## Theory Revision

A theory revision changes the meaning of one or more existing semantic constructs.

A theory revision establishes a new version of the theory and should be undertaken only when necessary.

Whenever possible, theory extensions are preferred over theory revisions.

---

# 10. Separation of Concerns

The project is organized into three independent layers.

## 10.1 Semantic Foundation (Why)

Defines:

* semantic meaning;
* semantic interpretation;
* semantic distinctions;
* canonical interpretation;
* admission principles.

This layer establishes the theoretical principles governing the project.

---

## 10.2 Domain Ontology (What)

Defines:

* semantic constructs;
* relationships;
* invariants;
* dependencies.

This layer defines the vocabulary through which a theory expresses its semantic distinctions.

---

## 10.3 Computational Architecture (How)

Defines:

* algorithms;
* policies;
* software architecture;
* storage;
* optimization;
* implementation.

The computational architecture realizes the ontology but never defines its semantics.

Implementation decisions shall not alter semantic meaning.

---

# 11. Fundamental Axioms

## Axiom 1 — Observation Integrity

Observations are immutable.

---

## Axiom 2 — Deterministic Interpretation

A declared theory shall deterministically assign a semantic interpretation to a given observation history.

---

## Axiom 3 — Canonical Interpretation

For identical observation histories interpreted under the same declared theory, exactly one canonical semantic interpretation shall exist.

---

## Axiom 4 — Semantic Necessity

Every semantic construct shall justify its existence by introducing at least one irreducible semantic distinction.

---

## Axiom 5 — Representation Independence

Representations may reorganize semantic knowledge but shall not introduce new semantic distinctions.

---

## Axiom 6 — Separation of Semantics and Computation

Implementation realizes semantic meaning but never defines semantic meaning.

---

## Axiom 7 — Theory Relativity

Every semantic interpretation is meaningful only relative to a declared theory.

Identical observations interpreted under different theories may legitimately produce different semantic interpretations.

---

## Axiom 8 — Theory-Relative Derivation

Every semantic construct shall be uniquely derivable from observations and previously established semantic constructs under exactly one declared theory.

A semantic construct has no semantic meaning independent of the theory that establishes it.

---

## Axiom 9 — Explainability

Every semantic interpretation shall be explainable through the deterministic application of the declared theory to the observation history.

---

# 12. Design Principles

The project follows these design principles.

1. Observations precede interpretation.
2. Semantic interpretation precedes ontology.
3. Ontology precedes computation.
4. Facts precede evaluations.
5. Objective market understanding precedes trading decisions.
6. Semantic meaning is independent of implementation.
7. Deterministic behavior is preferred over heuristic behavior.
8. Simplicity is preferred over unnecessary abstraction.
9. New semantic constructs require justification before implementation.
10. Software exists to realize the theory, not to define it.

---

# 13. Relationship to Subsequent Documents

This document establishes only the semantic foundation.

Subsequent specifications build upon this foundation.

* **02_MARKET_STRUCTURE_ONTOLOGY.md** defines the semantic constructs of the Market Structure Theory.
* **03_COMPUTATIONAL_ARCHITECTURE.md** specifies how those semantic constructs are realized in software.
* **04_VERIFICATION.md** defines the criteria used to validate the ontology and its computational realization.
* **05_PROJECT_PHILOSOPHY.md** documents the long-term architectural philosophy and engineering principles of the project.

No subsequent document may contradict the principles established in this specification without an explicit theory revision and version update.
