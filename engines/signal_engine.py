class SignalEngine:

    def __init__(self, df):
        self.df = df

    def generate_signal(self):

        latest = self.df.iloc[-1]

        score = 0

        reasons = []

        # EMA Alignment
        if (
            latest["EMA20"] >
            latest["EMA50"] >
            latest["EMA200"]
        ):
            score += 2
            reasons.append("EMA Alignment")

        # RSI
        if 45 <= latest["RSI"] <= 70:
            score += 1
            reasons.append("Healthy RSI")

        # Bullish BOS
        if latest["Bullish_BOS"]:
            score += 2
            reasons.append("Bullish BOS")

        # Bullish CHOCH
        if latest["Bullish_CHOCH"]:
            score += 1
            reasons.append("Bullish CHOCH")

        # Order Block
        if latest["Bullish_OB"]:
            score += 2
            reasons.append("Bullish Order Block")

        # Fair Value Gap
        if latest["Bullish_FVG"]:
            score += 1
            reasons.append("Bullish FVG")

        # Discount Zone
        if latest["Discount_Zone"]:
            score += 1
            reasons.append("Discount Zone")

        if score >= 8:
            signal = "STRONG BUY"

        elif score >= 6:
            signal = "BUY"

        elif score >= 4:
            signal = "WATCH"

        else:
            signal = "NO TRADE"

        return {
            "Score": score,
            "Signal": signal,
            "Reasons": reasons
        }