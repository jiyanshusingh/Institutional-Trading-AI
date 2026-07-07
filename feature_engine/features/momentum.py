"""
==========================================================
Momentum Features
==========================================================

Deterministic momentum-based market features.

No trading logic.
No AI.
No research.
==========================================================
"""

from __future__ import annotations

import pandas as pd

from feature_engine.features.utils import FeatureUtils


class MomentumFeatures:

    # ======================================================
    # RSI
    # ======================================================

    @staticmethod
    def rsi_7(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = (-delta).clip(lower=0)

        avg_gain = gain.rolling(7).mean()

        avg_loss = loss.rolling(7).mean()

        rs = FeatureUtils.safe_divide(
            avg_gain,
            avg_loss,
        )

        df["rsi_7"] = (
            100 -
            (100 / (1 + rs))
        )

        return df


    @staticmethod
    def rsi_14(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = (-delta).clip(lower=0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = FeatureUtils.safe_divide(
            avg_gain,
            avg_loss,
        )

        df["rsi_14"] = (
            100 -
            (100 / (1 + rs))
        )

        return df


    @staticmethod
    def rsi_21(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = (-delta).clip(lower=0)

        avg_gain = gain.rolling(21).mean()

        avg_loss = loss.rolling(21).mean()

        rs = FeatureUtils.safe_divide(
            avg_gain,
            avg_loss,
        )

        df["rsi_21"] = (
            100 -
            (100 / (1 + rs))
        )

        return df


    # ======================================================
    # Rate of Change
    # ======================================================

    @staticmethod
    def roc_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        previous = df["close"].shift(5)

        df["roc_5"] = (
            FeatureUtils.safe_divide(
                df["close"] - previous,
                previous,
            )
            * 100
        )

        return df


    @staticmethod
    def roc_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        previous = df["close"].shift(10)

        df["roc_10"] = (
            FeatureUtils.safe_divide(
                df["close"] - previous,
                previous,
            )
            * 100
        )

        return df


    @staticmethod
    def roc_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        previous = df["close"].shift(20)

        df["roc_20"] = (
            FeatureUtils.safe_divide(
                df["close"] - previous,
                previous,
            )
            * 100
        )

        return df
    
    # ======================================================
    # Momentum
    # ======================================================

    @staticmethod
    def momentum_5(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["momentum_5"] = (
            df["close"] -
            df["close"].shift(5)
        )

        return df


    @staticmethod
    def momentum_10(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["momentum_10"] = (
            df["close"] -
            df["close"].shift(10)
        )

        return df


    @staticmethod
    def momentum_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df["momentum_20"] = (
            df["close"] -
            df["close"].shift(20)
        )

        return df


    # ======================================================
    # MACD
    # ======================================================

    @staticmethod
    def macd(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        ema12 = (
            df["close"]
            .ewm(span=12, adjust=False)
            .mean()
        )

        ema26 = (
            df["close"]
            .ewm(span=26, adjust=False)
            .mean()
        )

        df["macd"] = ema12 - ema26

        return df


    @staticmethod
    def macd_signal(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "macd" not in df.columns:
            df = MomentumFeatures.macd(df)

        df["macd_signal"] = (
            df["macd"]
            .ewm(span=9, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def macd_histogram(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "macd" not in df.columns:
            df = MomentumFeatures.macd(df)

        if "macd_signal" not in df.columns:
            df = MomentumFeatures.macd_signal(df)

        df["macd_histogram"] = (
            df["macd"] -
            df["macd_signal"]
        )

        return df
    
    # ======================================================
    # Stochastic Oscillator
    # ======================================================

    @staticmethod
    def stochastic_k(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        lowest_low = (
            df["low"]
            .rolling(14)
            .min()
        )

        highest_high = (
            df["high"]
            .rolling(14)
            .max()
        )

        df["stochastic_k"] = (
            FeatureUtils.safe_divide(
                df["close"] - lowest_low,
                highest_high - lowest_low,
            )
            * 100
        )

        return df


    @staticmethod
    def stochastic_d(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if "stochastic_k" not in df.columns:
            df = MomentumFeatures.stochastic_k(df)

        df["stochastic_d"] = (
            df["stochastic_k"]
            .rolling(3)
            .mean()
        )

        return df


    # ======================================================
    # Williams %R
    # ======================================================

    @staticmethod
    def williams_r(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        highest_high = (
            df["high"]
            .rolling(14)
            .max()
        )

        lowest_low = (
            df["low"]
            .rolling(14)
            .min()
        )

        df["williams_r"] = (
            -100
            * FeatureUtils.safe_divide(
                highest_high - df["close"],
                highest_high - lowest_low,
            )
        )

        return df


    # ======================================================
    # Commodity Channel Index
    # ======================================================

    @staticmethod
    def cci_20(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        typical_price = (
            df["high"] +
            df["low"] +
            df["close"]
        ) / 3

        sma = (
            typical_price
            .rolling(20)
            .mean()
        )

        mean_deviation = (
            typical_price
            .rolling(20)
            .apply(
                lambda x: (
                    abs(
                        x - x.mean()
                    )
                ).mean(),
                raw=False,
            )
        )

        df["cci_20"] = (
            FeatureUtils.safe_divide(
                typical_price - sma,
                0.015 * mean_deviation,
            )
        )

        return df