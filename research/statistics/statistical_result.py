"""
==========================================================
Statistical Result
==========================================================

Purpose
-------
Represents the result of a statistical test.

Every statistical test in the Research Engine returns a
StatisticalResult.

Examples
--------
Pearson Correlation

Mutual Information

Mann-Whitney U

ROC AUC

Information Value

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# ==========================================================
# Statistical Test Types
# ==========================================================

class StatisticalTestType(Enum):

    PEARSON = "Pearson Correlation"

    SPEARMAN = "Spearman Correlation"

    KENDALL = "Kendall Correlation"

    MUTUAL_INFORMATION = "Mutual Information"

    INFORMATION_VALUE = "Information Value"

    MANN_WHITNEY = "Mann-Whitney U"

    KOLMOGOROV_SMIRNOV = "Kolmogorov-Smirnov"

    ROC_AUC = "ROC AUC"

    PRECISION = "Precision"

    RECALL = "Recall"

    F1_SCORE = "F1 Score"

    LOGISTIC_REGRESSION = "Logistic Regression"

    LINEAR_REGRESSION = "Linear Regression"


# ==========================================================
# Statistical Result
# ==========================================================

@dataclass
class StatisticalResult:
    """
    Result of a statistical test.
    """

    # ---------------------------------------------
    # Test Information
    # ---------------------------------------------

    test: StatisticalTestType

    feature: str

    target: str

    # ---------------------------------------------
    # Primary Statistics
    # ---------------------------------------------

    statistic: float

    p_value: float | None = None

    effect_size: float | None = None

    confidence_level: float = 0.95

    significant: bool = False

    # ---------------------------------------------
    # Sample Information
    # ---------------------------------------------

    sample_size: int = 0

    positive_samples: int = 0

    negative_samples: int = 0

    # ---------------------------------------------
    # Metadata
    # ---------------------------------------------

    timestamp: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ======================================================
    # Helper Methods
    # ======================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store additional information.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    def is_significant(
        self,
        alpha: float = 0.05,
    ) -> bool:
        """
        Determine statistical significance.
        """

        if self.p_value is None:
            return self.significant

        return self.p_value < alpha

    def to_dict(self) -> dict:
        """
        Serialize the result.
        """

        return {

            "test": self.test.value,

            "feature": self.feature,

            "target": self.target,

            "statistic": self.statistic,

            "p_value": self.p_value,

            "effect_size": self.effect_size,

            "confidence_level": self.confidence_level,

            "significant": self.significant,

            "sample_size": self.sample_size,

            "positive_samples": self.positive_samples,

            "negative_samples": self.negative_samples,

            "timestamp": self.timestamp,

            "metadata": self.metadata,

        }

    def __str__(self) -> str:

        return (
            f"{self.test.value}("
            f"feature={self.feature}, "
            f"target={self.target}, "
            f"statistic={self.statistic:.6f}, "
            f"p_value={self.p_value}, "
            f"significant={self.significant})"
        )