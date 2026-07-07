from pathlib import Path
import sys

import pandas as pd

INPUT_CSV = Path(
    "validation/output/broken_swings.csv"
)


def header(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python -m validation.semantic.visualize_broken_swing <Swing_ID>"
        )
        return

    swing_id = int(sys.argv[1])

    if not INPUT_CSV.exists():
        raise FileNotFoundError(INPUT_CSV)

    df = pd.read_csv(INPUT_CSV)

    row = df[df["Swing_ID"] == swing_id]

    if row.empty:
        print(f"Swing_ID {swing_id} not found.")
        return

    row = row.iloc[0]

    header("BROKEN SWING")

    print(f"Swing ID              : {int(row['Swing_ID'])}")
    print(f"Swing Type            : {row['Swing_Type']}")
    print(f"Swing Index           : {int(row['Swing_Index'])}")
    print(
        f"Confirmation Index    : "
        f"{int(row['Confirmation_Index'])}"
    )
    print(f"Swing Timestamp       : {row['Swing_Timestamp']}")
    print(f"Swing Price           : {row['Swing_Price']}")

    header("STRUCTURAL CONTEXT")

    print(
        f"Previous Same Type    : "
        f"{row['Previous_Same_Type_Swing_ID']}"
    )

    print(
        f"Latest Same Type      : "
        f"{row['Latest_Same_Type_Swing_ID']}"
    )

    print(
        f"Superseded            : "
        f"{row['Superseded_By_Same_Type']}"
    )

    print(
        f"Same-Type Before Break: "
        f"{int(row['Same_Type_Swings_Before_Break'])}"
    )

    print(
        f"Opp-Type Before Break : "
        f"{int(row['Opposite_Type_Swings_Before_Break'])}"
    )

    header("BREAK")

    print(
        f"Break Candle Index    : "
        f"{int(row['Break_Index'])}"
    )

    print(
        f"Break Timestamp       : "
        f"{row['Break_Timestamp']}"
    )

    print(
        f"Break Price           : "
        f"{row['Break_Price']}"
    )

    print(
        f"Break High            : "
        f"{row['Break_High']}"
    )

    print(
        f"Break Low             : "
        f"{row['Break_Low']}"
    )

    print(
        f"Break Close           : "
        f"{row['Break_Close']}"
    )

    print(
        f"Candles To Break      : "
        f"{int(row['Candles_To_Break'])}"
    )

    header("SURROUNDING SWINGS")

    start = max(0, swing_id - 4)
    end = min(len(df), swing_id + 3)

    subset = df.iloc[start:end]

    print(
        f"{'ID':>6} "
        f"{'Type':>6} "
        f"{'Index':>8} "
        f"{'Price':>10}"
    )

    print("-" * 40)

    for _, r in subset.iterrows():

        marker = " "

        if int(r["Swing_ID"]) == swing_id:
            marker = ">"

        print(
            f"{marker}"
            f"{int(r['Swing_ID']):>5} "
            f"{r['Swing_Type']:>6} "
            f"{int(r['Swing_Index']):>8} "
            f"{r['Swing_Price']:>10.2f}"
        )

    print()

    print("=" * 70)
    print("END")
    print("=" * 70)


if __name__ == "__main__":
    main()