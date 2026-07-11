"""
==========================================================
Target Builder
==========================================================

Purpose
-------
Generates objective research targets directly from
historical OHLCV data.

The builder creates continuous targets only.

No labels.
No thresholds.
No trading logic.

==========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from research.target_definitions import (
    TargetDefinition,
    TargetType,
)


class TargetBuilder:

    # ======================================================
    # Public API
    # ======================================================

    @staticmethod
    def build(
        df: pd.DataFrame,
        targets: list[TargetDefinition],
    ) -> pd.DataFrame:

        df = df.copy()

        for target in targets:

            if target.target_type == TargetType.FORWARD_RETURN:

                df = TargetBuilder.forward_return(
                    df,
                    target,
                )

            elif target.target_type == TargetType.FORWARD_HIGH:

                df = TargetBuilder.forward_high(
                    df,
                    target,
                )

            elif target.target_type == TargetType.FORWARD_LOW:

                df = TargetBuilder.forward_low(
                    df,
                    target,
                )

            elif target.target_type == TargetType.MAX_FAVORABLE_EXCURSION:

                df = TargetBuilder.mfe(
                    df,
                    target,
                )

            elif target.target_type == TargetType.MAX_ADVERSE_EXCURSION:

                df = TargetBuilder.mae(
                    df,
                    target,
                )

            elif target.target_type == TargetType.FUTURE_VOLATILITY:

                df = TargetBuilder.future_volatility(
                    df,
                    target,
                )

        return df

    # ======================================================
    # Forward Return
    # ======================================================

    @staticmethod
    def forward_return(
        df: pd.DataFrame,
        target: TargetDefinition,
    ) -> pd.DataFrame:

        future_close = df["close"].shift(
            -target.horizon
        )

        df[target.column_name] = (

            future_close - df["close"]

        ) / df["close"]

        return df

    # ======================================================
    # Forward High
    # ======================================================

    @staticmethod
    def forward_high(
        df: pd.DataFrame,
        target: TargetDefinition,
    ) -> pd.DataFrame:

        future_high = (

            df["high"]

            .shift(-1)

            .rolling(target.horizon)

            .max()

            .shift(

                -(target.horizon - 1)

            )

        )

        df[target.column_name] = (

            future_high - df["close"]

        ) / df["close"]

        return df

    # ======================================================
    # Forward Low
    # ======================================================

    @staticmethod
    def forward_low(
        df: pd.DataFrame,
        target: TargetDefinition,
    ) -> pd.DataFrame:

        future_low = (

            df["low"]

            .shift(-1)

            .rolling(target.horizon)

            .min()

            .shift(

                -(target.horizon - 1)

            )

        )

        df[target.column_name] = (

            future_low - df["close"]

        ) / df["close"]

        return df

    # ======================================================
    # Maximum Favorable Excursion
    # ======================================================

    @staticmethod
    def mfe(
        df: pd.DataFrame,
        target: TargetDefinition,
    ) -> pd.DataFrame:

        values = np.full(

            len(df),

            np.nan,

        )

        highs = df["high"].values

        closes = df["close"].values

        horizon = target.horizon

        for i in range(

            len(df) - horizon

        ):

            future_high = np.max(

                highs[i + 1:i + horizon + 1]

            )

            values[i] = (

                future_high - closes[i]

            ) / closes[i]

        df[target.column_name] = values

        return df

    # ======================================================
    # Maximum Adverse Excursion
    # ======================================================

    @staticmethod
    def mae(
        df: pd.DataFrame,
        target: TargetDefinition,
    ) -> pd.DataFrame:

        values = np.full(

            len(df),

            np.nan,

        )

        lows = df["low"].values

        closes = df["close"].values

        horizon = target.horizon

        for i in range(

            len(df) - horizon

        ):

            future_low = np.min(

                lows[i + 1:i + horizon + 1]

            )

            values[i] = (

                future_low - closes[i]

            ) / closes[i]

        df[target.column_name] = values

        return df

    # ======================================================
    # Future Volatility
    # ======================================================

    @staticmethod
    def future_volatility(
        df: pd.DataFrame,
        target: TargetDefinition,
    ) -> pd.DataFrame:

        future_returns = (

            df["close"]

            .pct_change()

            .shift(-1)

        )

        volatility = (

            future_returns

            .rolling(target.horizon)

            .std()

            .shift(

                -(target.horizon - 1)

            )

        )

        df[target.column_name] = volatility

        return df