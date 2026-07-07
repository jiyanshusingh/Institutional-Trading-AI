"""
==========================================================
Volatility Features
==========================================================

Deterministic volatility-based market features.

No trading logic.
No AI.
No research.
==========================================================
"""

from __future__ import annotations

import pandas as pd
from feature_engine.features.utils import FeatureUtils


class VolatilityFeatures:
    # ======================================================
    # Base Features
    # ======================================================

    @staticmethod
    def true_range(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        True Range.

        max(
            High - Low,
            |High - Previous Close|,
            |Low - Previous Close|
        )
        """

        previous_close = df["close"].shift(1)

        range1 = df["high"] - df["low"]

        range2 = (
            df["high"] - previous_close
        ).abs()

        range3 = (
            df["low"] - previous_close
        ).abs()

        df["true_range"] = pd.concat(
            [
                range1,
                range2,
                range3,
            ],
            axis=1,
        ).max(axis=1)

        return df

    # ======================================================
    # ATR
    # ======================================================

    @staticmethod
    def atr_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "true_range" not in df.columns:
            df = VolatilityFeatures.true_range(df)

        df["atr_5"] = (
            df["true_range"]
            .rolling(5)
            .mean()
        )

        return df

    @staticmethod
    def atr_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "true_range" not in df.columns:
            df = VolatilityFeatures.true_range(df)

        df["atr_10"] = (
            df["true_range"]
            .rolling(10)
            .mean()
        )

        return df

    @staticmethod
    def atr_14(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "true_range" not in df.columns:
            df = VolatilityFeatures.true_range(df)

        df["atr_14"] = (
            df["true_range"]
            .rolling(14)
            .mean()
        )

        return df

    @staticmethod
    def atr_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "true_range" not in df.columns:
            df = VolatilityFeatures.true_range(df)

        df["atr_20"] = (
            df["true_range"]
            .rolling(20)
            .mean()
        )

        return df

    # ======================================================
    # Range Moving Average
    # ======================================================

    @staticmethod
    def range_ma_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "candle_range" not in df.columns:

            df["candle_range"] = (
                df["high"] - df["low"]
            )

        df["range_ma_5"] = (
            df["candle_range"]
            .rolling(5)
            .mean()
        )

        return df

    @staticmethod
    def range_ma_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "candle_range" not in df.columns:

            df["candle_range"] = (
                df["high"] - df["low"]
            )

        df["range_ma_10"] = (
            df["candle_range"]
            .rolling(10)
            .mean()
        )

        return df

    @staticmethod
    def range_ma_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "candle_range" not in df.columns:

            df["candle_range"] = (
                df["high"] - df["low"]
            )

        df["range_ma_20"] = (
            df["candle_range"]
            .rolling(20)
            .mean()
        )

        return df

    # ======================================================
    # Range Expansion / Contraction
    # ======================================================

    @staticmethod
    def range_expansion(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Current Range / Average Range
        """

        if "candle_range" not in df.columns:

            df["candle_range"] = (
                df["high"] - df["low"]
            )

        if "range_ma_20" not in df.columns:
            df = VolatilityFeatures.range_ma_20(df)

        df["range_expansion"] = (
            FeatureUtils.safe_divide(
                df["candle_range"],
                df["range_ma_20"],
            )
        )

        return df

    @staticmethod
    def range_contraction(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Average Range / Current Range
        """

        if "candle_range" not in df.columns:

            df["candle_range"] = (
                df["high"] - df["low"]
            )

        if "range_ma_20" not in df.columns:
            df = VolatilityFeatures.range_ma_20(df)

        df["range_contraction"] = (
            FeatureUtils.safe_divide(
                df["range_ma_20"],
                df["candle_range"],
            )
        )

        return df
    # ======================================================
    # ATR Percent
    # ======================================================

    @staticmethod
    def atr_percent_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR 5 as percentage of Close.
        """

        if "atr_5" not in df.columns:
            df = VolatilityFeatures.atr_5(df)

        df["atr_percent_5"] = (
            FeatureUtils.safe_divide(
                df["atr_5"],
                df["close"],
            )
            * 100
        )

        return df


    @staticmethod
    def atr_percent_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR 10 as percentage of Close.
        """

        if "atr_10" not in df.columns:
            df = VolatilityFeatures.atr_10(df)

        df["atr_percent_10"] = (
            FeatureUtils.safe_divide(
                df["atr_10"],
                df["close"],
            )
            * 100
        )

        return df


    @staticmethod
    def atr_percent_14(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR 14 as percentage of Close.
        """

        if "atr_14" not in df.columns:
            df = VolatilityFeatures.atr_14(df)

        df["atr_percent_14"] = (
            FeatureUtils.safe_divide(
                df["atr_14"],
                df["close"],
            )
            * 100
        )

        return df


    @staticmethod
    def atr_percent_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR 20 as percentage of Close.
        """

        if "atr_20" not in df.columns:
            df = VolatilityFeatures.atr_20(df)

        df["atr_percent_20"] = (
            FeatureUtils.safe_divide(
                df["atr_20"],
                df["close"],
            )
            * 100
        )

        return df
    
    # ======================================================
    # Rolling Standard Deviation
    # ======================================================

    @staticmethod
    def std_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["std_5"] = (
            df["close"]
            .rolling(5)
            .std()
        )

        return df


    @staticmethod
    def std_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["std_10"] = (
            df["close"]
            .rolling(10)
            .std()
        )

        return df


    @staticmethod
    def std_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["std_20"] = (
            df["close"]
            .rolling(20)
            .std()
        )

        return df


    # ======================================================
    # Rolling Variance
    # ======================================================

    @staticmethod
    def variance_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["variance_5"] = (
            df["close"]
            .rolling(5)
            .var()
        )

        return df


    @staticmethod
    def variance_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["variance_10"] = (
            df["close"]
            .rolling(10)
            .var()
        )

        return df


    @staticmethod
    def variance_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["variance_20"] = (
            df["close"]
            .rolling(20)
            .var()
        )

        return df
    
    # ======================================================
    # ATR Ratio
    # ======================================================

    @staticmethod
    def atr_ratio(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR Ratio

        ATR14 / ATR20
        """

        if "atr_14" not in df.columns:
            df = VolatilityFeatures.atr_14(df)

        if "atr_20" not in df.columns:
            df = VolatilityFeatures.atr_20(df)

        df["atr_ratio"] = (
            FeatureUtils.safe_divide(
                df["atr_14"],
                df["atr_20"],
            )
        )

        return df


    # ======================================================
    # Volatility Expansion / Compression
    # ======================================================

    @staticmethod
    def volatility_expansion(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR14 is expanding.
        """

        if "atr_14" not in df.columns:
            df = VolatilityFeatures.atr_14(df)

        df["volatility_expansion"] = (
            df["atr_14"] >
            df["atr_14"].shift(1)
        )

        return df


    @staticmethod
    def volatility_compression(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        ATR14 is contracting.
        """

        if "atr_14" not in df.columns:
            df = VolatilityFeatures.atr_14(df)

        df["volatility_compression"] = (
            df["atr_14"] <
            df["atr_14"].shift(1)
        )

        return df
                