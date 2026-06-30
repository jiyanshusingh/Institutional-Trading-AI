import pandas as pd

from config.trading_config import (
    SWING_LOOKBACK,
    MIN_SWING_ATR,
)

from utils.market_utils import atr_displacement


class SwingEngine:

    def __init__(self, df):
        self.df = df.copy()

    def detect(self):

        self.df["Swing_High"] = False
        self.df["Swing_Low"] = False
        self.df["Swing_Strength"] = 0.0

        highs = self.df["High"]
        lows = self.df["Low"]
        atr = self.df["ATR"]

        lookback = SWING_LOOKBACK

        for i in range(lookback, len(self.df) - lookback):

            # -------------------------
            # Swing High
            # -------------------------
            if highs.iloc[i] == highs.iloc[
                i - lookback:i + lookback + 1
            ].max():

                displacement = atr_displacement(
                    highs.iloc[i],
                    lows.iloc[i],
                    atr.iloc[i]
                )

                if displacement >= MIN_SWING_ATR:

                    self.df.loc[
                        self.df.index[i],
                        "Swing_High"
                    ] = True

                    self.df.loc[
                        self.df.index[i],
                        "Swing_Strength"
                    ] = round(displacement, 2)

            # -------------------------
            # Swing Low
            # -------------------------
            if lows.iloc[i] == lows.iloc[
                i - lookback:i + lookback + 1
            ].min():

                displacement = atr_displacement(
                    highs.iloc[i],
                    lows.iloc[i],
                    atr.iloc[i]
                )

                if displacement >= MIN_SWING_ATR:

                    self.df.loc[
                        self.df.index[i],
                        "Swing_Low"
                    ] = True

                    self.df.loc[
                        self.df.index[i],
                        "Swing_Strength"
                    ] = round(displacement, 2)

        return self.df