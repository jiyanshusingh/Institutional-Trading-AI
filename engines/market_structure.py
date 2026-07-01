import pandas as pd
from config.trading_config import (
    SWING_LOOKBACK,
    STRUCTURE_BREAK_MIN_DISPLACEMENT,
    MIN_BODY_PERCENT
)

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

        self.df["BOS_Valid"] = False
        self.df["BOS_Type"] = None

        self.df["BOS_Level"] = None
        self.df["BOS_Displacement"] = 0.0

        continuation_high = None
        continuation_low = None

        for i in range(len(self.df)):

            row = self.df.iloc[i]

            # ---------------------------------------
            # Update continuation levels
            # ---------------------------------------

            if row["Structure"] == "HH":

                continuation_high = {
                    "price": row["High"],
                    "strength": row["Swing_Strength"],
                    "index": i
                }

            elif row["Structure"] == "LL":

                continuation_low = {
                    "price": row["Low"],
                    "strength": row["Swing_Strength"],
                    "index": i
                }

            close = row["Close"]
            open_price = row["Open"]
            high = row["High"]
            low = row["Low"]

            # ---------------------------------------
            # Candle quality
            # ---------------------------------------

            body = abs(close - open_price)
            range_size = high - low

            body_percent = (
                body / range_size
                if range_size > 0
                else 0
            )

            # ---------------------------------------
            # Calculate displacement
            # ---------------------------------------

            bullish_displacement = (
                close - continuation_high["price"]
                if continuation_high
                else 0
            )

            bearish_displacement = (
                continuation_low["price"] - close
                if continuation_low
                else 0
            )

            # ---------------------------------------
            # Bullish BOS
            # ---------------------------------------

            if (
                continuation_high is not None
                and bullish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bullish_BOS")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Type")
                ] = "BULLISH"

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Level")
                ] = continuation_high["price"]

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Displacement")
                ] = bullish_displacement

                if body_percent >= MIN_BODY_PERCENT:

                    self.df.iat[
                        i,
                        self.df.columns.get_loc("BOS_Valid")
                    ] = True

                continuation_high = None

            # ---------------------------------------
            # Bearish BOS
            # ---------------------------------------

            elif (
                continuation_low is not None
                and bearish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bearish_BOS")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Type")
                ] = "BEARISH"

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Level")
                ] = continuation_low["price"]

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Displacement")
                ] = bearish_displacement

                if body_percent >= MIN_BODY_PERCENT:

                    self.df.iat[
                        i,
                        self.df.columns.get_loc("BOS_Valid")
                    ] = True

                continuation_low = None

        return self.df
    def detect_choch(self):

        self.df["Bullish_CHOCH"] = False
        self.df["Bearish_CHOCH"] = False
        self.df["CHOCH_Level"] = None
        self.df["CHOCH_Displacement"] = 0.0

        previous_protected_low = None
        previous_protected_high = None

        bullish_triggered = False
        bearish_triggered = False

        for i in range(len(self.df)):

            close = self.df.iloc[i]["Close"]
            trend = self.df.iloc[i]["Trend_Candidate"]

            protected_low = self.df.iloc[i]["Protected_Low"]
            protected_high = self.df.iloc[i]["Protected_High"]

            # Reset trigger when a new protected low is created
            if protected_low != previous_protected_low:
                bearish_triggered = False
                previous_protected_low = protected_low

            # Reset trigger when a new protected high is created
            if protected_high != previous_protected_high:
                bullish_triggered = False
                previous_protected_high = protected_high

            # Calculate displacement
            bearish_displacement = (
                protected_low - close
                if protected_low is not None and pd.notna(protected_low)
                else 0
            )

            bullish_displacement = (
                close - protected_high
                if protected_high is not None and pd.notna(protected_high)
                else 0
            )

            # ------------------------
            # Bearish CHOCH
            # ------------------------
            if (
                trend == "UPTREND"
                and protected_low is not None
                and pd.notna(protected_low)
                and not bearish_triggered
                and bearish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bearish_CHOCH")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Level")
                ] = protected_low

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Displacement")
                ] = bearish_displacement

                bearish_triggered = True

            # ------------------------
            # Bullish CHOCH
            # ------------------------
            elif (
                trend == "DOWNTREND"
                and protected_high is not None
                and pd.notna(protected_high)
                and not bullish_triggered
                and bullish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bullish_CHOCH")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Level")
                ] = protected_high

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Displacement")
                ] = bullish_displacement

                bullish_triggered = True

        return self.df
        
    def detect_trend_candidate(self):

        self.df["Trend_Candidate"] = "UNKNOWN"

        trend = "UNKNOWN"

        pending_hl = False
        pending_lh = False

        for i in range(len(self.df)):

            structure = self.df.iloc[i]["Structure"]

        # ----------------------------
        # Bullish sequence
        # ----------------------------
            if structure == "HL":
                pending_hl = True

            elif structure == "HH":

                if pending_hl:
                    trend = "UPTREND"
                    pending_hl = False
                    pending_lh = False

        # ----------------------------
        # Bearish sequence
        # ----------------------------
            elif structure == "LH":
                pending_lh = True

            elif structure == "LL":

                if pending_lh:
                    trend = "DOWNTREND"
                    pending_lh = False
                    pending_hl = False

            self.df.iat[
                i,
                self.df.columns.get_loc("Trend_Candidate")
            ] = trend

        return self.df
    
    def detect_protected_swings(self):

        self.df["Protected_High"] = None
        self.df["Protected_Low"] = None

        pending_hl = None
        pending_lh = None

        protected_low = None
        protected_high = None

        for i in range(len(self.df)):

            structure = self.df.iloc[i]["Structure"]

            # Candidate Higher Low
            if structure == "HL":
                pending_hl = self.df.iloc[i]["Low"]

            # Candidate Lower High
            elif structure == "LH":
                pending_lh = self.df.iloc[i]["High"]

            # Confirm bullish impulse
            elif structure == "HH":
                if pending_hl is not None:
                    protected_low = pending_hl
                    protected_high = None
                    pending_hl = None

            # Confirm bearish impulse
            elif structure == "LL":
                if pending_lh is not None:
                    protected_high = pending_lh
                    protected_low = None
                    pending_lh = None

            self.df.iat[
                i,
                self.df.columns.get_loc("Protected_Low")
            ] = protected_low

            self.df.iat[
                i,
                self.df.columns.get_loc("Protected_High")
            ] = protected_high

        return self.df
    
    def detect_market_state(self):

        self.df["Market_State"] = "UNKNOWN"

        state = "UNKNOWN"

        for i in range(len(self.df)):

            bullish_bos = self.df.iloc[i]["Bullish_BOS"]
            bearish_bos = self.df.iloc[i]["Bearish_BOS"]

            bullish_choch = self.df.iloc[i]["Bullish_CHOCH"]
            bearish_choch = self.df.iloc[i]["Bearish_CHOCH"]

            trend_candidate = self.df.iloc[i]["Trend_Candidate"]

            # -------------------------------------------------
            # Initialize
            # -------------------------------------------------
            if state == "UNKNOWN":

                if trend_candidate == "UPTREND":
                    state = "UPTREND"

                elif trend_candidate == "DOWNTREND":
                    state = "DOWNTREND"

            # -------------------------------------------------
            # Uptrend
            # -------------------------------------------------
            elif state == "UPTREND":

                if bearish_choch:
                    state = "TRANSITION"

            # -------------------------------------------------
            # Downtrend
            # -------------------------------------------------
            elif state == "DOWNTREND":

                if bullish_choch:
                    state = "TRANSITION"

            # -------------------------------------------------
            # Transition
            # -------------------------------------------------
            elif state == "TRANSITION":

                # Reversal confirmed
                if bearish_bos:
                    state = "DOWNTREND"

                elif bullish_bos:
                    state = "UPTREND"

                # Failed reversal
                elif trend_candidate == "UPTREND":
                    state = "UPTREND"

                elif trend_candidate == "DOWNTREND":
                    state = "DOWNTREND"

            self.df.iat[
                i,
                self.df.columns.get_loc("Market_State")
            ] = state

        return self.df