import pandas as pd


class OrderBlockEngine:

    def __init__(self, df):
        self.df = df.copy()

    def detect_order_blocks(self):

        self.df["Bullish_OB"] = False
        self.df["Bearish_OB"] = False
        for i in range(1, len(self.df)):

            if self.df.iloc[i]["Bullish_BOS"]:

                for j in range(i - 1, -1, -1):

                    open_price = self.df.iloc[j]["Open"]
                    close_price = self.df.iloc[j]["Close"]

                    # Bearish candle
                    if close_price < open_price:

                        self.df.iloc[
                            j,
                            self.df.columns.get_loc("Bullish_OB")
                        ] = True

                        break
        for i in range(1, len(self.df)):

            if self.df.iloc[i]["Bearish_BOS"]:

                for j in range(i - 1, -1, -1):

                    open_price = self.df.iloc[j]["Open"]
                    close_price = self.df.iloc[j]["Close"]

                    # Bullish candle
                    if close_price > open_price:

                        self.df.iloc[
                            j,
                            self.df.columns.get_loc("Bearish_OB")
                        ] = True

                        break

        return self.df