class RiskEngine:

    def __init__(self, df):
        self.df = df

    def calculate(self):

        latest = self.df.iloc[-1]

        entry = latest["Close"]

        atr = latest["ATR"]

        stop = entry - (1.5 * atr)

        target1 = entry + (2 * atr)

        target2 = entry + (4 * atr)

        rr = round((target1 - entry) / (entry - stop), 2)

        return {
            "Entry": round(entry, 2),
            "StopLoss": round(stop, 2),
            "Target1": round(target1, 2),
            "Target2": round(target2, 2),
            "RR": rr
        }