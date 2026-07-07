from pathlib import Path

import pandas as pd


# ==========================================================
# Configuration
# ==========================================================

INPUT_EVENTS = Path(
    "research/continuation/continuation_events.csv"
)

OUTPUT_DATASET = Path(
    "research/continuation/successful/dataset.csv"
)

SYMBOL = "ACUTAAS"

TIMEFRAME = "1m"

SCANNER_VERSION = "1.0"


# ==========================================================
# Expected Columns
# ==========================================================

REQUIRED_COLUMNS = [

    "impulse_start",

    "impulse_end",

    "pullback_end",

    "continuation_index",

    "direction",

    "impulse_size",

    "retracement_percent",

]


# ==========================================================
# Data Loading
# ==========================================================

def load_events():

    if not INPUT_EVENTS.exists():

        raise FileNotFoundError(

            f"Input file not found:\n{INPUT_EVENTS}"

        )

    df = pd.read_csv(
        INPUT_EVENTS
    )

    missing = [

        column

        for column in REQUIRED_COLUMNS

        if column not in df.columns

    ]

    if missing:

        raise ValueError(

            "Missing required columns:\n"

            f"{missing}"

        )

    return df


# ==========================================================
# Output Helpers
# ==========================================================

def prepare_output_directory():

    OUTPUT_DATASET.parent.mkdir(

        parents=True,

        exist_ok=True,

    )
# ==========================================================
# Dataset Generation
# ==========================================================

def generate_dataset(events_df):
    """
    Transform scanner output into the canonical
    research dataset.

    One row = one continuation event.
    """

    dataset = events_df.copy()

    # ------------------------------------------------------
    # Stable Example IDs
    # ------------------------------------------------------

    dataset.insert(
        0,
        "Example_ID",
        [
            f"EX-{i:04d}"
            for i in range(
                1,
                len(dataset) + 1,
            )
        ],
    )

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    dataset["Symbol"] = SYMBOL

    dataset["Timeframe"] = TIMEFRAME

    dataset["Scanner_Version"] = SCANNER_VERSION

    # ------------------------------------------------------
    # Research Metadata
    # ------------------------------------------------------

    dataset["Review_Status"] = "Pending"

    dataset["Review_Result"] = "Unknown"

    dataset["Reviewer"] = ""

    dataset["Review_Date"] = ""

    dataset["Confidence"] = ""

    dataset["Comments"] = ""

    # ------------------------------------------------------
    # Reorder Columns
    # ------------------------------------------------------

    ordered_columns = [

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

        "Scanner_Version",

        "Review_Status",

        "Review_Result",

        "Reviewer",

        "Review_Date",

        "Confidence",

        "Comments",

    ]

    dataset = dataset[
        ordered_columns
    ]

    return dataset


# ==========================================================
# Dataset Statistics
# ==========================================================

def print_dataset_summary(dataset):

    bullish = (
        dataset["direction"]
        == "BULLISH"
    ).sum()

    bearish = (
        dataset["direction"]
        == "BEARISH"
    ).sum()

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print(
        f"Examples          : {len(dataset):,}"
    )

    print(
        f"Bullish           : {bullish:,}"
    )

    print(
        f"Bearish           : {bearish:,}"
    )

    print(
        f"Pending Reviews   : "
        f"{(dataset['Review_Status']=='Pending').sum():,}"
    )

    print()
    
# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("RESEARCH DATASET GENERATOR")
    print("=" * 60)
    print()

    prepare_output_directory()

    # ------------------------------------------------------
    # Load Scanner Output
    # ------------------------------------------------------

    events = load_events()

    print(
        f"Scanner Events : {len(events):,}"
    )

    # ------------------------------------------------------
    # Generate Dataset
    # ------------------------------------------------------

    dataset = generate_dataset(
        events
    )

    # ------------------------------------------------------
    # Save Dataset
    # ------------------------------------------------------

    dataset.to_csv(
        OUTPUT_DATASET,
        index=False,
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print_dataset_summary(
        dataset
    )

    print("=" * 60)
    print("OUTPUT")
    print("=" * 60)

    print(
        f"Dataset Saved :\n"
        f"{OUTPUT_DATASET}"
    )

    print()

    print("=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()