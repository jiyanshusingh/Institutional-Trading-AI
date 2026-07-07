"""
==========================================================
Trend Features
==========================================================

Deterministic trend-based market features.

No trading logic.
No AI.
No research.
==========================================================
"""

from __future__ import annotations

import pandas as pd


class TrendFeatures:

    # ======================================================
    # Exponential Moving Average
    # ======================================================

    @staticmethod
    def ema_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_5"] = (
            df["close"]
            .ewm(span=5, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_9(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_9"] = (
            df["close"]
            .ewm(span=9, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_10"] = (
            df["close"]
            .ewm(span=10, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_20"] = (
            df["close"]
            .ewm(span=20, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_21(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_21"] = (
            df["close"]
            .ewm(span=21, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_34(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_34"] = (
            df["close"]
            .ewm(span=34, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_50(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_50"] = (
            df["close"]
            .ewm(span=50, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_100(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_100"] = (
            df["close"]
            .ewm(span=100, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def ema_200(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["ema_200"] = (
            df["close"]
            .ewm(span=200, adjust=False)
            .mean()
        )

        return df
    
    # ======================================================
    # Simple Moving Average
    # ======================================================

    @staticmethod
    def sma_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["sma_5"] = (
            df["close"]
            .rolling(5)
            .mean()
        )

        return df


    @staticmethod
    def sma_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["sma_10"] = (
            df["close"]
            .rolling(10)
            .mean()
        )

        return df


    @staticmethod
    def sma_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["sma_20"] = (
            df["close"]
            .rolling(20)
            .mean()
        )

        return df


    @staticmethod
    def sma_50(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["sma_50"] = (
            df["close"]
            .rolling(50)
            .mean()
        )

        return df


    @staticmethod
    def sma_100(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["sma_100"] = (
            df["close"]
            .rolling(100)
            .mean()
        )

        return df


    @staticmethod
    def sma_200(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["sma_200"] = (
            df["close"]
            .rolling(200)
            .mean()
        )

        return df
    
    # ======================================================
    # Distance From Moving Average
    # ======================================================

    @staticmethod
    def distance_from_ema20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "ema_20" not in df.columns:
            df = TrendFeatures.ema_20(df)

        df["distance_from_ema20"] = (
            df["close"] -
            df["ema_20"]
        )

        return df


    @staticmethod
    def distance_from_ema50(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "ema_50" not in df.columns:
            df = TrendFeatures.ema_50(df)

        df["distance_from_ema50"] = (
            df["close"] -
            df["ema_50"]
        )

        return df


    @staticmethod
    def distance_from_ema200(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "ema_200" not in df.columns:
            df = TrendFeatures.ema_200(df)

        df["distance_from_ema200"] = (
            df["close"] -
            df["ema_200"]
        )

        return df


    @staticmethod
    def distance_from_sma20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "sma_20" not in df.columns:
            df = TrendFeatures.sma_20(df)

        df["distance_from_sma20"] = (
            df["close"] -
            df["sma_20"]
        )

        return df


    @staticmethod
    def distance_from_sma50(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "sma_50" not in df.columns:
            df = TrendFeatures.sma_50(df)

        df["distance_from_sma50"] = (
            df["close"] -
            df["sma_50"]
        )

        return df


    @staticmethod
    def distance_from_sma200(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "sma_200" not in df.columns:
            df = TrendFeatures.sma_200(df)

        df["distance_from_sma200"] = (
            df["close"] -
            df["sma_200"]
        )

        return df


    # ======================================================
    # EMA Slope
    # ======================================================

    @staticmethod
    def ema20_slope(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "ema_20" not in df.columns:
            df = TrendFeatures.ema_20(df)

        df["ema20_slope"] = (
            df["ema_20"]
            .diff()
        )

        return df


    @staticmethod
    def ema50_slope(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "ema_50" not in df.columns:
            df = TrendFeatures.ema_50(df)

        df["ema50_slope"] = (
            df["ema_50"]
            .diff()
        )

        return df


    @staticmethod
    def ema200_slope(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "ema_200" not in df.columns:
            df = TrendFeatures.ema_200(df)

        df["ema200_slope"] = (
            df["ema_200"]
            .diff()
        )

        return df