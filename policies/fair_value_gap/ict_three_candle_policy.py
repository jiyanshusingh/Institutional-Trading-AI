from models.fair_value_gap import FairValueGap


class ICTThreeCandleFVGPolicy:

    """
    ICT Three-Candle Fair Value Gap Detection Policy

    Bullish FVG
    ------------
    High(C1) < Low(C3)

    Gap:
        High(C1) -> Low(C3)

    Bearish FVG
    ------------
    Low(C1) > High(C3)

    Gap:
        High(C3) -> Low(C1)

    Rules
    -----
    - Detect every valid FVG.
    - Candle colour is ignored.
    - Dojis are valid.
    - Overlapping FVGs are allowed.
    - FVGs are never merged.
    """

    def detect(self, df):

        fvgs = []

        for i in range(len(df) - 2):

            c1 = df.iloc[i]
            c3 = df.iloc[i + 2]

            # -----------------------
            # Bullish FVG
            # -----------------------

            if c1["High"] < c3["Low"]:

                fvgs.append(

                    FairValueGap(

                        upper_price=c3["Low"],

                        lower_price=c1["High"]

                    )

                )
            # -----------------------
            # Bearish FVG
            # -----------------------

            elif c1["Low"] > c3["High"]:

                fvgs.append(

                    FairValueGap(

                        upper_price=c1["Low"],

                        lower_price=c3["High"]

                    )

                )

        return fvgs