from pathlib import Path

import pandas as pd
import pytest

from data.normalization.kaggle_normalizer import (
    KaggleNormalizer,
)


# ==========================================================
# Helpers
# ==========================================================

def create_kaggle_dataset(
    tmp_path: Path,
) -> Path:

    dataset = """date\topen\thigh\tlow\tclose\tvolume
14/09/2021 09:15\t349.5\t349.5\t349.5\t349.5\t0
14/09/2021 09:16\t350.0\t351.0\t349.0\t350.5\t1200
14/09/2021 09:17\t350.5\t352.0\t350.0\t351.5\t1500
"""

    path = tmp_path / "kaggle.tsv"

    path.write_text(dataset)

    return path


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    normalizer = KaggleNormalizer()

    assert (
        normalizer.normalizer_name
        == "KaggleNormalizer"
    )

    assert normalizer.vendor == "Kaggle"

    assert normalizer.version == "1.0"


# ==========================================================
# Normalize
# ==========================================================

def test_normalize_returns_dataframe(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    assert isinstance(
        df,
        pd.DataFrame,
    )


def test_output_file_created(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    normalizer.normalize(
        input_path,
        output_path,
    )

    assert output_path.exists()


# ==========================================================
# Canonical Schema
# ==========================================================

def test_canonical_columns(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    assert tuple(df.columns) == (
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    )


def test_timestamp_dtype(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    assert pd.api.types.is_datetime64_any_dtype(
        df["timestamp"]
    )


# ==========================================================
# Data Integrity
# ==========================================================

def test_row_count_preserved(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    assert len(df) == 3


def test_numeric_columns(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    for column in (
        "open",
        "high",
        "low",
        "close",
        "volume",
    ):
        assert pd.api.types.is_numeric_dtype(
            df[column]
        )


# ==========================================================
# Validation
# ==========================================================

def test_missing_input_file():

    normalizer = KaggleNormalizer()

    with pytest.raises(
        FileNotFoundError
    ):
        normalizer.normalize(
            "missing.tsv",
            "out.csv",
        )


def test_output_is_valid(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    # Should not raise
    normalizer.validate(df)


# ==========================================================
# Saved CSV
# ==========================================================

def test_saved_csv_matches_dataframe(
    tmp_path,
):

    input_path = create_kaggle_dataset(
        tmp_path
    )

    output_path = (
        tmp_path / "normalized.csv"
    )

    normalizer = KaggleNormalizer()

    df = normalizer.normalize(
        input_path,
        output_path,
    )

    loaded = pd.read_csv(
        output_path,
    )

    assert len(loaded) == len(df)

    assert tuple(loaded.columns) == (
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    )