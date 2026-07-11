"""
==========================================================
Feature Ranker
==========================================================

Purpose
-------
Ranks features using the statistical evidence produced
during research.

FeatureRanker NEVER computes statistics.

It only consumes StatisticalResult objects.

==========================================================
"""

from __future__ import annotations

from collections import defaultdict

from research.statistics.statistical_result import (
    StatisticalResult,
    StatisticalTestType,
)


class FeatureRanker:
    """
    Rank features by combining multiple statistical tests.
    """

    # ------------------------------------------------------
    # Weights
    # ------------------------------------------------------

    WEIGHTS = {

        StatisticalTestType.PEARSON: 1.0,

        StatisticalTestType.SPEARMAN: 1.0,

        StatisticalTestType.KENDALL: 1.0,

        StatisticalTestType.MUTUAL_INFORMATION: 2.0,

        StatisticalTestType.INFORMATION_VALUE: 2.0,

        StatisticalTestType.MANN_WHITNEY: 1.5,

        StatisticalTestType.KOLMOGOROV_SMIRNOV: 1.5,

    }

    # ======================================================
    # Rank
    # ======================================================

    @classmethod
    def rank(
        cls,
        results: list[StatisticalResult],
    ) -> list[dict]:
        """
        Rank all features.

        Returns
        -------
        List sorted by descending score.
        """

        grouped = defaultdict(list)

        for result in results:

            grouped[result.feature].append(result)

        ranking = []

        for feature, feature_results in grouped.items():

            score = cls.score_feature(
                feature_results
            )

            ranking.append({

                "feature": feature,

                "score": score,

                "tests": len(feature_results),

                "results": feature_results,

            })

        ranking.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        for rank, item in enumerate(

            ranking,

            start=1,

        ):

            item["rank"] = rank

        return ranking

    # ======================================================
    # Score
    # ======================================================

    @classmethod
    def score_feature(
        cls,
        results: list[StatisticalResult],
    ) -> float:
        """
        Calculate weighted score.
        """

        weighted_score = 0.0

        total_weight = 0.0

        for result in results:

            weight = cls.WEIGHTS.get(

                result.test,

                1.0,

            )

            value = cls.normalize(

                result,

            )

            weighted_score += (

                weight * value

            )

            total_weight += weight

        if total_weight == 0:

            return 0.0

        return weighted_score / total_weight

    # ======================================================
    # Normalize
    # ======================================================

    @staticmethod
    def normalize(
        result: StatisticalResult,
    ) -> float:
        """
        Convert every statistical result
        into a comparable score between 0 and 1.
        """

        value = abs(result.statistic)

        if result.test in (

            StatisticalTestType.PEARSON,

            StatisticalTestType.SPEARMAN,

            StatisticalTestType.KENDALL,

        ):

            return min(

                value,

                1.0,

            )

        if result.test == StatisticalTestType.MUTUAL_INFORMATION:

            return min(

                value,

                1.0,

            )

        if result.test == StatisticalTestType.INFORMATION_VALUE:

            return min(

                value / 0.5,

                1.0,

            )

        if result.test in (

            StatisticalTestType.MANN_WHITNEY,

            StatisticalTestType.KOLMOGOROV_SMIRNOV,

        ):

            return 1.0 if result.significant else 0.0

        return 0.0

    # ======================================================
    # Best Feature
    # ======================================================

    @classmethod
    def best_feature(
        cls,
        results: list[StatisticalResult],
    ) -> dict | None:

        ranking = cls.rank(results)

        if not ranking:

            return None

        return ranking[0]