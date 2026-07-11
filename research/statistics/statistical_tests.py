"""
==========================================================
Statistical Tests
==========================================================

Purpose
-------
Facade for all statistical tests used by the Research
Engine.

This module DOES NOT implement statistical algorithms.

It delegates to specialized statistical modules.

==========================================================
"""

from __future__ import annotations

import pandas as pd

from .correlation import Correlation
from .information import Information
from .hypothesis_tests import HypothesisTests
from .classification import ClassificationMetrics
from .regression import RegressionAnalysis


class StatisticalTests:
    """
    Unified interface for statistical analysis.
    """

    # ======================================================
    # Correlation
    # ======================================================

    @staticmethod
    def pearson(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> float:

        return Correlation.pearson(
            df,
            feature,
            target,
        )

    @staticmethod
    def spearman(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> float:

        return Correlation.spearman(
            df,
            feature,
            target,
        )

    @staticmethod
    def kendall(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> float:

        return Correlation.kendall(
            df,
            feature,
            target,
        )

    # ======================================================
    # Information Theory
    # ======================================================

    @staticmethod
    def mutual_information(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> float:

        return Information.mutual_information(
            df,
            feature,
            target,
        )

    @staticmethod
    def information_value(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> float:

        return Information.information_value(
            df,
            feature,
            target,
        )

    # ======================================================
    # Hypothesis Tests
    # ======================================================

    @staticmethod
    def mann_whitney(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ):

        return HypothesisTests.mann_whitney(
            df,
            feature,
            target,
        )

    @staticmethod
    def kolmogorov_smirnov(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ):

        return HypothesisTests.kolmogorov_smirnov(
            df,
            feature,
            target,
        )

    # ======================================================
    # Classification
    # ======================================================

    @staticmethod
    def roc_auc(
        y_true,
        y_score,
    ):

        return ClassificationMetrics.roc_auc(
            y_true,
            y_score,
        )

    @staticmethod
    def precision(
        y_true,
        y_pred,
    ):

        return ClassificationMetrics.precision(
            y_true,
            y_pred,
        )

    @staticmethod
    def recall(
        y_true,
        y_pred,
    ):

        return ClassificationMetrics.recall(
            y_true,
            y_pred,
        )

    @staticmethod
    def f1_score(
        y_true,
        y_pred,
    ):

        return ClassificationMetrics.f1_score(
            y_true,
            y_pred,
        )

    # ======================================================
    # Regression
    # ======================================================

    @staticmethod
    def logistic_regression(
        X,
        y,
    ):

        return RegressionAnalysis.logistic_regression(
            X,
            y,
        )

    @staticmethod
    def linear_regression(
        X,
        y,
    ):

        return RegressionAnalysis.linear_regression(
            X,
            y,
        )

    # ======================================================
    # Full Feature Report
    # ======================================================

    @staticmethod
    def evaluate_feature(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> dict:
        """
        Execute all applicable statistical tests for
        one feature against one target.
        """

        return {

            "pearson":
                StatisticalTests.pearson(
                    df,
                    feature,
                    target,
                ),

            "spearman":
                StatisticalTests.spearman(
                    df,
                    feature,
                    target,
                ),

            "kendall":
                StatisticalTests.kendall(
                    df,
                    feature,
                    target,
                ),

            "mutual_information":
                StatisticalTests.mutual_information(
                    df,
                    feature,
                    target,
                ),

            "information_value":
                StatisticalTests.information_value(
                    df,
                    feature,
                    target,
                ),

            "mann_whitney":
                StatisticalTests.mann_whitney(
                    df,
                    feature,
                    target,
                ),

            "kolmogorov_smirnov":
                StatisticalTests.kolmogorov_smirnov(
                    df,
                    feature,
                    target,
                ),

        }