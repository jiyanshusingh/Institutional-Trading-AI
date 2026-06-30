class ProbabilityEngine:

    def __init__(self, df):
        self.df = df

    def calculate(self):

        latest = self.df.iloc[-1]

        score = 0
        reasons = []

        # =====================================================
        # Trend (25)
        # =====================================================
        if latest["EMA20"] > latest["EMA50"] > latest["EMA200"]:
            score += 25
            reasons.append("Bullish EMA Alignment")

        # =====================================================
        # RSI (10)
        # =====================================================
        if 50 <= latest["RSI"] <= 70:
            score += 10
            reasons.append("Healthy RSI")

        # =====================================================
        # Market Structure (25)
        # =====================================================
        if latest["Bullish_BOS"]:
            score += 15
            reasons.append("Bullish BOS")

        if latest["Bullish_CHOCH"]:
            score += 10
            reasons.append("Bullish CHOCH")

        # =====================================================
        # Liquidity (10)
        # =====================================================
        if latest["Sell_Side_Liquidity"]:
            score += 10
            reasons.append("Sell Side Liquidity Grab")

        # =====================================================
        # Premium / Discount (10)
        # =====================================================
        if latest["Discount_Zone"]:
            score += 10
            reasons.append("Discount Zone")

        # =====================================================
        # Order Block (10)
        # =====================================================
        if latest["Bullish_OB"]:
            score += 10
            reasons.append("Bullish Order Block")

        # =====================================================
        # Fair Value Gap (10)
        # =====================================================
        if latest["Bullish_FVG"]:
            score += 10
            reasons.append("Bullish Fair Value Gap")

        # =====================================================
        # Probability
        # =====================================================
        probability = min(score, 95)

        # =====================================================
        # Confidence
        # =====================================================
        if probability >= 85:
            confidence = "Very High"

        elif probability >= 70:
            confidence = "High"

        elif probability >= 55:
            confidence = "Medium"

        else:
            confidence = "Low"

        # =====================================================
        # Trend Label
        # =====================================================
        if latest["EMA20"] > latest["EMA50"] > latest["EMA200"]:
            trend = "Bullish"

        elif latest["EMA20"] < latest["EMA50"] < latest["EMA200"]:
            trend = "Bearish"

        else:
            trend = "Sideways"

        # =====================================================
        # Momentum
        # =====================================================
        if latest["RSI"] >= 65:
            momentum = "Strong"

        elif latest["RSI"] >= 50:
            momentum = "Moderate"

        else:
            momentum = "Weak"

        # =====================================================
        # Institutional Bias
        # =====================================================
        if latest["Premium_Zone"]:
            bias = "Premium"

        elif latest["Discount_Zone"]:
            bias = "Discount"

        else:
            bias = "Neutral"

        # =====================================================
        # Return
        # =====================================================
        return {

            "Probability": probability,

            "Confidence": confidence,

            "Trend": trend,

            "Momentum": momentum,

            "InstitutionalBias": bias,

            "Reasons": reasons

        }