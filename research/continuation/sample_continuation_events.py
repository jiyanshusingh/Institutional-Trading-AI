from pathlib import Path

import pandas as pd


INPUT_CSV = Path(
    "research/continuation/continuation_events.csv"
)

OUTPUT_CSV = Path(
    "research/continuation/continuation_review_sample.csv"
)


LARGEST_COUNT = 10
SMALLEST_COUNT = 10
BULLISH_COUNT = 10
BEARISH_COUNT = 10
RANDOM_COUNT = 10

RANDOM_STATE = 42


def main():

    df = pd.read_csv(INPUT_CSV)

    if df.empty:
        print("No continuation events found.")
        return

    # --------------------------------------------------
    # Largest impulse events
    # --------------------------------------------------

    largest = (
        df.sort_values(
            "impulse_size",
            ascending=False,
        )
        .head(LARGEST_COUNT)
    )

    # --------------------------------------------------
    # Smallest impulse events
    # --------------------------------------------------

    smallest = (
        df.sort_values(
            "impulse_size",
            ascending=True,
        )
        .head(SMALLEST_COUNT)
    )

    # --------------------------------------------------
    # Bullish random
    # --------------------------------------------------

    bullish = (
        df[df["direction"] == "BULLISH"]
        .sample(
            min(
                BULLISH_COUNT,
                len(df[df["direction"] == "BULLISH"]),
            ),
            random_state=RANDOM_STATE,
        )
    )

    # --------------------------------------------------
    # Bearish random
    # --------------------------------------------------

    bearish = (
        df[df["direction"] == "BEARISH"]
        .sample(
            min(
                BEARISH_COUNT,
                len(df[df["direction"] == "BEARISH"]),
            ),
            random_state=RANDOM_STATE,
        )
    )

    # --------------------------------------------------
    # Overall random
    # --------------------------------------------------

    random_events = df.sample(
        min(RANDOM_COUNT, len(df)),
        random_state=RANDOM_STATE,
    )

    # --------------------------------------------------
    # Combine
    # --------------------------------------------------

    sample = pd.concat(
        [
            largest,
            smallest,
            bullish,
            bearish,
            random_events,
        ],
        ignore_index=True,
    )

    # --------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------

    sample = sample.drop_duplicates()

    # --------------------------------------------------
    # Sort
    # --------------------------------------------------

    sample = sample.sort_values(
        [
            "direction",
            "impulse_size",
        ],
        ascending=[
            True,
            False,
        ],
    ).reset_index(drop=True)

    # --------------------------------------------------
    # Example IDs
    # --------------------------------------------------

    sample.insert(
        0,
        "Example_ID",
        [
            f"EX-{i:03d}"
            for i in range(
                1,
                len(sample) + 1,
            )
        ],
    )

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sample.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    print("=" * 60)
    print("CONTINUATION REVIEW SAMPLE")
    print("=" * 60)
    print(f"Total Events     : {len(df):,}")
    print(f"Review Samples   : {len(sample):,}")
    print(f"Output           : {OUTPUT_CSV}")


if __name__ == "__main__":
    main()