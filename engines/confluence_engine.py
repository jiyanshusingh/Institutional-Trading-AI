class ConfluenceEngine:

    def __init__(self, df, signal):
        self.df = df
        self.signal = signal

    def calculate(self):

        latest = self.df.iloc[-1]

        score = 0
        reasons = []

        # EMA Trend
        if latest["EMA20"] > latest["EMA50"] > latest["EMA200"]:
            score += 15
            reasons.append("Bullish EMA Alignment")

        # RSI
        if 50 <= latest["RSI"] <= 70:
            score += 10
            reasons.append("Healthy RSI")

        # BOS
        if latest["Bullish_BOS"]:
            score += 15
            reasons.append("Bullish BOS")

        # CHOCH
        if latest["Bullish_CHOCH"]:
            score += 10
            reasons.append("Bullish CHOCH")

        # Liquidity
        if latest["Sell_Side_Liquidity"]:
            score += 10
            reasons.append("Sell Side Liquidity Grab")

        # Discount Zone
        if latest["Discount_Zone"]:
            score += 15
            reasons.append("Discount Zone")

        # Order Block
        if latest["Bullish_OB"]:
            score += 15
            reasons.append("Bullish Order Block")

        # Fair Value Gap
        if latest["Bullish_FVG"]:
            score += 10
            reasons.append("Bullish FVG")

        return {
            "ConfluenceScore": score,
            "Reasons": reasons
        }