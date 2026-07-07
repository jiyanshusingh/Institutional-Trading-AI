"""
==========================================================
Feature Calculator
==========================================================

Purpose
-------
Central computation engine for deterministic market
features.

Responsibilities
----------------
- Accept market observations.
- Compute requested features.
- Return DataFrame with new feature columns.

This module does NOT contain:

- Trading logic
- Strategy logic
- AI
- Research
- Opportunity ranking

==========================================================
"""

from __future__ import annotations

import pandas as pd

from .feature_registry import FEATURES
from .validators import DataValidator
from .features.price import PriceFeatures
from .feature_dispatcher import FEATURE_DISPATCHER

# ==========================================================
# Feature Calculator
# ==========================================================

class FeatureCalculator:
    """
    Computes deterministic market features.
    """

    def __init__(self):

        self.available_features = tuple(FEATURES)

        self.validator = DataValidator()
    # ======================================================
    # Public API
    # ======================================================

    def compute(
        self,
        df: pd.DataFrame,
        features: list[str],
    ) -> pd.DataFrame:
        """
        Compute requested features.
        """

        df = df.copy()

        self.validator.validate(df)

        for feature in features:

            df = self._ensure_feature(
                df=df,
                feature=feature,
            )

        return df
    # ======================================================
    # Dispatcher
    # ======================================================

    def _dispatch(
        self,
        df,
        feature,
    ):

        if feature not in FEATURE_DISPATCHER:

            raise NotImplementedError(
                f"Feature '{feature}' has not been implemented."
            )

        return FEATURE_DISPATCHER[feature](df)

    # ======================================================
    # Dependency Resolver
    # ======================================================

    def _ensure_feature(
        self,
        df: pd.DataFrame,
        feature: str,
    ) -> pd.DataFrame:
        """
        Ensure that a feature exists.

        If already computed,
        return immediately.

        Otherwise compute it.
        """

        if self.has_feature(
            df,
            feature,
        ):
            return df

        return self._dispatch(
            df=df,
            feature=feature,
        )

    # ======================================================
    # Helper
    # ======================================================

    def has_feature(
        self,
        df: pd.DataFrame,
        feature: str,
    ) -> bool:
        """
        Check whether a feature
        has already been computed.
        """

        return feature in df.columns
    
    def _safe_divide(
        self,
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
# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FEATURE CALCULATOR")
    print("=" * 60)

    calculator = FeatureCalculator()

    print()

    print(
        f"Registered Features : "
        f"{len(calculator.available_features)}"
    )

    print()

    print("Framework Ready ✓")
