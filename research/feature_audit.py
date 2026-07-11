"""
==========================================================
Feature Audit
==========================================================

Purpose
-------
Performs quality control (QC) on the generated feature
dataset before statistical validation.

Responsibilities
----------------
- Check every feature
- Detect NaN / Inf
- Compute descriptive statistics
- Validate feature ranges
- Export audit report

==========================================================
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


class FeatureAudit:

    # ======================================================
    # Public API
    # ======================================================

    @staticmethod
    def audit(
        df: pd.DataFrame,
        output_path: str | Path | None = None,
    ) -> pd.DataFrame:
        """
        Audit every generated feature.

        Parameters
        ----------
        df
            Feature DataFrame.

        output_path
            Optional CSV output path.

        Returns
        -------
        Audit DataFrame.
        """

        feature_columns = FeatureAudit._feature_columns(df)

        records = []

        for feature in feature_columns:

            series = df[feature]

            numeric = pd.to_numeric(
                series,
                errors="coerce",
            )
            numeric = (
                pd.to_numeric(
                    series,
                    errors="coerce",
                )
                .astype("float64")
            )

            nan_count = int(
                numeric.isna().sum()
            )

            inf_count = int(
                np.isinf(
                    numeric.to_numpy(
                        dtype=float,
                        na_value=np.nan,
                    )
                ).sum()
            )

            zero_count = int(
                (numeric == 0).sum()
            )

            record = {

                "feature": feature,

                "dtype": str(series.dtype),

                "rows": len(series),

                "nan_count": nan_count,

                "nan_percent":
                    round(
                        nan_count / len(series) * 100,
                        4,
                    ),

                "inf_count": inf_count,

                "zero_count": zero_count,

                "unique_count":
                    int(
                        numeric.nunique(
                            dropna=True,
                        )
                    ),

                "min": numeric.min(),

                "max": numeric.max(),

                "mean": numeric.mean(),

                "median": numeric.median(),

                "std": numeric.std(),

                "variance": numeric.var(),

                "skewness": numeric.skew(),

                "kurtosis": numeric.kurt(),

                "q01": numeric.quantile(0.01),

                "q05": numeric.quantile(0.05),

                "q25": numeric.quantile(0.25),

                "q50": numeric.quantile(0.50),

                "q75": numeric.quantile(0.75),

                "q95": numeric.quantile(0.95),

                "q99": numeric.quantile(0.99),

            }

            status, remarks = FeatureAudit._validate(
                feature,
                record,
            )

            record["status"] = status

            record["remarks"] = remarks

            records.append(record)

        audit = pd.DataFrame(records)

        if output_path is not None:

            output_path = Path(output_path)

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            audit.to_csv(
                output_path,
                index=False,
            )

        return audit

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def _feature_columns(
        df: pd.DataFrame,
    ) -> list[str]:

        excluded = {

            "timestamp",

            "open",

            "high",

            "low",

            "close",

            "volume",

        }

        excluded_prefixes = (

            "forward_",

            "mfe",

            "mae",

            "future_",

        )

        columns = []

        for column in df.columns:

            if column in excluded:

                continue

            if column.startswith(
                excluded_prefixes
            ):

                continue

            columns.append(column)

        return columns

    # ======================================================
    # Validation Rules
    # ======================================================

    @staticmethod
    def _validate(
        feature: str,
        record: dict,
    ) -> tuple[str, str]:

        remarks = []

        status = "PASS"

        if record["inf_count"] > 0:

            status = "FAIL"

            remarks.append(
                "Infinite values"
            )

        if record["unique_count"] <= 1:

            status = "FAIL"

            remarks.append(
                "Constant feature"
            )

        if feature.startswith("rsi"):

            if (
                record["min"] < 0
                or record["max"] > 100
            ):

                status = "FAIL"

                remarks.append(
                    "RSI out of range"
                )

        if feature.startswith("stochastic"):

            if (
                record["min"] < 0
                or record["max"] > 100
            ):

                status = "FAIL"

                remarks.append(
                    "Stochastic out of range"
                )

        if feature == "williams_r":

            if (
                record["min"] < -100
                or record["max"] > 0
            ):

                status = "FAIL"

                remarks.append(
                    "Williams %R out of range"
                )

        if feature == "body_ratio":

            if (
                record["min"] < 0
                or record["max"] > 1
            ):

                status = "FAIL"

                remarks.append(
                    "Body ratio out of range"
                )

        if feature.startswith("atr"):

            if record["min"] < 0:

                status = "FAIL"

                remarks.append(
                    "Negative ATR"
                )

        return status, "; ".join(remarks)