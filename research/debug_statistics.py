"""
==========================================================
Debug Statistics
==========================================================

Purpose
-------
Runs one feature against one target to verify that every
statistical module produces sensible results.

Pipeline

Feature Dataset
        ↓
Correlation
        ↓
Information
        ↓
Hypothesis Tests

==========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from research.statistics.correlation import Correlation
from research.statistics.information import Information
from research.statistics.hypothesis_tests import HypothesisTests
from sklearn.feature_selection import mutual_info_regression


# ==========================================================
# Configuration
# ==========================================================

DATASET = Path(
    "research/results/feature_dataset.csv"
)

FEATURE = "atr_14"

TARGET = "forward_return_10"


# ==========================================================
# Main
# ==========================================================

def main() -> None:

    print("=" * 60)
    print("LOAD DATASET")
    print("=" * 60)

    df = pd.read_csv(DATASET)

    print(df.shape)
    print()

    # ------------------------------------------------------
    # Keep only valid rows
    # ------------------------------------------------------

    data = df[[FEATURE, TARGET]].dropna()

    print(f"Rows Used : {len(data):,}")
    print()

    x = data[FEATURE]

    y = data[TARGET]

    # ======================================================
    # Correlation
    # ======================================================

    print("=" * 60)
    print("CORRELATION")
    print("=" * 60)

    correlation_results = Correlation.evaluate(
        df=data,
        feature=FEATURE,
        target=TARGET,
    )

    for result in correlation_results:

        print(result)

        print("-" * 60)

    # ======================================================
    # Information
    # ======================================================

    print()
    print("=" * 60)
    print("INFORMATION")
    print("=" * 60)

    information_results = Information.evaluate(
        df=data,
        feature=FEATURE,
        target=TARGET,
    )

    for result in information_results:

        print(result)

        print("-" * 60)

    # ======================================================
    # Hypothesis Tests
    # ======================================================

    print()
    print("=" * 60)
    print("HYPOTHESIS TESTS")
    print("=" * 60)

    hypothesis_results = HypothesisTests.compute(
        feature=x,
        target=y,
    )

    for result in hypothesis_results:

        print(result)

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()