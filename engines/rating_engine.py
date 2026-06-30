class RatingEngine:

    def __init__(self, signal, probability, confluence):
        self.signal = signal
        self.probability = probability
        self.confluence = confluence

    def calculate(self):

        score = (
            self.signal["Score"] * 10
            + self.probability["Probability"] * 0.4
            + self.confluence["ConfluenceScore"] * 0.5
        )

        score = round(score)

        if score >= 85:
            stars = "★★★★★"
            rating = "Strong Buy"

        elif score >= 70:
            stars = "★★★★☆"
            rating = "Buy"

        elif score >= 55:
            stars = "★★★☆☆"
            rating = "Watch"

        elif score >= 40:
            stars = "★★☆☆☆"
            rating = "Weak"

        else:
            stars = "★☆☆☆☆"
            rating = "Avoid"

        return {
            "Stars": stars,
            "Rating": rating,
            "Score": score
        }