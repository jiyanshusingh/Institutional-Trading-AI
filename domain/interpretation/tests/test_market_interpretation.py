from dataclasses import FrozenInstanceError

import pytest

from domain.interpretation.market_interpretation import (
    LiquidityContext,
    MarketBias,
    MarketInterpretation,
    StructuralAlignment,
    TrendStrength,
)


def create_market_interpretation():

    return MarketInterpretation(
        market_bias=MarketBias.BULLISH,
        trend_strength=TrendStrength.STRONG,
        structural_alignment=StructuralAlignment.ALIGNED,
        liquidity_context=LiquidityContext.BALANCED,
        confidence=0.85,
    )


def test_create_market_interpretation():

    interpretation = create_market_interpretation()

    assert interpretation.market_bias == MarketBias.BULLISH
    assert interpretation.trend_strength == TrendStrength.STRONG
    assert (
        interpretation.structural_alignment
        == StructuralAlignment.ALIGNED
    )
    assert (
        interpretation.liquidity_context
        == LiquidityContext.BALANCED
    )
    assert interpretation.confidence == 0.85


def test_confidence_cannot_be_negative():

    with pytest.raises(ValueError):

        MarketInterpretation(
            market_bias=MarketBias.BULLISH,
            trend_strength=TrendStrength.STRONG,
            structural_alignment=StructuralAlignment.ALIGNED,
            liquidity_context=LiquidityContext.BALANCED,
            confidence=-0.1,
        )


def test_confidence_cannot_exceed_one():

    with pytest.raises(ValueError):

        MarketInterpretation(
            market_bias=MarketBias.BULLISH,
            trend_strength=TrendStrength.STRONG,
            structural_alignment=StructuralAlignment.ALIGNED,
            liquidity_context=LiquidityContext.BALANCED,
            confidence=1.5,
        )


def test_is_bullish():

    interpretation = create_market_interpretation()

    assert interpretation.is_bullish
    assert not interpretation.is_bearish
    assert not interpretation.is_neutral


def test_market_interpretation_is_immutable():

    interpretation = create_market_interpretation()

    with pytest.raises(FrozenInstanceError):
        interpretation.confidence = 0.50