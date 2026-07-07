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


def main():

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"File not found: {INPUT_CSV}"
        )

    df = pd.read_csv(INPUT_CSV)

    if df.empty:
        raise ValueError(
            "Broken swing file is empty."
        )

    print_header("BROKEN SWING ANALYSIS")

    print(f"Total Broken Swings : {len(df):,}")

    print_header("SWING TYPE DISTRIBUTION")

    print(
        df["Swing_Type"]
        .value_counts()
        .sort_index()
    )

    print_header("CANDLES TO BREAK")

    print(df["Candles_To_Break"].describe())

    print_header("FASTEST 20 BREAKS")

    fastest = (
        df.sort_values("Candles_To_Break")
        .head(20)
    )

    print(
        fastest[
            [
                "Swing_ID",
                "Swing_Type",
                "Swing_Index",
                "Swing_Price",
                "Break_Index",
                "Candles_To_Break",
            ]
        ]
    )

    print_header("SLOWEST 20 BREAKS")

    slowest = (
        df.sort_values(
            "Candles_To_Break",
            ascending=False,
        )
        .head(20)
    )

    print(
        slowest[
            [
                "Swing_ID",
                "Swing_Type",
                "Swing_Index",
                "Swing_Price",
                "Break_Index",
                "Candles_To_Break",
            ]
        ]
    )

    print_header("BREAK PRICE STATISTICS")

    print(df["Break_Price"].describe())

    print_header("TOP 20 HIGHEST BREAK PRICES")

    print(
        df.nlargest(
            20,
            "Break_Price",
        )[
            [
                "Swing_ID",
                "Swing_Type",
                "Swing_Price",
                "Break_Price",
                "Candles_To_Break",
            ]
        ]
    )

    print_header("TOP 20 LOWEST BREAK PRICES")

    print(
        df.nsmallest(
            20,
            "Break_Price",
        )[
            [
                "Swing_ID",
                "Swing_Type",
                "Swing_Price",
                "Break_Price",
                "Candles_To_Break",
            ]
        ]
    )

    print_header("ANALYSIS COMPLETE")


if __name__ == "__main__":
    main()