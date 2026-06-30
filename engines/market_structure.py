import pandas as pd
from config.trading_config import SWING_LOOKBACK, BOS_MIN_DISPLACEMENT

class MarketStructure:

    def __init__(self, df):
        self.df = df.copy()

    def detect_swings(self, lookback=SWING_LOOKBACK):

        self.df["Swing_High"] = False
        self.df["Swing_Low"] = False
        self.df["Swing_Strength"] = 0.0

        highs = self.df["High"]
        lows = self.df["Low"]

        for i in range(lookback, len(self.df) - lookback):

            is_swing_high = (
                highs.iloc[i]
                == highs.iloc[i - lookback:i + lookback + 1].max()
            )

            is_swing_low = (
                lows.iloc[i]
                == lows.iloc[i - lookback:i + lookback + 1].min()
            )

            confirmation_index = i + lookback

            if confirmation_index >= len(self.df):
                continue

            if is_swing_high:
                self.df.iat[
                    confirmation_index,
                    self.df.columns.get_loc("Swing_High")
                ] = True

                self.df.iat[
                    confirmation_index,
                    self.df.columns.get_loc("Swing_Strength")
                ] = (
                    highs.iloc[i]
                    - lows.iloc[i - lookback:i + lookback + 1].min()
                )

            if is_swing_low:
                self.df.iat[
                    confirmation_index,
                    self.df.columns.get_loc("Swing_Low")
                ] = True

                self.df.iat[
                    confirmation_index,
                    self.df.columns.get_loc("Swing_Strength")
                ] = (
                    highs.iloc[i - lookback:i + lookback + 1].max()
                    - lows.iloc[i]
                )

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
        self.df["BOS_Level"] = None
        self.df["BOS_Displacement"] = 0.0

        last_swing_high = None
        last_swing_low = None

        for i in range(len(self.df)):

            row = self.df.iloc[i]

            if row["Swing_High"]:
                last_swing_high = {
                    "price": row["High"],
                    "strength": row["Swing_Strength"],
                    "index": i
                }

            if row["Swing_Low"]:
                last_swing_low = {
                    "price": row["Low"],
                    "strength": row["Swing_Strength"],
                    "index": i
                }

            close = row["Close"]

            # Bullish BOS
            displacement = (
                close - last_swing_high["price"]
                if last_swing_high
                else 0
            )

            # Bearish BOS
            bearish_displacement = (
                last_swing_low["price"] - close
                if last_swing_low
                else 0
            )

            if (
                last_swing_high is not None
                and displacement >= BOS_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bullish_BOS")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Level")
                ] = last_swing_high["price"]

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Displacement")
                ] = displacement

                last_swing_high = None

            elif (
                last_swing_low is not None
                and bearish_displacement >= BOS_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bearish_BOS")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Level")
                ] = last_swing_low["price"]

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Displacement")
                ] = bearish_displacement

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
    
    def detect_trend_state(self):

        self.df["Trend_State"] = "UNKNOWN"

        trend = "UNKNOWN"

        for i in range(len(self.df)):

            structure = self.df.iloc[i]["Structure"]

            if structure in ["HH", "HL"]:
                trend = "UPTREND"

            elif structure in ["LH", "LL"]:
                trend = "DOWNTREND"

            self.df.iloc[
                i,
                self.df.columns.get_loc("Trend_State")
            ] = trend

        return self.df