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
        
        return self.df
    
    def detect_bos(self):

        self.df["Bullish_BOS"] = False
        self.df["Bearish_BOS"] = False

        last_swing_high = None
        last_swing_low = None

        for i in range(len(self.df)):

            # Update latest swing levels
            if self.df.iloc[i]["Swing_High"]:
                last_swing_high = self.df.iloc[i]["High"]

            if self.df.iloc[i]["Swing_Low"]:
                last_swing_low = self.df.iloc[i]["Low"]

            close = self.df.iloc[i]["Close"]

            # Bullish BOS
            if last_swing_high is not None and close > last_swing_high:
                self.df.iloc[
                    i,
                    self.df.columns.get_loc("Bullish_BOS")
                ] = True

                last_swing_high = None

            # Bearish BOS
            if last_swing_low is not None and close < last_swing_low:
                self.df.iloc[
                    i,
                    self.df.columns.get_loc("Bearish_BOS")
                ] = True

                last_swing_low = None

        return self.df
    def detect_choch(self):

        self.df["Bullish_CHOCH"] = False
        self.df["Bearish_CHOCH"] = False

        trend = None

        for i in range(len(self.df)):

            structure = self.df.iloc[i]["Structure"]

            # Detect current trend
            if structure in ["HH", "HL"]:
                trend = "UP"

            elif structure in ["LH", "LL"]:
                trend = "DOWN"

            # Bullish CHOCH
            if (
                trend == "DOWN"
                and self.df.iloc[i]["Bullish_BOS"]
            ):
                self.df.iloc[
                    i,
                    self.df.columns.get_loc("Bullish_CHOCH")
                ] = True

                trend = "UP"

            # Bearish CHOCH
            elif (
                trend == "UP"
                and self.df.iloc[i]["Bearish_BOS"]
            ):
                self.df.iloc[
                    i,
                    self.df.columns.get_loc("Bearish_CHOCH")
                ] = True

                trend = "DOWN"

        return self.df