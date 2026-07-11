"""
==========================================================
Information Statistics
==========================================================

Purpose
-------
Information-theoretic statistical tests.

Implements

- Mutual Information
- Information Value (IV)

All methods return StatisticalResult.

==========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.feature_selection import mutual_info_classif

from research.statistics.statistical_result import (
    StatisticalResult,
    StatisticalTestType,
)
from sklearn.feature_selection import mutual_info_regression

class Information:
    """
    Information-theoretic statistical tests.
    """

    # ======================================================
    # Mutual Information
    # ======================================================

    @staticmethod
    def mutual_information(
        df: pd.DataFrame,
        feature: str,
        target: str,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        X = data[[feature]]

        y = data[target]

        mi = mutual_info_regression(
            X,
            y,
            discrete_features=False,
            random_state=42,
        )[0]
        result = StatisticalResult(

            test=StatisticalTestType.MUTUAL_INFORMATION,

            feature=feature,

            target=target,

            statistic=float(mi),

            sample_size=len(data),

        )

        result.add_metadata(

            "strength",

            Information._mi_strength(mi),

        )

        return result

    # ======================================================
    # Information Value
    # ======================================================

    @staticmethod
    def information_value(
        df: pd.DataFrame,
        feature: str,
        target: str,
        bins: int = 10,
    ) -> StatisticalResult:

        data = df[
            [feature, target]
        ].dropna()

        if data.empty:

            return StatisticalResult(

                test=StatisticalTestType.INFORMATION_VALUE,

                feature=feature,

                target=target,

                statistic=0.0,

                sample_size=0,

            )

        data = data.copy()

        data["bin"] = pd.qcut(

            data[feature],

            q=bins,

            duplicates="drop",

        )

        grouped = data.groupby(

            "bin",

            observed=False,

        )

        total_good = (data[target] == 0).sum()

        total_bad = (data[target] == 1).sum()

        iv = 0.0

        epsilon = 1e-10

        for _, group in grouped:

            good = (group[target] == 0).sum()

            bad = (group[target] == 1).sum()

            dist_good = max(

                good / max(total_good, 1),

                epsilon,

            )

            dist_bad = max(

                bad / max(total_bad, 1),

                epsilon,

            )

            woe = np.log(

                dist_good / dist_bad

            )

            iv += (

                dist_good - dist_bad

            ) * woe

        result = StatisticalResult(

            test=StatisticalTestType.INFORMATION_VALUE,

            feature=feature,

            target=target,

            statistic=float(iv),

            sample_size=len(data),

        )

        result.add_metadata(

            "predictive_power",

            Information._iv_strength(iv),

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

            Information.mutual_information(

                df,

                feature,

                target,

            ),

            Information.information_value(

                df,

                feature,

                target,

            ),

        ]

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _mi_strength(
        value: float,
    ) -> str:

        if value < 0.05:
            return "Negligible"

        if value < 0.10:
            return "Weak"

        if value < 0.20:
            return "Moderate"

        return "Strong"

    @staticmethod
    def _iv_strength(
        value: float,
    ) -> str:

        if value < 0.02:
            return "Not Predictive"

        if value < 0.10:
            return "Weak"

        if value < 0.30:
            return "Medium"

        if value < 0.50:
            return "Strong"

        return "Suspicious"