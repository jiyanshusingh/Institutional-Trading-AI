"""
Kaggle Dataset Normalizer

Converts Kaggle OHLCV datasets into the canonical
Institutional Trading AI market data format.

Canonical Schema
----------------
timestamp
open
high
low
close
volume
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data.contracts.dataset_normalizer import (
    DatasetNormalizer,
)


class KaggleNormalizer(DatasetNormalizer):
    """
    Normalizes Kaggle market datasets.
    """

    @property
    def normalizer_name(self) -> str:
        return "KaggleNormalizer"

    @property
    def vendor(self) -> str:
        return "Kaggle"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def normalize(
        self,
        input_path: str | Path,
        output_path: str | Path,
    ) -> pd.DataFrame:

        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file not found: {input_path}"
            )

        # ------------------------------------------------------
        # Read Dataset
        # ------------------------------------------------------

        df = self._read_dataset(input_path)

        # ------------------------------------------------------
        # Normalize Columns
        # ------------------------------------------------------

        df = self._normalize_columns(df)

        # ------------------------------------------------------
        # Normalize Timestamp
        # ------------------------------------------------------

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            dayfirst=True,
            errors="raise",
        )

        # ------------------------------------------------------
        # Numeric Conversion
        # ------------------------------------------------------

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="raise",
            )

        # ------------------------------------------------------
        # Canonical Order
        # ------------------------------------------------------

        df = df[
            [
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]

        # ------------------------------------------------------
        # Sort
        # ------------------------------------------------------

        df = df.sort_values(
            "timestamp"
        ).reset_index(drop=True)

        # ------------------------------------------------------
        # Validate
        # ------------------------------------------------------

        self.validate(df)

        # ------------------------------------------------------
        # Save
        # ------------------------------------------------------

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            output_path,
            index=False,
        )

        return df

    # ==========================================================
    # Internal Helpers
    # ==========================================================

    def _read_dataset(
        self,
        path: Path,
    ) -> pd.DataFrame:
        """
        Read comma, tab, or whitespace separated files.
        """

        # Try comma-separated first
        df = pd.read_csv(path)

        if len(df.columns) > 1:
            return df

        # Try tab-separated
        df = pd.read_csv(
            path,
            sep="\t",
        )

        if len(df.columns) > 1:
            return df

        # Try arbitrary whitespace
        df = pd.read_csv(
            path,
            sep=r"\s+",
            engine="python",
        )

        return df

    def _normalize_columns(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df.columns = [
            column.strip().lower()
            for column in df.columns
        ]

        column_mapping = {
            "date": "timestamp",
            "datetime": "timestamp",
            "time": "timestamp",
        }

        df = df.rename(
            columns=column_mapping,
        )

        return df