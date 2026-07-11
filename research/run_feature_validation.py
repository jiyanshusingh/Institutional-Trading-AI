"""
==========================================================
Run Feature Validation
==========================================================

Purpose
-------
Executes the complete feature validation workflow.

Pipeline

CSV
    ↓
Feature Calculator
    ↓
Target Builder
    ↓
Feature Validation Pipeline
    ↓
CSV Report

==========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from feature_engine.feature_calculator import (
    FeatureCalculator,
)

from feature_engine.feature_registry import (
    FEATURES,
)

from research.feature_validation_pipeline import (
    FeatureValidationPipeline,
)

from research.target_definitions import (
    TARGET_DEFINITIONS,
)


# ==========================================================
# Configuration
# ==========================================================

DATA_FILE = Path(
    "historical_data/normalized/ACUTAAS_1m.csv"
)

OUTPUT_DIR = Path(
    "research/results"
)

FEATURE_DATASET = OUTPUT_DIR / "feature_dataset.csv"

VALIDATION_REPORT = OUTPUT_DIR / "validation_report.csv"


# ==========================================================
# Main
# ==========================================================

def main() -> None:

    print("=" * 60)
    print("Loading Historical Data")
    print("=" * 60)

    df = pd.read_csv(
        DATA_FILE,
        parse_dates=["timestamp"],
    )

    print(f"Rows      : {len(df):,}")
    print(f"Columns   : {len(df.columns)}")

    # ------------------------------------------------------
    # Feature Calculation
    # ------------------------------------------------------

    print()
    print("=" * 60)
    print("Calculating Features")
    print("=" * 60)

    calculator = FeatureCalculator()

    feature_df = calculator.calculate(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    feature_df.to_csv(
        FEATURE_DATASET,
        index=False,
    )

    print("Feature dataset saved.")

    # ------------------------------------------------------
    # Features
    # ------------------------------------------------------

    features = [

        feature.name

        for feature in FEATURES

        if feature.name in feature_df.columns

    ]

    print()

    print(f"Features Available : {len(features)}")

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    print()
    print("=" * 60)
    print("Running Validation")
    print("=" * 60)

    pipeline = FeatureValidationPipeline(

        df=feature_df,

        features=features,

        targets=list(
            TARGET_DEFINITIONS
        ),

    )

    report = pipeline.dataframe()

    report.to_csv(

        VALIDATION_REPORT,

        index=False,

    )

    print()
    print("=" * 60)
    print("Validation Complete")
    print("=" * 60)

    print(f"Rows analysed     : {len(feature_df):,}")
    print(f"Features tested   : {len(features)}")
    print(f"Targets generated : {len(TARGET_DEFINITIONS)}")
    print()
    print("Top Results")
    print(
        report.sort_values(
            "score",
            ascending=False,
        ).head(20)
    )

    print()
    print("Feature Dataset")
    print(FEATURE_DATASET)

    print()

    print("Validation Report")
    print(VALIDATION_REPORT)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()