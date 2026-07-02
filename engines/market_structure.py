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
        self.df["Continuation_High"] = None
        self.df["Continuation_High_Index"] = None

        self.df["Continuation_Low"] = None
        self.df["Continuation_Low_Index"] = None
        
        continuation_high = None
        continuation_low = None
        
        self.df["Bullish_BOS"] = False
        self.df["Bearish_BOS"] = False

        self.df["BOS_Valid"] = False
        self.df["BOS_Type"] = None

        self.df["BOS_Level"] = None
        self.df["BOS_Displacement"] = 0.0

        # ---------------------------------------
        # NEW
        # ---------------------------------------

        self.df["BOS_Broken_Swing_Index"] = None
        for i in range(len(self.df)):

            row = self.df.iloc[i]
            protected_low = row["Protected_Low"]
            protected_low_index = row["Protected_Low_Index"]

            protected_high = row["Protected_High"]
            protected_high_index = row["Protected_High_Index"]
            continuation_high_price = (
                continuation_high["price"]
                if continuation_high is not None
                else None
            )

            continuation_high_index = (
                continuation_high["index"]
                if continuation_high is not None
                else None
            )

            continuation_low_price = (
                continuation_low["price"]
                if continuation_low is not None
                else None
            )

            continuation_low_index = (
                continuation_low["index"]
                if continuation_low is not None
                else None
            )
            # ---------------------------------------
            # Update continuation levels
            # ---------------------------------------
            if row["Structure"] == "HH":

                continuation_high = {
                    "price": row["High"],
                    "index": i
                }

            elif row["Structure"] == "LL":

                continuation_low = {
                    "price": row["Low"],
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
                close - continuation_high_price
                if continuation_high_price is not None
                else 0
            )

            bearish_displacement = (
                continuation_low_price - close
                if continuation_low_price is not None
                else 0
            )
            # ---------------------------------------
            # Bullish BOS
            # ---------------------------------------

            if (
                continuation_high_price is not None
                and protected_low is not None
                and bullish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):
                print("=" * 60)
                print("Bullish BOS")
                print("Current Candle       :", i)
                print("Continuation High    :", continuation_high_price)
                print("Continuation Index   :", continuation_high_index)
                print("Protected Low        :", protected_low)
                print("Protected Low Index  :", protected_low_index)
                print("Close                :", close)
            
                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bullish_BOS")
                ] = True
                continuation_high = None
                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Type")
                ] = "BULLISH"

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Level")
                ] = continuation_high_price

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Displacement")
                ] = bullish_displacement

                # ---------------------------------------
                # NEW
                # Store Broken Swing Index
                # ---------------------------------------

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Broken_Swing_Index")
                ] = continuation_high_index

                if body_percent >= MIN_BODY_PERCENT:

                    self.df.iat[
                        i,
                        self.df.columns.get_loc("BOS_Valid")
                    ] = True

                

            # ---------------------------------------
            # Bearish BOS
            # ---------------------------------------

            elif (
                continuation_low_price is not None
                and protected_high is not None
                and bearish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):
                print("=" * 60)
                print("Bearish BOS")
                print("Current Candle       :", i)
                print("Continuation Low     :", continuation_low_price)
                print("Continuation Index   :", continuation_low_index)
                print("Protected High       :", protected_high)
                print("Protected High Index :", protected_high_index)
                print("Close                :", close)
                print("=" * 60)
                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bearish_BOS")
                ] = True
                continuation_low = None
                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Type")
                ] = "BEARISH"

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Level")
                ] = continuation_low_price

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Displacement")
                ] = bearish_displacement

                # ---------------------------------------
                # NEW
                # Store Broken Swing Index
                # ---------------------------------------

                self.df.iat[
                    i,
                    self.df.columns.get_loc("BOS_Broken_Swing_Index")
                ] = continuation_low_index

                if body_percent >= MIN_BODY_PERCENT:

                    self.df.iat[
                        i,
                        self.df.columns.get_loc("BOS_Valid")
                    ] = True

                

        return self.df
    def detect_choch(self):

        self.df["Bullish_CHOCH"] = False
        self.df["Bearish_CHOCH"] = False

        self.df["CHOCH_Valid"] = False
        self.df["CHOCH_Type"] = None

        self.df["CHOCH_Level"] = None
        self.df["CHOCH_Displacement"] = 0.0

        self.df["CHOCH_Broken_Swing_Index"] = None
        self.df["CHOCH_Base_Swing_Index"] = None

        previous_protected_low_index = None
        previous_protected_high_index = None

        bearish_triggered = False
        bullish_triggered = False

        for i in range(len(self.df)):

            row = self.df.iloc[i]

            close = row["Close"]
            open_price = row["Open"]
            high = row["High"]
            low = row["Low"]

            protected_low = row["Protected_Low"]
            protected_low_index = row["Protected_Low_Index"]

            protected_high = row["Protected_High"]
            protected_high_index = row["Protected_High_Index"]
            # ---------------------------------------
            # Reset CHOCH trigger
            # One Protected Swing -> One CHOCH
            # ---------------------------------------

            if protected_low_index != previous_protected_low_index:

                bearish_triggered = False
                previous_protected_low_index = protected_low_index

            if protected_high_index != previous_protected_high_index:

                bullish_triggered = False
                previous_protected_high_index = protected_high_index

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
            # Displacement
            # ---------------------------------------

            bearish_displacement = (
                protected_low - close
                if protected_low is not None
                else 0
            )

            bullish_displacement = (
                close - protected_high
                if protected_high is not None
                else 0
            )
            # ---------------------------------------
            # Bearish CHOCH
            # Protected Low broken
            # ---------------------------------------

            if (
                protected_low is not None
                and not bearish_triggered
                and bearish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bearish_CHOCH")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Type")
                ] = "BEARISH"

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Level")
                ] = protected_low

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Displacement")
                ] = bearish_displacement

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Broken_Swing_Index")
                ] = protected_low_index
                
                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Base_Swing_Index")
                ] = protected_low_index

                if body_percent >= MIN_BODY_PERCENT:

                    self.df.iat[
                        i,
                        self.df.columns.get_loc("CHOCH_Valid")
                    ] = True

                bearish_triggered = True
                
                # ---------------------------------------
            # Bullish CHOCH
            # Protected High broken
            # ---------------------------------------

            elif (
                protected_high is not None
                and not bullish_triggered
                and bullish_displacement >= STRUCTURE_BREAK_MIN_DISPLACEMENT
            ):

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Bullish_CHOCH")
                ] = True

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Type")
                ] = "BULLISH"

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Level")
                ] = protected_high

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Displacement")
                ] = bullish_displacement

                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Broken_Swing_Index")
                ] = protected_high_index
                
                self.df.iat[
                    i,
                    self.df.columns.get_loc("CHOCH_Base_Swing_Index")
                ] = protected_high_index

                if body_percent >= MIN_BODY_PERCENT:

                    self.df.iat[
                        i,
                        self.df.columns.get_loc("CHOCH_Valid")
                    ] = True

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

        self.df["Protected_High_Index"] = None
        self.df["Protected_Low_Index"] = None

        pending_hl = None
        pending_lh = None

        protected_low = None
        protected_high = None

        for i in range(len(self.df)):

            structure = self.df.iloc[i]["Structure"]

            # ----------------------------------------
            # Candidate Higher Low
            # ----------------------------------------
            if structure == "HL":

                pending_hl = {
                    "index": i,
                    "price": self.df.iloc[i]["Low"]
                }

            # ----------------------------------------
            # Candidate Lower High
            # ----------------------------------------
            elif structure == "LH":

                pending_lh = {
                    "index": i,
                    "price": self.df.iloc[i]["High"]
                }

            # ----------------------------------------
            # Confirm Bullish Structure
            # HH confirms the previous HL
            # ----------------------------------------
            elif structure == "HH":

                if pending_hl is not None:

                    protected_low = pending_hl
                    protected_high = None
                    pending_hl = None

            # ----------------------------------------
            # Confirm Bearish Structure
            # LL confirms the previous LH
            # ----------------------------------------
            elif structure == "LL":

                if pending_lh is not None:

                    protected_high = pending_lh
                    protected_low = None
                    pending_lh = None

            # ----------------------------------------
            # Store Bullish Protected Swing
            # ----------------------------------------
            if protected_low is not None:

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Protected_Low")
                ] = protected_low["price"]

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Protected_Low_Index")
                ] = protected_low["index"]

            # ----------------------------------------
            # Store Bearish Protected Swing
            # ----------------------------------------
            if protected_high is not None:

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Protected_High")
                ] = protected_high["price"]

                self.df.iat[
                    i,
                    self.df.columns.get_loc("Protected_High_Index")
                ] = protected_high["index"]
        # ---------------------------------------------------
        # DEBUG (temporary)
        # Remove after validation
        # ---------------------------------------------------
        print("\n===== PROTECTED SWINGS =====\n")

        debug_columns = [
            "Structure",
            "Protected_High",
            "Protected_High_Index",
            "Protected_Low",
            "Protected_Low_Index"
        ]

        print(
            self.df[debug_columns]
            .loc[
                self.df["Structure"].isin(["HH", "HL", "LH", "LL"])
            ]
        )

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