"""
==========================================================
Volume Features
==========================================================

Deterministic volume-based market features.

No trading logic.
No AI.
No research.
==========================================================
"""

from __future__ import annotations

import pandas as pd
from feature_engine.features.utils import FeatureUtils

class VolumeFeatures:

    # ======================================================
    # Helper
    # ======================================================
    # ======================================================
    # Base Features
    # ======================================================

    @staticmethod
    def volume(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Raw traded volume.
        """

        df["volume"] = df["volume"]

        return df

    @staticmethod
    def cumulative_volume(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Running cumulative traded volume.
        """

        df["cumulative_volume"] = (
            df["volume"].cumsum()
        )

        return df

    # ======================================================
    # Delta Features
    # ======================================================

    @staticmethod
    def volume_change(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Current volume minus previous volume.
        """

        df["volume_change"] = (
            df["volume"].diff()
        )

        return df

    @staticmethod
    def volume_change_percent(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Percentage change in volume.
        """

        if "volume_change" not in df.columns:
            df = VolumeFeatures.volume_change(df)

        previous_volume = (
            df["volume"].shift(1)
        )

        df["volume_change_percent"] = (
            FeatureUtils.safe_divide(
                df["volume_change"],
                previous_volume,
            )
            * 100
        )

        return df

    # ======================================================
    # Moving Averages
    # ======================================================

    @staticmethod
    def volume_ma_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        5-period volume average.
        """

        df["volume_ma_5"] = (
            df["volume"]
            .rolling(5)
            .mean()
        )

        return df

    @staticmethod
    def volume_ma_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        10-period volume average.
        """

        df["volume_ma_10"] = (
            df["volume"]
            .rolling(10)
            .mean()
        )

        return df

    @staticmethod
    def volume_ma_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        20-period volume average.
        """

        df["volume_ma_20"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )

        return df

    # ======================================================
    # Relative Volume
    # ======================================================

    @staticmethod
    def relative_volume_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Current volume / 5-period average.
        """

        if "volume_ma_5" not in df.columns:
            df = VolumeFeatures.volume_ma_5(df)

        df["relative_volume_5"] = (
            FeatureUtils.safe_divide(
                df["volume"],
                df["volume_ma_5"],
            )
        )

        return df

    @staticmethod
    def relative_volume_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Current volume / 10-period average.
        """

        if "volume_ma_10" not in df.columns:
            df = VolumeFeatures.volume_ma_10(df)

        df["relative_volume_10"] = (
            FeatureUtils.safe_divide(
                df["volume"],
                df["volume_ma_10"],
            )
        )

        return df

    @staticmethod
    def relative_volume_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Current volume / 20-period average.
        """

        if "volume_ma_20" not in df.columns:
            df = VolumeFeatures.volume_ma_20(df)

        df["relative_volume_20"] = (
            FeatureUtils.safe_divide(
                df["volume"],
                df["volume_ma_20"],
            )
        )

        return df