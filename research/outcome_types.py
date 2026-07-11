"""
==========================================================
Outcome Types
==========================================================

Purpose
-------
Defines every canonical future market outcome used by the
Research Engine.

This module DOES NOT determine outcomes.

It only defines:

- Outcome identifiers
- Categories
- Descriptions
- Metadata

Outcome evaluation is performed by the Research Engine.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ==========================================================
# Outcome Category
# ==========================================================

class OutcomeCategory(Enum):

    BOS = "Break of Structure"

    CHOCH = "Change of Character"

    TREND = "Trend"

    EXPANSION = "Expansion"

    PULLBACK = "Pullback"

    LIQUIDITY = "Liquidity"

    RISK = "Risk"

    RETURN = "Return"

    VOLATILITY = "Volatility"


# ==========================================================
# Outcome Metadata
# ==========================================================

@dataclass(frozen=True)
class Outcome:

    id: str

    name: str

    category: OutcomeCategory

    description: str

    measurable: bool


# ==========================================================
# Outcome Registry
# ==========================================================

OUTCOMES = {

    # ------------------------------------------------------
    # BOS
    # ------------------------------------------------------

    "bos_continuation": Outcome(

        id="OUT-001",

        name="BOS Continuation",

        category=OutcomeCategory.BOS,

        description=(
            "Price continues after a confirmed BOS."
        ),

        measurable=True,

    ),

    "bos_failure": Outcome(

        id="OUT-002",

        name="BOS Failure",

        category=OutcomeCategory.BOS,

        description=(
            "Confirmed BOS fails."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # CHOCH
    # ------------------------------------------------------

    "choch_reversal": Outcome(

        id="OUT-003",

        name="CHOCH Reversal",

        category=OutcomeCategory.CHOCH,

        description=(
            "CHOCH results in a confirmed reversal."
        ),

        measurable=True,

    ),

    "choch_failure": Outcome(

        id="OUT-004",

        name="CHOCH Failure",

        category=OutcomeCategory.CHOCH,

        description=(
            "CHOCH fails to reverse the trend."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # Trend
    # ------------------------------------------------------

    "trend_continuation": Outcome(

        id="OUT-005",

        name="Trend Continuation",

        category=OutcomeCategory.TREND,

        description=(
            "Trend continues."
        ),

        measurable=True,

    ),

    "trend_reversal": Outcome(

        id="OUT-006",

        name="Trend Reversal",

        category=OutcomeCategory.TREND,

        description=(
            "Trend reverses."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # Expansion
    # ------------------------------------------------------

    "expansion_success": Outcome(

        id="OUT-007",

        name="Expansion Success",

        category=OutcomeCategory.EXPANSION,

        description=(
            "Expansion reaches predefined objective."
        ),

        measurable=True,

    ),

    "expansion_failure": Outcome(

        id="OUT-008",

        name="Expansion Failure",

        category=OutcomeCategory.EXPANSION,

        description=(
            "Expansion fails before objective."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # Pullback
    # ------------------------------------------------------

    "pullback_completion": Outcome(

        id="OUT-009",

        name="Pullback Completion",

        category=OutcomeCategory.PULLBACK,

        description=(
            "Pullback completes successfully."
        ),

        measurable=True,

    ),

    "deep_pullback": Outcome(

        id="OUT-010",

        name="Deep Pullback",

        category=OutcomeCategory.PULLBACK,

        description=(
            "Pullback exceeds predefined depth."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # Liquidity
    # ------------------------------------------------------

    "liquidity_reversal": Outcome(

        id="OUT-011",

        name="Liquidity Reversal",

        category=OutcomeCategory.LIQUIDITY,

        description=(
            "Liquidity sweep results in reversal."
        ),

        measurable=True,

    ),

    "liquidity_continuation": Outcome(

        id="OUT-012",

        name="Liquidity Continuation",

        category=OutcomeCategory.LIQUIDITY,

        description=(
            "Liquidity sweep results in continuation."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    "positive_return": Outcome(

        id="OUT-013",

        name="Positive Return",

        category=OutcomeCategory.RETURN,

        description=(
            "Future return is positive."
        ),

        measurable=True,

    ),

    "negative_return": Outcome(

        id="OUT-014",

        name="Negative Return",

        category=OutcomeCategory.RETURN,

        description=(
            "Future return is negative."
        ),

        measurable=True,

    ),

    # ------------------------------------------------------
    # Volatility
    # ------------------------------------------------------

    "volatility_expansion": Outcome(

        id="OUT-015",

        name="Volatility Expansion",

        category=OutcomeCategory.VOLATILITY,

        description=(
            "Future volatility increases."
        ),

        measurable=True,

    ),

    "volatility_contraction": Outcome(

        id="OUT-016",

        name="Volatility Contraction",

        category=OutcomeCategory.VOLATILITY,

        description=(
            "Future volatility decreases."
        ),

        measurable=True,

    ),

}


# ==========================================================
# Helper Functions
# ==========================================================

def get_outcome(
    outcome_name: str,
) -> Outcome:
    """
    Return metadata for an outcome.
    """

    return OUTCOMES[outcome_name]


def list_outcomes():
    """
    Return all registered outcomes.
    """

    return sorted(OUTCOMES.keys())


def outcomes_by_category(
    category: OutcomeCategory,
):
    """
    Return all outcomes belonging to a category.
    """

    return {

        name: outcome

        for name, outcome in OUTCOMES.items()

        if outcome.category == category

    }


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("OUTCOME TYPES")
    print("=" * 60)

    print()

    print(
        f"Total Outcomes : {len(OUTCOMES)}"
    )

    print()

    for outcome in list_outcomes():

        print(outcome)