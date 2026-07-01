import pandas as pd
class ValidationEngine:

    def __init__(self, df):
        self.df = df

    def validate_swings(self):
        errors = []
        swing_high_indices = self.df[self.df["Swing_High"]].index.tolist()
        swing_low_indices = self.df[self.df["Swing_Low"]].index.tolist()

        # Rule 1: A candle cannot be both Swing High and Swing Low
        for i in range(len(self.df)):
            if (
                self.df.iloc[i]["Swing_High"]
                and self.df.iloc[i]["Swing_Low"]
            ):
                errors.append(
                    f"Row {i}: Candle is both Swing High and Swing Low."
                )
        return {
        "passed": len(errors) == 0,
        "errors": errors
    }
    def validate_structure(self):

        errors = []

        for i in range(len(self.df)):

            swing_high = self.df.iloc[i]["Swing_High"]
            swing_low = self.df.iloc[i]["Swing_Low"]
            structure = self.df.iloc[i]["Structure"]

            # Rule 1
            if swing_high and structure not in ["HH", "LH", ""]:
                errors.append(
                    f"Row {i}: Swing High has invalid structure '{structure}'."
                )

            # Rule 2
            if swing_low and structure not in ["HL", "LL", ""]:
                errors.append(
                    f"Row {i}: Swing Low has invalid structure '{structure}'."
                )

            # Rule 3
            if (
                not swing_high
                and not swing_low
                and structure != ""
            ):
                errors.append(
                    f"Row {i}: Non-swing candle has structure '{structure}'."
                )

            # Rule 4
            if (
                (swing_high or swing_low)
                and structure == ""
            ):
                errors.append(
                    f"Row {i}: Swing candle missing structure."
                )

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    def validate_trend_candidate(self):

        errors = []

        for i in range(len(self.df)):

            structure = self.df.iloc[i]["Structure"]
            trend = self.df.iloc[i]["Trend_Candidate"]

            if structure in ["HH", "HL"]:

                if trend != "UPTREND":

                    errors.append(
                        f"Row {i}: {structure} should produce UPTREND."
                    )

            elif structure in ["LH", "LL"]:

                if trend != "DOWNTREND":

                    errors.append(
                        f"Row {i}: {structure} should produce DOWNTREND."
                    )

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    def validate_protected_swings(self):

        errors = []

        for i in range(len(self.df)):

            market_state = self.df.iloc[i]["Market_State"]

            protected_low = self.df.iloc[i]["Protected_Low"]
            protected_high = self.df.iloc[i]["Protected_High"]

            has_low = pd.notna(protected_low)
            has_high = pd.notna(protected_high)

            # Rule 1
            if has_low and has_high:
                errors.append(
                    f"Row {i}: Both Protected_Low and Protected_High exist."
                )
        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    def validate_bos(self):

        errors = []

        ...

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    def validate_choch(self):

        errors = []

        for i in range(len(self.df)):

            trend_candidate = self.df.iloc[i]["Trend_Candidate"]
            
            bullish_choch = self.df.iloc[i]["Bullish_CHOCH"]
            bearish_choch = self.df.iloc[i]["Bearish_CHOCH"]

            protected_low = self.df.iloc[i]["Protected_Low"]
            protected_high = self.df.iloc[i]["Protected_High"]

            has_low = pd.notna(protected_low)
            has_high = pd.notna(protected_high)
            
            # --------------------------------------------------
            # Rule 1
            # Cannot have both CHOCHs on same candle
            # --------------------------------------------------

            if bullish_choch and bearish_choch:

                errors.append(
                    f"Row {i}: Candle cannot be both Bullish_CHOCH and Bearish_CHOCH."
                )

            # --------------------------------------------------
            # Rule 2
            # Bullish CHOCH only from Downtrend / Transition
            # --------------------------------------------------

            if (
                bullish_choch
                and self.df.iloc[i]["Trend_Candidate"] != "DOWNTREND"
            ):
                errors.append(
                    f"Row {i}: Bullish_CHOCH requires DOWNTREND Trend_Candidate."
                )

            # --------------------------------------------------
            # Rule 3
            # Bearish CHOCH only from Uptrend / Transition
            # --------------------------------------------------

            if (
                bearish_choch
                and self.df.iloc[i]["Trend_Candidate"] != "UPTREND"
            ):
                errors.append(
                    f"Row {i}: Bearish_CHOCH requires UPTREND Trend_Candidate."
                )
            # --------------------------------------------------
            # Rule 4
            # Bullish CHOCH requires Protected High
            # --------------------------------------------------

            if bullish_choch and not has_high:

                errors.append(
                    f"Row {i}: Bullish_CHOCH without Protected_High."
                )

            # --------------------------------------------------
            # Rule 5
            # Bearish CHOCH requires Protected Low
            # --------------------------------------------------

            if bearish_choch and not has_low:

                errors.append(
                    f"Row {i}: Bearish_CHOCH without Protected_Low."
                )

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    def validate_market_state(self):

        return {
            "passed": True,
            "errors": []
        }

    def validate_all(self):

        validators = {
            "Swings": self.validate_swings(),
            "Structure": self.validate_structure(),
            "Trend": self.validate_trend_candidate(),
            "Protected Swings": self.validate_protected_swings(),
            "BOS": self.validate_bos(),
            "CHOCH": self.validate_choch(),
            "Market State": self.validate_market_state()
        }

        passed = all(v["passed"] for v in validators.values())

        return {
            "passed": passed,
            "results": validators
        }