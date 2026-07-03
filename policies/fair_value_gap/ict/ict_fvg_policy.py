from models.fair_value_gap import FairValueGap

from policies.fair_value_gap.base_fvg_policy import (
    FairValueGapPolicy
)


class ICTFairValueGapPolicy(FairValueGapPolicy):

    def detect(
        self,
        configuration
    ):

        df = configuration.df

        fvgs = []

        for i in range(len(df) - 2):

            first = df.iloc[i]
            third = df.iloc[i + 2]

            # -------------------------
            # Bullish FVG
            # -------------------------

            if third["Low"] > first["High"]:

                fvgs.append(

                    FairValueGap(

                        start_index=i,

                        middle_index=i + 1,

                        end_index=i + 2,

                        upper_price=third["Low"],

                        lower_price=first["High"],

                        direction="BULLISH",

                        policy="ICT"

                    )

                )

            # -------------------------
            # Bearish FVG
            # -------------------------

            elif third["High"] < first["Low"]:

                fvgs.append(

                    FairValueGap(

                        start_index=i,

                        middle_index=i + 1,

                        end_index=i + 2,

                        upper_price=first["Low"],

                        lower_price=third["High"],

                        direction="BEARISH",

                        policy="ICT"

                    )

                )

        return tuple(fvgs)