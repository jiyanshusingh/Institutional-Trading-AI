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
        ...

    def validate_trend_candidate(self):
        ...

    def validate_protected_swings(self):
        ...

    def validate_bos(self):
        ...

    def validate_choch(self):
        ...

    def validate_market_state(self):
        ...

    def validate_all(self):
        ...