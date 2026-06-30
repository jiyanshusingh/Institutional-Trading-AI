class ProbabilityEngine:

    def __init__(self, df, signal):
        self.df = df
        self.signal = signal

    def calculate(self):

        latest = self.df.iloc[-1]

        score = self.signal["Score"]

        # -----------------------------
        # Probability
        # -----------------------------
        probability = min(95, score * 12 + 20)

        # -----------------------------
        # Confidence
        # -----------------------------
        if probability >= 85:
            confidence = "Very High"
        elif probability >= 75:
            confidence = "High"
        elif probability >= 60:
            confidence = "Medium"
        else:
            confidence = "Low"

        # -----------------------------
        # Trend
        # -----------------------------
        if latest["EMA20"] > latest["EMA50"] > latest["EMA200"]:
            trend = "Bullish"

        elif latest["EMA20"] < latest["EMA50"] < latest["EMA200"]:
            trend = "Bearish"

        else:
            trend = "Sideways"

        # -----------------------------
        # Momentum
        # -----------------------------
        rsi = latest["RSI"]

        if rsi >= 65:
            momentum = "Strong"

        elif rsi >= 50:
            momentum = "Moderate"

        else:
            momentum = "Weak"

        # -----------------------------
        # Institutional Bias
        # -----------------------------
        if latest["Premium_Zone"]:
            bias = "Premium"

        elif latest["Discount_Zone"]:
            bias = "Discount"

        else:
            bias = "Neutral"

        return {

            "Probability": probability,

            "Confidence": confidence,

            "Trend": trend,

            "Momentum": momentum,

            "InstitutionalBias": bias,

            "Recommendation": self.signal["Signal"]

        }