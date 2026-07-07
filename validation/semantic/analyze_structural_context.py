from pathlib import Path

import pandas as pd

INPUT_CSV = Path(
    "validation/output/broken_swings.csv"
)


def print_header(title: str):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_group_statistics(
    name: str,
    df: pd.DataFrame,
):

    print(f"\n{name}")
    print("-" * len(name))

    print(f"Count                : {len(df):,}")

    if len(df) == 0:
        return

    print(
        f"Average Break Time   : "
        f"{df['Candles_To_Break'].mean():.2f}"
    )

    print(
        f"Median Break Time    : "
        f"{df['Candles_To_Break'].median():.2f}"
    )

    print(
        f"Minimum Break Time   : "
        f"{df['Candles_To_Break'].min()}"
    )

    print(
        f"Maximum Break Time   : "
        f"{df['Candles_To_Break'].max()}"
    )


def main():

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            INPUT_CSV
        )

    df = pd.read_csv(INPUT_CSV)

    print_header(
        "STRUCTURAL CONTEXT ANALYSIS"
    )

    print(
        f"Total Broken Swings : {len(df):,}"
    )

    #
    # Superseded
    #

    print_header(
        "SUPERSEDED ANALYSIS"
    )

    superseded = df[
        df["Superseded_By_Same_Type"]
    ]

    not_superseded = df[
        ~df["Superseded_By_Same_Type"]
    ]

    print_group_statistics(
        "Superseded",
        superseded,
    )

    print_group_statistics(
        "Not Superseded",
        not_superseded,
    )

    #
    # Same-Type Swing Count
    #

    print_header(
        "SAME-TYPE SWINGS BEFORE BREAK"
    )

    print(
        df[
            "Same_Type_Swings_Before_Break"
        ]
        .value_counts()
        .sort_index()
    )

    #
    # Opposite-Type Swing Count
    #

    print_header(
        "OPPOSITE-TYPE SWINGS BEFORE BREAK"
    )

    print(
        df[
            "Opposite_Type_Swings_Before_Break"
        ]
        .value_counts()
        .sort_index()
    )

    #
    # Latest Swing
    #

    print_header(
        "LATEST SWING STATUS"
    )

    latest = (
        df["Latest_Same_Type_Swing_ID"]
        == df["Swing_ID"]
    )

    print(
        f"Latest Swing        : "
        f"{latest.sum():,}"
    )

    print(
        f"Not Latest Swing    : "
        f"{(~latest).sum():,}"
    )

    print()

    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()