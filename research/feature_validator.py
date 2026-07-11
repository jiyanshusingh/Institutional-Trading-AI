"""
==========================================================
Feature Validator
==========================================================

Purpose
-------
Validates one feature against one research target.

Runs all statistical tests and produces one
ValidationResult.

No feature ranking.
No report generation.
No file I/O.

==========================================================
"""

from __future__ import annotations

import pandas as pd

from research.feature_ranker import FeatureRanker
from research.validation_result import ValidationResult

from research.statistics.correlation import Correlation
from research.statistics.information import Information


class FeatureValidator:
    """
    Validates one feature.
    """

    # ======================================================
    # Public API
    # ======================================================

    @staticmethod
    def validate(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> ValidationResult:
        """
        Validate one feature against one target.
        """

        FeatureValidator._validate_inputs(

            df,

            feature,

            target,

        )

        validation = ValidationResult(

            feature=feature,

            target=target,

        )

        # --------------------------------------------------
        # Correlation
        # --------------------------------------------------

        for result in Correlation.evaluate(

            df,

            feature,

            target,

        ):

            validation.add_result(

                result,

            )

        # --------------------------------------------------
        # Information Theory
        # --------------------------------------------------

        validation.add_result(

            Information.mutual_information(

                df,

                feature,

                target,

            )

        )
        # --------------------------------------------------
        # Hypothesis Tests
        # --------------------------------------------------

        # --------------------------------------------------
        # Overall Score
        # --------------------------------------------------

        validation.score = (

            FeatureRanker.score_feature(

                validation.statistical_results,

            )

        )

        validation.confidence = (

            validation.significance_ratio

        )

        validation.status = (

            FeatureValidator._status(

                validation.score,

            )

        )

        return validation

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _validate_inputs(

        df: pd.DataFrame,

        feature: str,

        target: str,

    ) -> None:

        if feature not in df.columns:

            raise ValueError(

                f"Feature '{feature}' "

                "not found."

            )

        if target not in df.columns:

            raise ValueError(

                f"Target '{target}' "

                "not found."

            )

    @staticmethod
    def _status(
        score: float,
    ) -> str:
        """
        Research status.
        """

        if score >= 0.80:

            return "CORE"

        if score >= 0.60:

            return "VALIDATED"

        if score >= 0.40:

            return "PROMISING"

        if score >= 0.20:

            return "WEAK"

        return "REJECTED"