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
            "python -m validation.semantic.visualize_break_event <Swing_ID>"
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

    break_index = int(row["Break_Index"])

    #
    # Every swing broken on the same candle
    #
    broken = (
        df[df["Break_Index"] == break_index]
        .copy()
        .sort_values("Swing_Index")
    )

    header("BREAK EVENT")

    print(f"Break Candle Index : {break_index}")
    print(f"Timestamp          : {row['Break_Timestamp']}")
    print(f"Break High         : {row['Break_High']}")
    print(f"Break Low          : {row['Break_Low']}")
    print(f"Break Close        : {row['Break_Close']}")

    header("BROKEN SWINGS")

    print(
        f"{'ID':>6} "
        f"{'Type':>6} "
        f"{'SwingIdx':>10} "
        f"{'Price':>10} "
        f"{'Latest':>8} "
        f"{'Sup':>6}"
    )

    print("-" * 60)

    for _, r in broken.iterrows():

        marker = " "

        if int(r["Swing_ID"]) == swing_id:
            marker = ">"

        latest = (
            int(r["Latest_Same_Type_Swing_ID"])
            == int(r["Swing_ID"])
        )

        print(
            f"{marker}"
            f"{int(r['Swing_ID']):>5} "
            f"{r['Swing_Type']:>6} "
            f"{int(r['Swing_Index']):>10} "
            f"{r['Swing_Price']:>10.2f} "
            f"{str(latest):>8} "
            f"{str(r['Superseded_By_Same_Type']):>6}"
        )

    header("SUMMARY")

    highs = (
        broken["Swing_Type"] == "HIGH"
    ).sum()

    lows = (
        broken["Swing_Type"] == "LOW"
    ).sum()

    print(f"Broken Swings : {len(broken)}")
    print(f"Broken Highs  : {highs}")
    print(f"Broken Lows   : {lows}")

    print()

    print(
        "Earliest Swing :",
        int(broken["Swing_Index"].min())
    )

    print(
        "Latest Swing   :",
        int(broken["Swing_Index"].max())
    )

    print(
        "Average Age    :",
        (
            break_index
            - broken["Swing_Index"]
        ).mean()
    )

    print(
        "Oldest Age     :",
        (
            break_index
            - broken["Swing_Index"]
        ).max()
    )

    print()

    print("=" * 70)
    print("END")
    print("=" * 70)


if __name__ == "__main__":
    main()