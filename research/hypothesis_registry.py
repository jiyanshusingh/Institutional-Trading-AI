"""
==========================================================
Hypothesis Registry
==========================================================

Purpose
-------
Central registry of every research hypothesis supported
by the Research Engine.

This module DOES NOT execute experiments.

It only defines:

- Hypothesis IDs
- Research questions
- Related features
- Related events
- Expected outcomes

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ==========================================================
# Hypothesis Status
# ==========================================================

class HypothesisStatus(Enum):

    PLANNED = "Planned"

    UNDER_RESEARCH = "Under Research"

    VALIDATED = "Validated"

    REJECTED = "Rejected"


# ==========================================================
# Hypothesis Metadata
# ==========================================================

@dataclass(frozen=True)
class Hypothesis:

    id: str

    title: str

    description: str

    features: tuple[str, ...]

    events: tuple[str, ...]

    expected_outcomes: tuple[str, ...]

    status: HypothesisStatus


# ==========================================================
# Hypothesis Registry
# ==========================================================

HYPOTHESES = {

    # ------------------------------------------------------
    # ATR
    # ------------------------------------------------------

    "atr_bos_continuation": Hypothesis(

        id="HYP-001",

        title="ATR predicts BOS continuation",

        description=(
            "Higher ATR values at a confirmed BOS "
            "increase the probability of successful "
            "trend continuation."
        ),

        features=(
            "atr_14",
        ),

        events=(
            "bos",
        ),

        expected_outcomes=(
            "bos_continuation",
        ),

        status=HypothesisStatus.PLANNED,

    ),

    # ------------------------------------------------------
    # Relative Volume
    # ------------------------------------------------------

    "relative_volume_bos": Hypothesis(

        id="HYP-002",

        title="Relative Volume predicts BOS strength",

        description=(
            "Higher Relative Volume at BOS "
            "indicates stronger continuation."
        ),

        features=(
            "relative_volume_20",
        ),

        events=(
            "bos",
        ),

        expected_outcomes=(
            "bos_continuation",
        ),

        status=HypothesisStatus.PLANNED,

    ),

    # ------------------------------------------------------
    # EMA Slope
    # ------------------------------------------------------

    "ema20_trend": Hypothesis(

        id="HYP-003",

        title="EMA20 slope predicts trend continuation",

        description=(
            "Positive EMA20 slope increases "
            "the probability of continuation."
        ),

        features=(
            "ema20_slope",
        ),

        events=(
            "bos",
            "expansion_start",
        ),

        expected_outcomes=(
            "trend_continuation",
        ),

        status=HypothesisStatus.PLANNED,

    ),

    # ------------------------------------------------------
    # RSI
    # ------------------------------------------------------

    "rsi_reversal": Hypothesis(

        id="HYP-004",

        title="RSI predicts reversal",

        description=(
            "Extreme RSI values increase "
            "reversal probability."
        ),

        features=(
            "rsi_14",
        ),

        events=(
            "choch",
        ),

        expected_outcomes=(
            "trend_reversal",
        ),

        status=HypothesisStatus.PLANNED,

    ),

    # ------------------------------------------------------
    # Liquidity
    # ------------------------------------------------------

    "liquidity_sweep_reversal": Hypothesis(

        id="HYP-005",

        title="Liquidity sweep predicts reversal",

        description=(
            "Liquidity sweeps increase "
            "the probability of reversal."
        ),

        features=(
            "relative_volume_20",
            "atr_14",
        ),

        events=(
            "liquidity_sweep",
        ),

        expected_outcomes=(
            "trend_reversal",
        ),

        status=HypothesisStatus.PLANNED,

    ),

}


# ==========================================================
# Helper Functions
# ==========================================================

def get_hypothesis(
    hypothesis_name: str,
) -> Hypothesis:
    """
    Return metadata for a hypothesis.
    """

    return HYPOTHESES[hypothesis_name]


def list_hypotheses():
    """
    Return all hypothesis names.
    """

    return sorted(HYPOTHESES.keys())


def hypotheses_by_status(
    status: HypothesisStatus,
):
    """
    Return hypotheses having the given status.
    """

    return {

        name: hypothesis

        for name, hypothesis in HYPOTHESES.items()

        if hypothesis.status == status

    }


def hypotheses_by_feature(
    feature: str,
):
    """
    Return hypotheses using a feature.
    """

    return {

        name: hypothesis

        for name, hypothesis in HYPOTHESES.items()

        if feature in hypothesis.features

    }


def hypotheses_by_event(
    event: str,
):
    """
    Return hypotheses related to an event.
    """

    return {

        name: hypothesis

        for name, hypothesis in HYPOTHESES.items()

        if event in hypothesis.events

    }


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("HYPOTHESIS REGISTRY")
    print("=" * 60)

    print()

    print(
        f"Total Hypotheses : "
        f"{len(HYPOTHESES)}"
    )

    print()

    for hypothesis in list_hypotheses():

        print(hypothesis)