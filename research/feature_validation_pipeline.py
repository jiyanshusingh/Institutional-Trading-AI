"""
==========================================================
Feature Validation Pipeline
==========================================================

Purpose
-------
Runs the complete feature validation workflow.

Pipeline

Historical Data
        ↓
Target Builder
        ↓
Feature Validator
        ↓
Feature Ranking
        ↓
Validation Results

==========================================================
"""

from __future__ import annotations

import pandas as pd

from research.feature_ranker import FeatureRanker
from research.feature_validator import FeatureValidator
from research.target_builder import TargetBuilder
from research.target_definitions import TargetDefinition
from research.validation_result import ValidationResult


class FeatureValidationPipeline:
    """
    Complete feature validation pipeline.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        features: list[str],
        targets: list[TargetDefinition],
    ) -> None:

        self.df = df.copy()

        self.features = features

        self.targets = targets

    # ======================================================
    # Public API
    # ======================================================

    def run(
        self,
    ) -> list[ValidationResult]:
        """
        Execute complete validation pipeline.
        """

        # ----------------------------------------------
        # Step 1
        # Generate research targets
        # ----------------------------------------------

        dataset = TargetBuilder.build(

            self.df,

            self.targets,

        )

        validation_results: list[
            ValidationResult
        ] = []

        # ----------------------------------------------
        # Step 2
        # Validate every feature
        # ----------------------------------------------

        for target in self.targets:

            target_column = target.column_name

            for feature in self.features:

                result = FeatureValidator.validate(

                    df=dataset,

                    feature=feature,

                    target=target_column,

                )

                validation_results.append(
                    result
                )

        # ----------------------------------------------
        # Step 3
        # Rank all results
        # ----------------------------------------------

        ranked = FeatureRanker.rank(

            [

                statistic

                for validation in validation_results

                for statistic in validation.statistical_results

            ]

        )

        rank_lookup = {

            item["feature"]: item

            for item in ranked

        }

        # ----------------------------------------------
        # Step 4
        # Attach ranking
        # ----------------------------------------------

        for validation in validation_results:

            if validation.feature in rank_lookup:

                info = rank_lookup[
                    validation.feature
                ]

                validation.rank = info["rank"]

                validation.score = info["score"]

        return validation_results

    # ======================================================
    # Convenience
    # ======================================================

    def dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Execute pipeline and return results
        as a DataFrame.
        """

        results = self.run()

        return pd.DataFrame(

            [

                result.to_dict()

                for result in results

            ]

        )
# ==========================================================
# Execute Pipeline
# ==========================================================

if __name__ == "__main__":

    from pathlib import Path

    from feature_engine.feature_engine import FeatureEngine
    from research.feature_audit import FeatureAudit
    from research.target_definitions import TARGET_DEFINITIONS

    print("=" * 60)
    print("FEATURE VALIDATION PIPELINE")
    print("=" * 60)

    # ------------------------------------------------------
    # Load Dataset
    # ------------------------------------------------------

    dataset_path = Path("research/results/feature_dataset.csv")

    print("\nLoading dataset...")
    df = pd.read_csv(dataset_path)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    # ------------------------------------------------------
    # Feature List
    # ------------------------------------------------------

    feature_columns = FeatureAudit._feature_columns(df)

    print(f"Features : {len(feature_columns)}")

    # ------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------

    pipeline = FeatureValidationPipeline(

        df=df,

        features=feature_columns,

        targets=TARGET_DEFINITIONS,

    )

    print("\nRunning validation...")

    results = pipeline.dataframe()

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    output_dir = Path("research/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    validation_file = output_dir / "validation_results.csv"
    ranking_file = output_dir / "feature_ranking.csv"

    results.to_csv(
        validation_file,
        index=False,
    )

    ranking = (
        results[
            ["feature", "rank", "score", "status"]
        ]
        .drop_duplicates()
        .sort_values("rank")
    )

    ranking.to_csv(
        ranking_file,
        index=False,
    )

    print("\nDone.")
    print(f"\nValidation : {validation_file}")
    print(f"Ranking    : {ranking_file}")