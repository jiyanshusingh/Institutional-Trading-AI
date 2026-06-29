import pandas as pd


class FVGEngine:

    def __init__(self, df):
        self.df = df.copy()

    def detect_fvg(self):

        self.df["Bullish_FVG"] = False
        self.df["Bearish_FVG"] = False

        self.df["FVG_High"] = None
        self.df["FVG_Low"] = None

        for i in range(1, len(self.df) - 1):

            prev = self.df.iloc[i - 1]
            curr = self.df.iloc[i]
            nxt = self.df.iloc[i + 1]

            # Bullish Fair Value Gap
            if prev["High"] < nxt["Low"]:

                self.df.loc[self.df.index[i], "Bullish_FVG"] = True
                self.df.loc[self.df.index[i], "FVG_High"] = nxt["Low"]
                self.df.loc[self.df.index[i], "FVG_Low"] = prev["High"]

            # Bearish Fair Value Gap
            if prev["Low"] > nxt["High"]:

                self.df.loc[self.df.index[i], "Bearish_FVG"] = True
                self.df.loc[self.df.index[i], "FVG_High"] = prev["Low"]
                self.df.loc[self.df.index[i], "FVG_Low"] = nxt["High"]

        return self.df