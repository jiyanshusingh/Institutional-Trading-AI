import pandas as pd


class PremiumDiscountEngine:

    def __init__(self, df):
        self.df = df.copy()

    def detect_zones(self):

        self.df["Premium_Zone"] = False
        self.df["Discount_Zone"] = False
        self.df["Equilibrium"] = None

        last_high = None
        last_low = None

        for i in range(len(self.df)):

            if self.df.iloc[i]["Swing_High"]:
                last_high = self.df.iloc[i]["High"]

            if self.df.iloc[i]["Swing_Low"]:
                last_low = self.df.iloc[i]["Low"]

            if last_high is not None and last_low is not None:

                eq = (last_high + last_low) / 2
                self.df.loc[self.df.index[i], "Equilibrium"] = eq

                close = self.df.iloc[i]["Close"]

                if close > eq:
                    self.df.loc[self.df.index[i], "Premium_Zone"] = True
                else:
                    self.df.loc[self.df.index[i], "Discount_Zone"] = True

        return self.df