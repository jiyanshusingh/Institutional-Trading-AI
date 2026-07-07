"""
==========================================================
Feature Utilities
==========================================================

Shared utility functions used across all feature modules.

These utilities are domain-independent and reusable.

This module contains NO feature computation.

==========================================================
"""

from __future__ import annotations

import pandas as pd


class FeatureUtils:
    """
    Common utilities for feature computation.
    """

    # ======================================================
    # Safe Math
    # ======================================================

    @staticmethod
    def safe_divide(
        numerator: pd.Series,
        denominator: pd.Series,
    ) -> pd.Series:
        """
        Safely divide two Series.

        Division by zero returns NA.
        """

        return numerator / denominator.replace(
            0,
            pd.NA,
        )

    # ======================================================
    # Rolling Helpers
    # ======================================================

    @staticmethod
    def rolling_mean(
        series: pd.Series,
        window: int,
    ) -> pd.Series:
        """
        Rolling mean.
        """

        return (
            series
            .rolling(window)
            .mean()
        )

    @staticmethod
    def rolling_sum(
        series: pd.Series,
        window: int,
    ) -> pd.Series:
        """
        Rolling sum.
        """

        return (
            series
            .rolling(window)
            .sum()
        )

    @staticmethod
    def rolling_max(
        series: pd.Series,
        window: int,
    ) -> pd.Series:
        """
        Rolling maximum.
        """

        return (
            series
            .rolling(window)
            .max()
        )

    @staticmethod
    def rolling_min(
        series: pd.Series,
        window: int,
    ) -> pd.Series:
        """
        Rolling minimum.
        """

        return (
            series
            .rolling(window)
            .min()
        )

    @staticmethod
    def rolling_std(
        series: pd.Series,
        window: int,
    ) -> pd.Series:
        """
        Rolling standard deviation.
        """

        return (
            series
            .rolling(window)
            .std()
        )

    # ======================================================
    # Previous Values
    # ======================================================

    @staticmethod
    def previous(
        series: pd.Series,
        periods: int = 1,
    ) -> pd.Series:
        """
        Previous values.
        """

        return series.shift(periods)

    # ======================================================
    # Absolute Value
    # ======================================================

    @staticmethod
    def absolute(
        series: pd.Series,
    ) -> pd.Series:
        """
        Absolute value.
        """

        return series.abs()