"""
Normalize a Kaggle dataset into the Institutional Trading AI
canonical market data format.

Usage
-----
python -m scripts.normalize_kaggle_dataset
"""

from pathlib import Path

from data.normalization.kaggle_normalizer import (
    KaggleNormalizer,
)


def main() -> None:

    input_path = Path(
        "historical_data/raw/kaggle/ACUTAAS_minute.csv"
    )

    output_path = Path(
        "historical_data/normalized/ACUTAAS_1m.csv"
    )

    normalizer = KaggleNormalizer()

    print("=" * 60)
    print("KAGGLE DATASET NORMALIZATION")
    print("=" * 60)

    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print()

    df = normalizer.normalize(
        input_path=input_path,
        output_path=output_path,
    )

    print("Normalization completed successfully.")
    print()

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")
    print()

    print("Canonical Schema")
    print("----------------")
    for column in df.columns:
        print(column)

    print()
    print("First Five Rows")
    print("----------------")
    print(df.head())

    print()
    print("=" * 60)
    print("NORMALIZED DATASET CREATED")
    print("=" * 60)


if __name__ == "__main__":
    main()