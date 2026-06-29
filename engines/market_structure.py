import pandas as pd


class MarketStructure:

    def __init__(self, df):
        self.df = df.copy()

    def detect_swings(self, lookback=3):

        self.df["Swing_High"] = False
        self.df["Swing_Low"] = False

        highs = self.df["High"]
        lows = self.df["Low"]

        for i in range(lookback, len(self.df) - lookback):

            if highs.iloc[i] == highs.iloc[i-lookback:i+lookback+1].max():
                self.df.loc[self.df.index[i], "Swing_High"] = True

            if lows.iloc[i] == lows.iloc[i-lookback:i+lookback+1].min():
                self.df.loc[self.df.index[i], "Swing_Low"] = True

        return self.df

    def classify_structure(self):
        print("\nInside classify_structure:")
        print(self.df.columns)
        self.df["Structure"] = ""

        previous_high = None

        for idx in self.df[self.df["Swing_High"]].index:

            current = self.df.loc[idx, "High"]

            if previous_high is None:
                previous_high = current
                continue

            if current > previous_high:
                self.df.loc[idx, "Structure"] = "HH"
            else:
                self.df.loc[idx, "Structure"] = "LH"

            previous_high = current

        previous_low = None

        for idx in self.df[self.df["Swing_Low"]].index:

            current = self.df.loc[idx, "Low"]

            if previous_low is None:
                previous_low = current
                continue

            if current > previous_low:
                self.df.loc[idx, "Structure"] = "HL"
            else:
                self.df.loc[idx, "Structure"] = "LL"

            previous_low = current
        print("After detect_swings:")
        print(self.df.columns)
        return self.df