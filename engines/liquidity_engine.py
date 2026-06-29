import pandas as pd


class LiquidityEngine:

    def __init__(self, df):
        self.df = df.copy()

    def detect_liquidity_sweeps(self):

        self.df["Buy_Side_Liquidity"] = False
        self.df["Sell_Side_Liquidity"] = False

        last_swing_high = None
        last_swing_low = None

        for i in range(len(self.df)):

            # Store latest swing levels
            if self.df.iloc[i]["Swing_High"]:
                last_swing_high = self.df.iloc[i]["High"]

            if self.df.iloc[i]["Swing_Low"]:
                last_swing_low = self.df.iloc[i]["Low"]

            # Buy-side liquidity sweep
            if last_swing_high is not None:

                if (
                    self.df.iloc[i]["High"] > last_swing_high
                    and self.df.iloc[i]["Close"] < last_swing_high
                ):
                    self.df.loc[
                        self.df.index[i],
                        "Buy_Side_Liquidity"
                    ] = True

            # Sell-side liquidity sweep
            if last_swing_low is not None:

                if (
                    self.df.iloc[i]["Low"] < last_swing_low
                    and self.df.iloc[i]["Close"] > last_swing_low
                ):
                    self.df.loc[
                        self.df.index[i],
                        "Sell_Side_Liquidity"
                    ] = True

        return self.df