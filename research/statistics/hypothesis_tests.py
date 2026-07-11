"""
==========================================================
Hypothesis Tests
==========================================================

Purpose
-------
Hypothesis testing for feature validation.

Implements

- Mann-Whitney U Test
- Kolmogorov-Smirnov Test

All methods return StatisticalResult.

==========================================================
"""

from __future__ import annotations

import pandas as pd

from scipy.stats import ks_2samp
from scipy.stats import mannwhitneyu

from research.statistics.statistical_result import (
    StatisticalResult,
    StatisticalTestType,
)


class HypothesisTests:
    """
    Statistical hypothesis tests.
    """

    # ======================================================
    # Mann-Whitney U
    # ======================================================

    @staticmethod
    def mann_whitney(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        if data.empty:

            return StatisticalResult(

                test=StatisticalTestType.MANN_WHITNEY,

                feature=feature,

                target=target,

                statistic=0.0,

                sample_size=0,

            )

        groups = data.groupby(target)

        if len(groups) != 2:

            raise ValueError(
                "Mann-Whitney requires exactly "
                "two target classes."
            )

        values = [
            group[feature].values
            for _, group in groups
        ]

        statistic, p_value = mannwhitneyu(

            values[0],

            values[1],

            alternative="two-sided",

        )

        result = StatisticalResult(

            test=StatisticalTestType.MANN_WHITNEY,

            feature=feature,

            target=target,

            statistic=float(statistic),

            p_value=float(p_value),

            significant=p_value < 0.05,

            sample_size=len(data),

            positive_samples=len(values[1]),

            negative_samples=len(values[0]),

        )

        result.add_metadata(

            "interpretation",

            HypothesisTests._interpret_pvalue(
                p_value,
            ),

        )

        return result

    # ======================================================
    # Kolmogorov-Smirnov
    # ======================================================

    @staticmethod
    def kolmogorov_smirnov(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        if data.empty:

            return StatisticalResult(

                test=StatisticalTestType.KOLMOGOROV_SMIRNOV,

                feature=feature,

                target=target,

                statistic=0.0,

                sample_size=0,

            )

        groups = data.groupby(target)

        if len(groups) != 2:

            raise ValueError(
                "Kolmogorov-Smirnov requires "
                "exactly two target classes."
            )

        values = [
            group[feature].values
            for _, group in groups
        ]

        statistic, p_value = ks_2samp(

            values[0],

            values[1],

        )

        result = StatisticalResult(

            test=StatisticalTestType.KOLMOGOROV_SMIRNOV,

            feature=feature,

            target=target,

            statistic=float(statistic),

            p_value=float(p_value),

            significant=p_value < 0.05,

            sample_size=len(data),

            positive_samples=len(values[1]),

            negative_samples=len(values[0]),

        )

        result.add_metadata(

            "interpretation",

            HypothesisTests._interpret_pvalue(
                p_value,
            ),

        )

        return result

    # ======================================================
    # Convenience
    # ======================================================

    @staticmethod
    def evaluate(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> list[StatisticalResult]:

        return [

            HypothesisTests.mann_whitney(

                df,

                feature,

                target,

            ),

            HypothesisTests.kolmogorov_smirnov(

                df,

                feature,

                target,

            ),

        ]

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _interpret_pvalue(
        p_value: float,
    ) -> str:

        if p_value < 0.001:
            return "Very Strong Evidence"

        if p_value < 0.01:
            return "Strong Evidence"

        if p_value < 0.05:
            return "Statistically Significant"

        return "Not Significant"
    