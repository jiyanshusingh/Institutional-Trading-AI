from pathlib import Path

import pandas as pd


# ==========================================================
# Research Configuration
# ==========================================================

RESEARCH_CATEGORY = "successful"

DEFAULT_SAMPLE_SIZE = 30

RANDOM_SEED = 42


# ==========================================================
# Input / Output Paths
# ==========================================================

INPUT_DATASET = Path(
    f"research/continuation/"
    f"{RESEARCH_CATEGORY}/dataset.csv"
)

OUTPUT_SAMPLE = Path(
    f"research/continuation/"
    f"{RESEARCH_CATEGORY}/review_sample.csv"
)


# ==========================================================
# Required Columns
# ==========================================================

REQUIRED_COLUMNS = [

    "Example_ID",

    "Symbol",

    "Timeframe",

    "direction",

    "impulse_start",

    "impulse_end",

    "pullback_end",

    "continuation_index",

    "impulse_size",

    "retracement_percent",

]


# ==========================================================
# Dataset Loading
# ==========================================================

def load_dataset():

    if not INPUT_DATASET.exists():

        raise FileNotFoundError(

            f"Dataset not found:\n"
            f"{INPUT_DATASET}"

        )

    dataset = pd.read_csv(
        INPUT_DATASET
    )

    if dataset.empty:

        raise ValueError(

            "Dataset is empty."

        )

    missing = [

        column

        for column in REQUIRED_COLUMNS

        if column not in dataset.columns

    ]

    if missing:

        raise ValueError(

            "Dataset is missing "
            f"required columns:\n{missing}"

        )

    return dataset


# ==========================================================
# Output Helpers
# ==========================================================

def prepare_output_directory():

    OUTPUT_SAMPLE.parent.mkdir(

        parents=True,

        exist_ok=True,

    )
# ==========================================================
# Review Sample Generation
# ==========================================================

def generate_review_sample(
    dataset,
    sample_size=DEFAULT_SAMPLE_SIZE,
):
    """
    Generate a reproducible random review sample.

    Parameters
    ----------
    dataset : pandas.DataFrame

    sample_size : int

    Returns
    -------
    pandas.DataFrame
    """

    available = len(dataset)

    # ------------------------------------------------------
    # Prevent requesting more samples than available
    # ------------------------------------------------------

    sample_size = min(
        sample_size,
        available,
    )

    sample = dataset.sample(

        n=sample_size,

        random_state=RANDOM_SEED,

        replace=False,

    )

    # ------------------------------------------------------
    # Sort by Example_ID for easier review
    # ------------------------------------------------------

    sample = sample.sort_values(

        by="Example_ID",

    ).reset_index(

        drop=True,

    )

    return sample


# ==========================================================
# Statistics
# ==========================================================

def print_sample_summary(
    dataset,
    review_sample,
):

    print("=" * 60)
    print("REVIEW SAMPLE SUMMARY")
    print("=" * 60)

    print(
        f"Dataset Size      : {len(dataset):,}"
    )

    print(
        f"Review Sample     : {len(review_sample):,}"
    )

    print(
        f"Sampling Method   : Random"
    )

    print(
        f"Random Seed       : {RANDOM_SEED}"
    )

    bullish = (
        review_sample["direction"]
        == "BULLISH"
    ).sum()

    bearish = (
        review_sample["direction"]
        == "BEARISH"
    ).sum()

    print(
        f"Bullish Examples  : {bullish:,}"
    )

    print(
        f"Bearish Examples  : {bearish:,}"
    )

    print()
# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("REVIEW SAMPLE GENERATOR")
    print("=" * 60)
    print()

    print(
        f"Research Category : {RESEARCH_CATEGORY}"
    )

    print(
        f"Sample Size       : {DEFAULT_SAMPLE_SIZE}"
    )

    print(
        f"Random Seed       : {RANDOM_SEED}"
    )

    print()

    prepare_output_directory()

    # ------------------------------------------------------
    # Load Dataset
    # ------------------------------------------------------

    dataset = load_dataset()

    print(
        f"Dataset Loaded    : {len(dataset):,}"
    )

    # ------------------------------------------------------
    # Generate Review Sample
    # ------------------------------------------------------

    review_sample = generate_review_sample(
        dataset=dataset,
        sample_size=DEFAULT_SAMPLE_SIZE,
    )

    # ------------------------------------------------------
    # Save Review Sample
    # ------------------------------------------------------

    review_sample.to_csv(
        OUTPUT_SAMPLE,
        index=False,
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print()

    print_sample_summary(
        dataset,
        review_sample,
    )

    print("=" * 60)
    print("OUTPUT")
    print("=" * 60)

    print(
        f"Review Sample Saved :\n"
        f"{OUTPUT_SAMPLE}"
    )

    print()

    print("=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()