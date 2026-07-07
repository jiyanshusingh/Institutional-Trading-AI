"""
==========================================================
Price Features
==========================================================

Deterministic price-based market features.

No trading logic.
No AI.
No research.
==========================================================
"""

from __future__ import annotations

import pandas as pd


class PriceFeatures:

    # ======================================================
    # Helper
    # ======================================================

    @staticmethod
    def safe_divide(
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
    # Base Features
    # ======================================================

    @staticmethod
    def candle_range(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["candle_range"] = (
            df["high"] - df["low"]
        )

        return df

    @staticmethod
    def body_size(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["body_size"] = (
            df["close"] - df["open"]
        ).abs()

        return df

    @staticmethod
    def upper_wick(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        candle_top = df[
            ["open", "close"]
        ].max(axis=1)

        df["upper_wick"] = (
            df["high"] - candle_top
        )

        return df

    @staticmethod
    def lower_wick(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        candle_bottom = df[
            ["open", "close"]
        ].min(axis=1)

        df["lower_wick"] = (
            candle_bottom - df["low"]
        )

        return df

    # ======================================================
    # Derived Features
    # ======================================================

    @staticmethod
    def body_ratio(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "body_size" not in df.columns:
            df = PriceFeatures.body_size(df)

        if "candle_range" not in df.columns:
            df = PriceFeatures.candle_range(df)

        df["body_ratio"] = PriceFeatures.safe_divide(
            df["body_size"],
            df["candle_range"],
        )

        return df

    @staticmethod
    def upper_wick_ratio(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "upper_wick" not in df.columns:
            df = PriceFeatures.upper_wick(df)

        if "candle_range" not in df.columns:
            df = PriceFeatures.candle_range(df)

        df["upper_wick_ratio"] = (
            PriceFeatures.safe_divide(
                df["upper_wick"],
                df["candle_range"],
            )
        )

        return df

    @staticmethod
    def lower_wick_ratio(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "lower_wick" not in df.columns:
            df = PriceFeatures.lower_wick(df)

        if "candle_range" not in df.columns:
            df = PriceFeatures.candle_range(df)

        df["lower_wick_ratio"] = (
            PriceFeatures.safe_divide(
                df["lower_wick"],
                df["candle_range"],
            )
        )

        return df

    @staticmethod
    def open_position(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "candle_range" not in df.columns:
            df = PriceFeatures.candle_range(df)

        df["open_position"] = (
            PriceFeatures.safe_divide(
                df["open"] - df["low"],
                df["candle_range"],
            )
        )

        return df

    @staticmethod
    def close_position(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "candle_range" not in df.columns:
            df = PriceFeatures.candle_range(df)

        df["close_position"] = (
            PriceFeatures.safe_divide(
                df["close"] - df["low"],
                df["candle_range"],
            )
        )

        return df
    @staticmethod
    def gap(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Opening Gap

        Current Open - Previous Close
        """

        df["gap"] = (
            df["open"] -
            df["close"].shift(1)
        )

        return df

    @staticmethod
    def gap_percent(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Gap as percentage of previous close.
        """

        if "gap" not in df.columns:
            df = PriceFeatures.gap(df)

        previous_close = df["close"].shift(1)

        df["gap_percent"] = (
            PriceFeatures._safe_divide(
                df["gap"],
                previous_close,
            )
            * 100
        )

        return df

    @staticmethod
    def median_price(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Median Price

        (High + Low) / 2
        """

        df["median_price"] = (
            df["high"] +
            df["low"]
        ) / 2

        return df

    @staticmethod
    def typical_price(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Typical Price

        (High + Low + Close) / 3
        """

        df["typical_price"] = (
            df["high"] +
            df["low"] +
            df["close"]
        ) / 3

        return df

    @staticmethod
    def weighted_close(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Weighted Close

        (High + Low + 2*Close) / 4
        """

        df["weighted_close"] = (
            df["high"] +
            df["low"] +
            (2 * df["close"])
        ) / 4

        return df

    @staticmethod
    def hl2(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        HL2

        (High + Low) / 2
        """

        df["hl2"] = (
            df["high"] +
            df["low"]
        ) / 2

        return df

    @staticmethod
    def hlc3(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        HLC3

        (High + Low + Close) / 3
        """

        df["hlc3"] = (
            df["high"] +
            df["low"] +
            df["close"]
        ) / 3

        return df

    @staticmethod
    def ohlc4(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        OHLC4

        (Open + High + Low + Close) / 4
        """

        df["ohlc4"] = (
            df["open"] +
            df["high"] +
            df["low"] +
            df["close"]
        ) / 4

        return df