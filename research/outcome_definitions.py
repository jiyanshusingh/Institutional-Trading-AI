"""
==========================================================
Outcome Definitions
==========================================================

Purpose
-------
Defines the evaluation rules for every research outcome.

This module DOES NOT evaluate outcomes.

It only specifies:

- Outcome identifier
- Success criteria
- Failure criteria
- Evaluation horizon
- Required measurements

The OutcomeBuilder consumes these definitions to label
ResearchSamples.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ==========================================================
# Evaluation Metric
# ==========================================================

class EvaluationMetric(Enum):

    ATR = "ATR"

    PRICE = "Price"

    PERCENT = "Percent"

    RISK_REWARD = "Risk Reward"

    SWING = "Swing"

    CANDLES = "Candles"


# ==========================================================
# Outcome Definition
# ==========================================================

@dataclass(frozen=True)
class OutcomeDefinition:

    id: str

    outcome: str

    description: str

    success_metric: EvaluationMetric

    success_value: float

    failure_metric: EvaluationMetric

    failure_value: float

    max_bars: int

    requires_protected_swing: bool

    notes: str = ""


# ==========================================================
# Registry
# ==========================================================

OUTCOME_DEFINITIONS = {

    # ------------------------------------------------------
    # BOS Continuation
    # ------------------------------------------------------

    "bos_continuation": OutcomeDefinition(

        id="OD-001",

        outcome="bos_continuation",

        description=(
            "Price moves 2 ATR before violating "
            "the protected swing."
        ),

        success_metric=EvaluationMetric.ATR,

        success_value=2.0,

        failure_metric=EvaluationMetric.SWING,

        failure_value=1.0,

        max_bars=20,

        requires_protected_swing=True,

    ),

    # ------------------------------------------------------
    # BOS Failure
    # ------------------------------------------------------

    "bos_failure": OutcomeDefinition(

        id="OD-002",

        outcome="bos_failure",

        description=(
            "Protected swing is violated before "
            "price reaches 2 ATR."
        ),

        success_metric=EvaluationMetric.SWING,

        success_value=1.0,

        failure_metric=EvaluationMetric.ATR,

        failure_value=2.0,

        max_bars=20,

        requires_protected_swing=True,

    ),

    # ------------------------------------------------------
    # Trend Continuation
    # ------------------------------------------------------

    "trend_continuation": OutcomeDefinition(

        id="OD-003",

        outcome="trend_continuation",

        description=(
            "Trend continues at least 3 ATR."
        ),

        success_metric=EvaluationMetric.ATR,

        success_value=3.0,

        failure_metric=EvaluationMetric.SWING,

        failure_value=1.0,

        max_bars=40,

        requires_protected_swing=True,

    ),

    # ------------------------------------------------------
    # Trend Reversal
    # ------------------------------------------------------

    "trend_reversal": OutcomeDefinition(

        id="OD-004",

        outcome="trend_reversal",

        description=(
            "Trend reverses by breaking the "
            "protected swing."
        ),

        success_metric=EvaluationMetric.SWING,

        success_value=1.0,

        failure_metric=EvaluationMetric.ATR,

        failure_value=2.0,

        max_bars=30,

        requires_protected_swing=True,

    ),

    # ------------------------------------------------------
    # Expansion
    # ------------------------------------------------------

    "expansion_success": OutcomeDefinition(

        id="OD-005",

        outcome="expansion_success",

        description=(
            "Expansion reaches 3 ATR."
        ),

        success_metric=EvaluationMetric.ATR,

        success_value=3.0,

        failure_metric=EvaluationMetric.SWING,

        failure_value=1.0,

        max_bars=30,

        requires_protected_swing=True,

    ),

    # ------------------------------------------------------
    # Pullback
    # ------------------------------------------------------

    "pullback_completion": OutcomeDefinition(

        id="OD-006",

        outcome="pullback_completion",

        description=(
            "Pullback completes within 15 candles."
        ),

        success_metric=EvaluationMetric.CANDLES,

        success_value=15,

        failure_metric=EvaluationMetric.CANDLES,

        failure_value=30,

        max_bars=30,

        requires_protected_swing=False,

    ),

}


# ==========================================================
# Helper Functions
# ==========================================================

def get_definition(
    outcome: str,
) -> OutcomeDefinition:
    """
    Return an outcome definition.
    """

    return OUTCOME_DEFINITIONS[outcome]


def list_definitions():
    """
    Return all registered outcome definitions.
    """

    return sorted(OUTCOME_DEFINITIONS.keys())


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("OUTCOME DEFINITIONS")
    print("=" * 60)

    print()

    print(
        f"Definitions : {len(OUTCOME_DEFINITIONS)}"
    )

    print()

    for definition in list_definitions():

        print(definition)