from datetime import datetime

import pytest
from datetime import datetime, UTC
from domain.thesis.market_thesis import MarketThesis


def build_thesis() -> MarketThesis:
    return MarketThesis(
        thesis_id="THESIS-001",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        reasoning_model="ICTReasoningModel",
        theory="ICT",
        version="1.0",

        market_regime="Trending",
        session="Regular",

        objectives=("Swing Trading",),

        central_claim="Bullish continuation is currently the best-supported explanation.",

        supporting_evidence=(
            "Bullish Expansion",
            "Protected Swing Intact",
            "Bullish FVG",
        ),

        counter_evidence=(
            "Weekly Liquidity Overhead",
        ),

        assumptions=(
            "Higher timeframe remains bullish.",
        ),

        expected_structural_evolution="Continuation toward external liquidity.",

        invalidation=(
            "Confirmed Bearish CHOCH",
        ),

        uncertainty="MODERATE",
    )


def test_market_thesis_creation():

    thesis = build_thesis()

    assert thesis.symbol == "RELIANCE"
    assert thesis.timeframe == "15m"
    assert thesis.reasoning_model == "ICTReasoningModel"


def test_market_thesis_is_frozen():

    thesis = build_thesis()

    with pytest.raises(AttributeError):
        thesis.symbol = "TCS"


def test_market_thesis_is_falsifiable():

    thesis = build_thesis()

    assert thesis.is_falsifiable()


def test_market_thesis_counts_supporting_evidence():

    thesis = build_thesis()

    assert thesis.evidence_count() == 3


def test_market_thesis_counts_counter_evidence():

    thesis = build_thesis()

    assert thesis.counter_evidence_count() == 1


def test_market_thesis_has_counter_evidence():

    thesis = build_thesis()

    assert thesis.has_counter_evidence()


def test_market_thesis_has_assumptions():

    thesis = build_thesis()

    assert thesis.has_assumptions()


def test_market_thesis_summary():

    thesis = build_thesis()

    summary = thesis.summary()

    assert "RELIANCE" in summary
    assert "Bullish continuation" in summary