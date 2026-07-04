"""
Market Interpretation

Theory 1.0

Represents the theory-dependent interpretation of an immutable
CanonicalMarketModel.

This object is immutable and contains no computation.
"""

from dataclasses import dataclass
from enum import Enum


class MarketBias(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class TrendStrength(Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"


class StructuralAlignment(Enum):
    ALIGNED = "ALIGNED"
    MIXED = "MIXED"
    CONFLICTING = "CONFLICTING"


class LiquidityContext(Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    BALANCED = "BALANCED"


@dataclass(frozen=True, slots=True)
class MarketInterpretation:
    """
    Immutable interpretation of the market.
    """

    market_bias: MarketBias

    trend_strength: TrendStrength

    structural_alignment: StructuralAlignment

    liquidity_context: LiquidityContext

    confidence: float

    def __post_init__(self):

        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                "Confidence must be between 0.0 and 1.0."
            )

    @property
    def is_bullish(self) -> bool:
        return self.market_bias == MarketBias.BULLISH

    @property
    def is_bearish(self) -> bool:
        return self.market_bias == MarketBias.BEARISH

    @property
    def is_neutral(self) -> bool:
        return self.market_bias == MarketBias.NEUTRAL