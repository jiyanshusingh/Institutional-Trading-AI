from pathlib import Path

import pandas as pd


INPUT_CSV = Path(
    "research/continuation/continuation_windows.csv"
)

OUTPUT_CSV = Path(
    "research/continuation/continuation_events.csv"
)


MERGE_DISTANCE = 2


def main():

    df = pd.read_csv(INPUT_CSV)

    if df.empty:

        print("No continuation windows found.")
        return

    df = df.sort_values(
        "continuation_index"
    ).reset_index(drop=True)

    events = []

    current_group = [df.iloc[0]]

    for i in range(1, len(df)):

        previous = current_group[-1]

        current = df.iloc[i]

        if (
            current["continuation_index"]
            - previous["continuation_index"]
        ) <= MERGE_DISTANCE:

            current_group.append(current)

        else:

            representative = max(
                current_group,
                key=lambda row: row["impulse_size"],
            )

            events.append(representative)

            current_group = [current]

    representative = max(
        current_group,
        key=lambda row: row["impulse_size"],
    )

    events.append(representative)

    result = pd.DataFrame(events)

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    print("=" * 60)
    print("CONTINUATION EVENT GROUPING")
    print("=" * 60)
    print(f"Input Windows : {len(df):,}")
    print(f"Events        : {len(result):,}")
    print(
        "Reduction     : "
        f"{100 * (1 - len(result) / len(df)):.2f}%"
    )
    print(f"Output        : {OUTPUT_CSV}")


if __name__ == "__main__":
    main()