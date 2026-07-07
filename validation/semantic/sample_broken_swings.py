from pathlib import Path

import pandas as pd

INPUT_CSV = Path(
    "validation/output/broken_swings.csv"
)

OUTPUT_CSV = Path(
    "validation/output/broken_swings_sample.csv"
)

SAMPLE_SIZE = 40
RANDOM_SEED = 42


def main():

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Broken swing file not found: {INPUT_CSV}"
        )

    df = pd.read_csv(INPUT_CSV)

    if df.empty:
        raise ValueError(
            "Broken swing file is empty."
        )

    sample_size = min(
        SAMPLE_SIZE,
        len(df),
    )

    sample = df.sample(
        n=sample_size,
        random_state=RANDOM_SEED,
    )

    sample = sample.sort_values(
        by="Break_Index"
    ).reset_index(drop=True)

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sample.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    print("=" * 60)
    print("BROKEN SWING SAMPLE")
    print("=" * 60)
    print(f"Input Rows   : {len(df)}")
    print(f"Sample Size  : {len(sample)}")
    print(f"Output File  : {OUTPUT_CSV}")


if __name__ == "__main__":
    main()