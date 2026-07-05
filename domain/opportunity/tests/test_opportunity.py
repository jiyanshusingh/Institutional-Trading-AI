from datetime import UTC, datetime

import pytest

from domain.opportunity.opportunity import Opportunity


def make_opportunity():

    return Opportunity(
        opportunity_id="OPP-001",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        opportunity_type="LONG",
        direction="LONG",
        priority="HIGH",

        supporting_thesis_ids=("THESIS-001",),

        evidence_quality="STRONG",
        reasoning_quality="HIGH",

        expected_structural_evolution=(
            "Bullish structural continuation."
        ),

        assumptions=(
            "Current structural context remains valid.",
        ),

        invalidation=(
            "Confirmed bearish CHOCH.",
        ),
    )


def test_opportunity_creation():

    opportunity = make_opportunity()

    assert opportunity.symbol == "RELIANCE"
    assert opportunity.timeframe == "15m"


def test_is_long():

    opportunity = make_opportunity()

    assert opportunity.is_long


def test_is_actionable():

    opportunity = make_opportunity()

    assert opportunity.is_actionable


def test_has_supporting_theses():

    opportunity = make_opportunity()

    assert opportunity.has_supporting_theses


def test_summary():

    opportunity = make_opportunity()

    summary = opportunity.summary

    assert summary["symbol"] == "RELIANCE"
    assert summary["type"] == "LONG"


def test_invalid_opportunity_type():

    with pytest.raises(ValueError):

        Opportunity(
            opportunity_id="1",
            created_at=datetime.now(UTC),

            symbol="RELIANCE",
            timeframe="15m",

            opportunity_type="BUY",
            direction="LONG",
            priority="HIGH",
        )


def test_invalid_priority():

    with pytest.raises(ValueError):

        Opportunity(
            opportunity_id="1",
            created_at=datetime.now(UTC),

            symbol="RELIANCE",
            timeframe="15m",

            opportunity_type="LONG",
            direction="LONG",
            priority="VERY HIGH",
        )


def test_wait_is_not_actionable():

    opportunity = Opportunity(
        opportunity_id="WAIT-1",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        opportunity_type="WAIT",
        direction="NONE",
        priority="LOW",
    )

    assert opportunity.is_wait
    assert not opportunity.is_actionable