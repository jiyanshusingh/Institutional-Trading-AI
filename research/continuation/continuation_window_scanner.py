from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from dataclasses import asdict

INPUT_CSV = Path(
    "historical_data/normalized/ACUTAAS_1m.csv"
)

OUTPUT_CSV = Path(
    "research/continuation/continuation_windows.csv"
)


# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

LOOKAHEAD = 40

MIN_IMPULSE_PERCENT = 2.0

MIN_PULLBACK_PERCENT = 10.0
MAX_PULLBACK_PERCENT = 60.0


# -------------------------------------------------------
# Model
# -------------------------------------------------------

@dataclass(slots=True)
class ContinuationWindow:

    impulse_start: int
    impulse_end: int

    pullback_end: int

    continuation_index: int

    direction: str

    impulse_size: float

    retracement_percent: float


# -------------------------------------------------------
# Scanner
# -------------------------------------------------------

class ContinuationWindowScanner:

    def __init__(self, df):

        self.df = df.reset_index(drop=True)

    def scan(self):

        windows = []

        highs = self.df["high"].values
        lows = self.df["low"].values
        closes = self.df["close"].values

        n = len(self.df)

        for start in range(n - LOOKAHEAD):

            for impulse_end in range(
                start + 3,
                min(start + 15, n),
            ):

                start_price = closes[start]

                end_price = closes[impulse_end]

                move_percent = (
                    (end_price - start_price)
                    / start_price
                ) * 100

                # -----------------------------
                # Bullish
                # -----------------------------

                if move_percent >= MIN_IMPULSE_PERCENT:

                    impulse_high = highs[
                        start:impulse_end + 1
                    ].max()

                    impulse_low = lows[
                        start:impulse_end + 1
                    ].min()

                    impulse_range = (
                        impulse_high - impulse_low
                    )

                    if impulse_range <= 0:
                        continue

                    best_pullback = None

                    for j in range(
                        impulse_end + 1,
                        min(
                            impulse_end + 15,
                            n,
                        ),
                    ):

                        pullback_low = lows[
                            impulse_end:j + 1
                        ].min()

                        retracement = (
                            impulse_high
                            - pullback_low
                        )

                        retracement_percent = (
                            retracement
                            / impulse_range
                        ) * 100

                        if (
                            retracement_percent
                            < MIN_PULLBACK_PERCENT
                        ):
                            continue

                        if (
                            retracement_percent
                            > MAX_PULLBACK_PERCENT
                        ):
                            break

                        best_pullback = j

                        break

                    if best_pullback is None:
                        continue

                    continuation = None

                    for k in range(
                        best_pullback + 1,
                        min(
                            best_pullback + 20,
                            n,
                        ),
                    ):

                        if highs[k] > impulse_high:

                            continuation = k

                            break

                    if continuation is None:
                        continue

                    windows.append(

                        ContinuationWindow(

                            impulse_start=start,

                            impulse_end=impulse_end,

                            pullback_end=best_pullback,

                            continuation_index=continuation,

                            direction="BULLISH",

                            impulse_size=round(
                                move_percent,
                                2,
                            ),

                            retracement_percent=round(
                                retracement_percent,
                                2,
                            ),
                        )

                    )

        return windows


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    print("Starting Continuation Window Scanner...")

    df = pd.read_csv(INPUT_CSV)
    print(df.columns.tolist())

    scanner = ContinuationWindowScanner(df)

    windows = scanner.scan()

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    pd.DataFrame(
        [
            asdict(w)
            for w in windows
        ]
    ).to_csv(
        OUTPUT_CSV,
        index=False,
    )

    print("=" * 60)
    print("CONTINUATION WINDOW SCANNER")
    print("=" * 60)
    print(f"Rows          : {len(df):,}")
    print(f"Windows Found : {len(windows):,}")
    print(f"Output        : {OUTPUT_CSV}")


if __name__ == "__main__":
    main()