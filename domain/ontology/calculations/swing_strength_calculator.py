"""
Swing Strength Calculator

Theory 1.0

Calculates normalized swing strength.

Current definition

(high - low) / ATR
"""

class SwingStrengthCalculator:

    def calculate(
        self,
        *,
        high: float,
        low: float,
        atr: float,
    ) -> float:

        if atr < 0:
            raise ValueError(
                "ATR cannot be negative."
            )

        if high < low:
            raise ValueError(
                "High cannot be below Low."
            )

        if atr == 0:
            return 0.0

        strength = (
            high - low
        ) / atr

        return round(
            strength,
            2,
        )