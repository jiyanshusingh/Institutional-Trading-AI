# 05_PROJECT_PHILOSOPHY.md

**Version:** 1.0 (Draft)
**Status:** Normative Philosophy Document

---

# 1. Purpose

This document defines the long-term philosophy of the Institutional Trading AI project.

Its purpose is to preserve the principles that guide the evolution of the system beyond any individual implementation, programming language, market theory, or trading strategy.

While the Semantic Foundation defines *why* the theory exists, the Ontology defines *what* exists, the Computational Model defines *how* it is realized, and the Verification Specification defines *how correctness is demonstrated*, this document explains **how the project should evolve over time**.

---

# 2. Vision

The project aims to build a deterministic, explainable, extensible, and reusable market reasoning framework.

The objective is **not** to build a collection of trading strategies.

The objective is to build a system capable of constructing a canonical semantic interpretation of market observations under a declared theory, and enabling multiple reasoning and decision systems to operate upon that interpretation.

Trading is an application of the framework, not its foundation.

---

# 3. Guiding Principle

The project shall always prioritize:

1. Semantic correctness.
2. Ontological consistency.
3. Deterministic computation.
4. Explainability.
5. Extensibility.
6. Maintainability.

Implementation convenience shall never override semantic correctness.

---

# 4. Separation of Concerns

The project is intentionally divided into independent layers.

## Semantics

Answers:

> Why does this distinction exist?

---

## Ontology

Answers:

> What concepts exist?

---

## Computation

Answers:

> How are those concepts realized?

---

## Verification

Answers:

> How do we know the realization is correct?

---

## Evaluation

Answers:

> What do the established semantic constructs imply?

---

## Decision

Answers:

> What action should be taken?

---

## Execution

Answers:

> How is that action performed?

Each layer has exactly one responsibility.

No layer shall redefine the responsibilities of another.

---

# 5. Theory Before Strategy

Strategies are not part of the semantic foundation.

A strategy consumes semantic constructs produced by a declared theory.

Different strategies may operate over the same Canonical Market Model without changing the underlying semantic interpretation.

The semantic engine shall remain strategy-independent.

---

# 6. Determinism Before Intelligence

The project adopts deterministic semantic construction as its foundation.

Machine Learning, statistical methods, and Large Language Models are enhancements that operate on established semantic knowledge.

They shall not replace deterministic semantic construction.

The system shall first understand the market, then reason about it.

---

# 7. Explainability

Every significant output should be explainable.

The system should be capable of answering questions such as:

* Why was this Swing established?
* Why was this Structure Event confirmed?
* Why does this Origin Region exist?
* Why was this trade candidate generated?

Explainability is a design requirement rather than an optional feature.

---

# 8. Minimality

The project seeks the smallest semantic ontology capable of expressing the distinctions required by the declared theory.

New concepts shall not be admitted because they are popular or commonly used.

A concept shall enter the ontology only if it introduces an irreducible semantic distinction.

---

# 9. Extensibility

The framework shall support multiple market theories.

Examples include:

* ICT
* Wyckoff
* Classical Price Action
* Volume Profile
* Market Profile
* Future semantic theories

Extending the framework shall not require changing its semantic foundation.

New theories should extend the system through additional ontology and computation rather than altering existing semantics.

---

# 10. Evolution

The project shall evolve through controlled extension.

Changes shall be classified as one of the following:

## Theory Extension

Introduces new semantic distinctions while preserving existing semantics.

---

## Ontology Extension

Introduces new semantic constructs required by the theory.

---

## Computational Improvement

Improves implementation while preserving semantics.

---

## Strategy Extension

Introduces new evaluations, decisions, or execution policies.

Each type of change shall preserve backward compatibility whenever possible.

---

# 11. Engineering Principles

Software engineering decisions shall follow these principles.

* Prefer clarity over cleverness.
* Prefer correctness over optimization.
* Prefer immutability over mutable state.
* Prefer explicit dependencies over hidden coupling.
* Prefer composition over unnecessary inheritance.
* Prefer deterministic behavior over implicit heuristics.
* Prefer reproducibility over convenience.

---

# 12. Research Principles

Research shall be disciplined.

Before introducing a new concept, ask:

1. Does the theory require it?
2. What semantic distinction does it introduce?
3. Can existing constructs already express that distinction?
4. Is it independent of implementation?
5. Is it deterministic?
6. Does it simplify or complicate the ontology?

Questions that do not improve the semantic foundation, ontology, computational model, or trading capability should be deferred.

---

# 13. Artificial Intelligence

Artificial Intelligence is a consumer of the semantic model, not its replacement.

Recommended roles include:

* evaluation support;
* opportunity ranking;
* confidence estimation;
* natural language explanation;
* historical comparison;
* research assistance.

AI should operate on structured semantic knowledge rather than raw market observations whenever possible.

---

# 14. Long-Term Architecture

The intended progression of the project is:

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
        │
        ▼
Monitoring
        │
        ▼
Learning
```

Every future capability shall integrate into this architecture without violating the responsibilities of each layer.

---

# 15. Success Criteria

The project will be considered successful when it satisfies the following objectives:

* Produces deterministic semantic interpretations.
* Preserves semantic correctness across implementations.
* Supports multiple market theories.
* Enables explainable evaluation and decision making.
* Generates reusable semantic knowledge.
* Allows automation without sacrificing transparency.
* Serves as a foundation for advanced analytics, machine learning, and autonomous trading systems.

Success is measured by correctness, explainability, extensibility, and long-term maintainability—not merely by short-term trading performance.

---

# 16. Conclusion

The Institutional Trading AI project is a market reasoning framework before it is a trading system.

Its purpose is to construct a canonical semantic interpretation of market observations under a declared theory and provide a stable foundation upon which evaluation, decision-making, automation, and intelligent systems can be built.

Every future contribution should preserve this philosophy.

When uncertainty arises, preference shall be given to semantic correctness, deterministic behavior, and architectural simplicity over implementation convenience or short-term optimization.
