import pandas as pd


class SMCEngine:

    def __init__(self, df):
        self.df = df.copy()

    def detect_choch(self):

        self.df["Bullish_CHOCH"] = False
        self.df["Bearish_CHOCH"] = False

        last_bullish_bos = False
        last_bearish_bos = False

        for i in range(len(self.df)):

            # Track the latest BOS direction
            if self.df.iloc[i]["Bullish_BOS"]:
                last_bullish_bos = True
                last_bearish_bos = False

            elif self.df.iloc[i]["Bearish_BOS"]:
                last_bearish_bos = True
                last_bullish_bos = False

            # CHOCH occurs when the opposite BOS appears
            if last_bullish_bos and self.df.iloc[i]["Bearish_BOS"]:
                self.df.loc[self.df.index[i], "Bearish_CHOCH"] = True

            if last_bearish_bos and self.df.iloc[i]["Bullish_BOS"]:
                self.df.loc[self.df.index[i], "Bullish_CHOCH"] = True

        return self.df