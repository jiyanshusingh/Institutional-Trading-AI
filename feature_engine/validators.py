"""
==========================================================
Validators
==========================================================

Purpose
-------
Central validation engine for market observations.

Responsibilities
----------------
- Validate input DataFrames.
- Validate required columns.
- Validate numeric data.
- Validate timestamps.
- Validate missing values.

This module does NOT:

- Compute features.
- Fill missing values.
- Modify data.
- Perform research.

==========================================================
"""

from __future__ import annotations

import pandas as pd


# ==========================================================
# Validator
# ==========================================================

class DataValidator:
    """
    Validates market observations before feature
    computation.
    """

    # ======================================================
    # Public API
    # ======================================================

    def validate(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Run all core validations.
        """

        self.validate_required_columns(df)

        self.validate_numeric_columns(df)

        self.validate_missing_values(df)

        self.validate_duplicate_timestamps(df)

        self.validate_sorted_timestamps(df)

    # ======================================================
    # Required Columns
    # ======================================================

    def validate_required_columns(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Validate OHLC columns.
        """

        required = [
            "open",
            "high",
            "low",
            "close",
        ]

        missing = [

            column

            for column in required

            if column not in df.columns

        ]

        if missing:

            raise ValueError(

                f"Missing required columns: {missing}"

            )

    # ======================================================
    # Numeric Columns
    # ======================================================

    def validate_numeric_columns(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Ensure OHLC columns are numeric.
        """

        numeric_columns = [

            "open",

            "high",

            "low",

            "close",

        ]

        invalid = []

        for column in numeric_columns:

            if not pd.api.types.is_numeric_dtype(

                df[column]

            ):

                invalid.append(column)

        if invalid:

            raise TypeError(

                f"Non-numeric columns: {invalid}"

            )

    # ======================================================
    # Missing Values
    # ======================================================

    def validate_missing_values(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Detect missing values.
        """

        missing = df.isna().sum()

        missing = missing[missing > 0]

        if not missing.empty:

            raise ValueError(

                "Missing values detected:\n"

                f"{missing}"

            )

    # ======================================================
    # Duplicate Timestamps
    # ======================================================

    def validate_duplicate_timestamps(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Detect duplicate timestamps.
        """

        if "timestamp" not in df.columns:

            return

        duplicates = df["timestamp"].duplicated()

        if duplicates.any():

            raise ValueError(

                "Duplicate timestamps detected."

            )

    # ======================================================
    # Sorted Timestamps
    # ======================================================

    def validate_sorted_timestamps(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Ensure timestamps are ascending.
        """

        if "timestamp" not in df.columns:

            return

        if not df["timestamp"].is_monotonic_increasing:

            raise ValueError(

                "Timestamps must be sorted."

            )


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("DATA VALIDATOR")

    print("=" * 60)

    print()

    print("Framework Ready ✓")