"""
==========================================================
Volume Features
==========================================================

Purpose
-------
Deterministic volume feature computations.

This module contains NO:

- Trading logic
- AI
- Strategy logic
- Research

Only mathematical feature computation.

==========================================================
"""

from __future__ import annotations

import pandas as pd


class VolumeFeatures:
    """
    Deterministic volume features.
    """

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _safe_divide(
        numerator: pd.Series,
        denominator: pd.Series,
    ) -> pd.Series:
        """
        Safe division.

        Division by zero returns NA.
        """

        return numerator / denominator.replace(
            0,
            pd.NA,
        )

    # ======================================================
    # Raw Volume
    # ======================================================

    @staticmethod
    def volume(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Copy raw traded volume.

        Added for naming consistency.
        """

        df["volume"] = df["volume"]

        return df

    # ======================================================
    # Volume Moving Average
    # ======================================================

    @staticmethod
    def volume_ma20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        20-period average volume.
        """

        df["volume_ma20"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )

        return df

    @staticmethod
    def volume_ma50(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        50-period average volume.
        """

        df["volume_ma50"] = (
            df["volume"]
            .rolling(50)
            .mean()
        )

        return df

    # ======================================================
    # Relative Volume
    # ======================================================

    @staticmethod
    def relative_volume(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Current Volume / 20-period Average Volume
        """

        if "volume_ma20" not in df.columns:

            df = VolumeFeatures.volume_ma20(df)

        df["relative_volume"] = (
            VolumeFeatures._safe_divide(
                df["volume"],
                df["volume_ma20"],
            )
        )

        return df

    # ======================================================
    # Volume Change
    # ======================================================

    @staticmethod
    def volume_change(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Percentage change in volume.
        """

        df["volume_change"] = (
            df["volume"]
            .pct_change()
        )

        return df

    # ======================================================
    # Volume Z-Score
    # ======================================================

    @staticmethod
    def volume_zscore(
        df: pd.DataFrame,
        window: int = 20,
    ) -> pd.DataFrame:
        """
        Rolling Z-score of volume.
        """

        mean = (
            df["volume"]
            .rolling(window)
            .mean()
        )

        std = (
            df["volume"]
            .rolling(window)
            .std()
        )

        df["volume_zscore"] = (
            VolumeFeatures._safe_divide(
                df["volume"] - mean,
                std,
            )
        )

        return df

    # ======================================================
    # Volume Percentile
    # ======================================================

    @staticmethod
    def volume_percentile(
        df: pd.DataFrame,
        window: int = 100,
    ) -> pd.DataFrame:
        """
        Rolling percentile rank of volume.
        """

        df["volume_percentile"] = (
            df["volume"]
            .rolling(window)
            .rank(pct=True)
        )

        return df

    # ======================================================
    # High Volume Candle
    # ======================================================

    @staticmethod
    def high_volume_candle(
        df: pd.DataFrame,
        threshold: float = 2.0,
    ) -> pd.DataFrame:
        """
        High-volume flag based on Relative Volume.
        """

        if "relative_volume" not in df.columns:

            df = VolumeFeatures.relative_volume(df)

        df["high_volume_candle"] = (
            df["relative_volume"] >= threshold
        )

        return df

    # ======================================================
    # Low Volume Candle
    # ======================================================

    @staticmethod
    def low_volume_candle(
        df: pd.DataFrame,
        threshold: float = 0.5,
    ) -> pd.DataFrame:
        """
        Low-volume flag based on Relative Volume.
        """

        if "relative_volume" not in df.columns:

            df = VolumeFeatures.relative_volume(df)

        df["low_volume_candle"] = (
            df["relative_volume"] <= threshold
        )

        return df