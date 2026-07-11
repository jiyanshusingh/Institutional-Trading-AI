"""
==========================================================
Correlation Statistics
==========================================================

Purpose
-------
Correlation-based statistical tests.

Implements

- Pearson Correlation
- Spearman Rank Correlation
- Kendall Tau Correlation

All methods return StatisticalResult.

==========================================================
"""

from __future__ import annotations

import pandas as pd

from scipy.stats import kendalltau
from scipy.stats import pearsonr
from scipy.stats import spearmanr

from research.statistics.statistical_result import (
    StatisticalResult,
    StatisticalTestType,
)


class Correlation:
    """
    Correlation statistical tests.
    """

    # ======================================================
    # Pearson
    # ======================================================

    @staticmethod
    def pearson(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        statistic, p_value = pearsonr(
            data[feature],
            data[target],
        )

        return StatisticalResult(

            test=StatisticalTestType.PEARSON,

            feature=feature,

            target=target,

            statistic=float(statistic),

            p_value=float(p_value),

            significant=p_value < 0.05,

            sample_size=len(data),

        )

    # ======================================================
    # Spearman
    # ======================================================

    @staticmethod
    def spearman(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        statistic, p_value = spearmanr(
            data[feature],
            data[target],
        )

        return StatisticalResult(

            test=StatisticalTestType.SPEARMAN,

            feature=feature,

            target=target,

            statistic=float(statistic),

            p_value=float(p_value),

            significant=p_value < 0.05,

            sample_size=len(data),

        )

    # ======================================================
    # Kendall Tau
    # ======================================================

    @staticmethod
    def kendall(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        statistic, p_value = kendalltau(
            data[feature],
            data[target],
        )

        return StatisticalResult(

            test=StatisticalTestType.KENDALL,

            feature=feature,

            target=target,

            statistic=float(statistic),

            p_value=float(p_value),

            significant=p_value < 0.05,

            sample_size=len(data),

        )

    # ======================================================
    # Convenience
    # ======================================================

    @staticmethod
    def evaluate(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> list[StatisticalResult]:
        """
        Execute all correlation tests.
        """

        return [

            Correlation.pearson(
                df,
                feature,
                target,
            ),

            Correlation.spearman(
                df,
                feature,
                target,
            ),

            Correlation.kendall(
                df,
                feature,
                target,
            ),

        ]