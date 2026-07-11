"""
==========================================================
Feature Engine
==========================================================

Purpose
-------
Application service responsible for computing every
registered deterministic market feature.

Responsibilities
----------------
- Accept raw OHLCV DataFrame
- Discover registered features
- Delegate computation to FeatureCalculator
- Return enriched DataFrame

This class is the public entry point to the Feature Engine.

The Research Framework should NEVER interact directly with

    - Feature Registry
    - Feature Calculator
    - Feature Dispatcher

==========================================================
"""

from __future__ import annotations

import pandas as pd

from .feature_calculator import FeatureCalculator
from .feature_dispatcher import FEATURE_DISPATCHER


# ==========================================================
# Feature Engine
# ==========================================================

class FeatureEngine:
    """
    Public execution engine for deterministic features.
    """

    def __init__(self) -> None:

        self.calculator = FeatureCalculator()

    # ======================================================
    # Public API
    # ======================================================

    def run(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Compute every implemented deterministic feature.
        """

        return self.calculator.compute(

            df=df,

            features=self.feature_names(),

        )

    # ======================================================
    # Registry
    # ======================================================

    @staticmethod
    def feature_names() -> list[str]:
        """
        Return every implemented feature.

        Uses the dispatcher rather than the registry because
        the registry also contains planned features that do
        not yet have implementations.
        """

        return list(FEATURE_DISPATCHER.keys())

    @staticmethod
    def total_features() -> int:
        """
        Number of implemented features.
        """

        return len(FEATURE_DISPATCHER)

    def available_features(
        self,
    ) -> tuple[str, ...]:

        return tuple(self.feature_names())

    # ======================================================
    # Convenience
    # ======================================================

    def available_features(
        self,
    ) -> tuple[str, ...]:

        return tuple(self.feature_names())


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FEATURE ENGINE")
    print("=" * 60)

    engine = FeatureEngine()

    print()

    print(
        f"Registered Features : "
        f"{engine.total_features()}"
    )

    print()

    print("Framework Ready ✓")