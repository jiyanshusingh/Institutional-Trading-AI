"""
ICT Market Interpreter

Theory 1.0

Interprets a CanonicalMarketModel and produces a
MarketInterpretation with bias, trend strength,
structural alignment, and liquidity context.
"""

from domain.interpretation.market_interpretation import (
    MarketInterpretation,
    MarketBias,
    TrendStrength,
    StructuralAlignment,
    LiquidityContext,
)
from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)
from domain.ontology.structure_event import (
    StructureEventType,
)
from domain.ontology.expansion import ExpansionDirection


class ICTMarketInterpreter:
    """
    ICT Market Interpreter.

    Converts objective semantic facts into
    theory-dependent market interpretation.
    """

    @property
    def interpreter_name(self) -> str:
        return "ICTMarketInterpreter"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    def interpret(
        self,
        market: CanonicalMarketModel,
    ) -> MarketInterpretation:
        """
        Produce a MarketInterpretation from the
        CanonicalMarketModel.
        """

        market_bias = self._determine_bias(market)

        trend_strength = self._determine_trend_strength(market)

        structural_alignment = self._determine_alignment(market)

        liquidity_context = self._determine_liquidity_context(market)

        confidence = self._calculate_confidence(
            market_bias,
            trend_strength,
            structural_alignment,
        )

        return MarketInterpretation(
            market_bias=market_bias,
            trend_strength=trend_strength,
            structural_alignment=structural_alignment,
            liquidity_context=liquidity_context,
            confidence=confidence,
        )

    # ==========================================================
    # Interpretation Rules
    # ==========================================================

    def _determine_bias(
        self,
        market: CanonicalMarketModel,
    ) -> MarketBias:

        if not market.expansions:
            return MarketBias.NEUTRAL

        latest = market.expansions[-1]

        if latest.direction == ExpansionDirection.BULLISH:
            return MarketBias.BULLISH

        if latest.direction == ExpansionDirection.BEARISH:
            return MarketBias.BEARISH

        return MarketBias.NEUTRAL

    def _determine_trend_strength(
        self,
        market: CanonicalMarketModel,
    ) -> TrendStrength:

        swing_count = len(market.swings)
        event_count = len(market.structure_events)
        protected_count = len(market.protected_swings)

        score = 0
        if swing_count >= 6:
            score += 1
        if event_count >= 2:
            score += 1
        if protected_count >= 1:
            score += 1
        if len(market.expansions) >= 1:
            score += 1

        if score >= 3:
            return TrendStrength.STRONG
        if score >= 2:
            return TrendStrength.MODERATE
        return TrendStrength.WEAK

    def _determine_alignment(
        self,
        market: CanonicalMarketModel,
    ) -> StructuralAlignment:

        if not market.expansions:
            return StructuralAlignment.CONFLICTING

        latest_expansion = market.expansions[-1]
        expansion_direction = latest_expansion.direction

        aligned_events = 0
        counter_events = 0

        for event in market.structure_events:
            if event.direction.value == expansion_direction.value:
                aligned_events += 1
            else:
                counter_events += 1

        if counter_events == 0:
            return StructuralAlignment.ALIGNED

        if counter_events < aligned_events:
            return StructuralAlignment.MIXED

        return StructuralAlignment.CONFLICTING

    def _determine_liquidity_context(
        self,
        market: CanonicalMarketModel,
    ) -> LiquidityContext:

        return LiquidityContext.BALANCED

    def _calculate_confidence(
        self,
        bias: MarketBias,
        strength: TrendStrength,
        alignment: StructuralAlignment,
    ) -> float:

        if bias == MarketBias.NEUTRAL:
            return 0.3

        base = 0.5

        if strength == TrendStrength.STRONG:
            base += 0.2
        elif strength == TrendStrength.MODERATE:
            base += 0.1

        if alignment == StructuralAlignment.ALIGNED:
            base += 0.2
        elif alignment == StructuralAlignment.MIXED:
            base += 0.0
        else:
            base -= 0.1

        return max(0.0, min(1.0, base))