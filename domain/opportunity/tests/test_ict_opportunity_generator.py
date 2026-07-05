from datetime import UTC, datetime

from domain.opportunity.ict_opportunity_generator import (
    ICTOpportunityGenerator,
)
from domain.opportunity.opportunity import Opportunity
from domain.thesis.market_thesis import MarketThesis


def make_thesis(
    claim: str,
    uncertainty: str,
) -> MarketThesis:

    return MarketThesis(
        thesis_id="THESIS-001",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        reasoning_model="ICTReasoningModel",
        theory="ICT",
        version="1.0",

        market_regime="Bullish Expansion",
        session="UNKNOWN",

        objectives=(),

        central_claim=claim,

        supporting_evidence=(
            "Bullish Expansion",
            "Bullish BOS",
            "Protected Structure Present",
        ),

        counter_evidence=(),

        assumptions=(
            "Current structural context remains valid.",
        ),

        expected_structural_evolution=(
            "Continuation of current structure."
        ),

        invalidation=(
            "Confirmed opposing CHOCH.",
        ),

        uncertainty=uncertainty,
    )


# ==========================================================
# Metadata
# ==========================================================

def test_generator_metadata():

    generator = ICTOpportunityGenerator()

    assert generator.generator_name == "ICTOpportunityGenerator"
    assert generator.theory == "ICT"
    assert generator.version == "1.0"


# ==========================================================
# Public API
# ==========================================================

def test_generate_returns_tuple():

    generator = ICTOpportunityGenerator()

    opportunities = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )

    assert isinstance(opportunities, tuple)


def test_generate_returns_opportunity():

    generator = ICTOpportunityGenerator()

    opportunities = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )

    assert len(opportunities) == 1
    assert isinstance(opportunities[0], Opportunity)


# ==========================================================
# Decision Rules
# ==========================================================

def test_bullish_strong_generates_long():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )[0]

    assert opportunity.opportunity_type == "LONG"


def test_bearish_strong_generates_short():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bearish continuation",
                "STRONG",
            ),
        )
    )[0]

    assert opportunity.opportunity_type == "SHORT"


def test_moderate_generates_wait():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "MODERATE",
            ),
        )
    )[0]

    assert opportunity.opportunity_type == "WAIT"


def test_weak_generates_wait():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bearish continuation",
                "WEAK",
            ),
        )
    )[0]

    assert opportunity.opportunity_type == "WAIT"


# ==========================================================
# Propagation
# ==========================================================

def test_symbol_propagates():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )[0]

    assert opportunity.symbol == "RELIANCE"


def test_timeframe_propagates():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )[0]

    assert opportunity.timeframe == "15m"


def test_supporting_thesis_id_propagates():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )[0]

    assert opportunity.supporting_thesis_ids == (
        "THESIS-001",
    )


def test_actionable_long():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "STRONG",
            ),
        )
    )[0]

    assert opportunity.is_actionable


def test_wait_not_actionable():

    generator = ICTOpportunityGenerator()

    opportunity = generator.generate(
        (
            make_thesis(
                "Bullish continuation",
                "WEAK",
            ),
        )
    )[0]

    assert opportunity.is_wait
    assert not opportunity.is_actionable