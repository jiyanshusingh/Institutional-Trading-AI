from datetime import UTC, datetime

import pytest

from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)


def make_ranking() -> OpportunityRanking:

    return OpportunityRanking(
        ranking_id="RANK-001",
        created_at=datetime.now(UTC),

        assessment_id="ASSESSMENT-001",

        rank_position=1,

        ranking_score=80,

        priority="HIGH",

        portfolio_eligible=True,

        rationale="Highest ranked opportunity.",
    )


# ==========================================================
# Creation
# ==========================================================

def test_ranking_creation():

    ranking = make_ranking()

    assert ranking.assessment_id == "ASSESSMENT-001"
    assert ranking.rank_position == 1
    assert ranking.ranking_score == 80


# ==========================================================
# Priority
# ==========================================================

def test_is_high_priority():

    ranking = make_ranking()

    assert ranking.is_high_priority


def test_is_not_medium_priority():

    ranking = make_ranking()

    assert not ranking.is_medium_priority


def test_is_not_low_priority():

    ranking = make_ranking()

    assert not ranking.is_low_priority


# ==========================================================
# Rank
# ==========================================================

def test_is_top_ranked():

    ranking = make_ranking()

    assert ranking.is_top_ranked


def test_ready_for_portfolio():

    ranking = make_ranking()

    assert ranking.ready_for_portfolio


# ==========================================================
# Summary
# ==========================================================

def test_summary():

    ranking = make_ranking()

    summary = ranking.summary

    assert summary["rank_position"] == 1
    assert summary["ranking_score"] == 80
    assert summary["priority"] == "HIGH"


# ==========================================================
# Validation
# ==========================================================

def test_invalid_priority():

    with pytest.raises(ValueError):

        OpportunityRanking(
            ranking_id="1",
            created_at=datetime.now(UTC),

            assessment_id="A1",

            rank_position=1,

            ranking_score=80,

            priority="VERY_HIGH",

            portfolio_eligible=True,

            rationale="Invalid priority.",
        )


def test_invalid_rank_position():

    with pytest.raises(ValueError):

        OpportunityRanking(
            ranking_id="1",
            created_at=datetime.now(UTC),

            assessment_id="A1",

            rank_position=0,

            ranking_score=80,

            priority="HIGH",

            portfolio_eligible=True,

            rationale="Invalid rank.",
        )


def test_invalid_score():

    with pytest.raises(ValueError):

        OpportunityRanking(
            ranking_id="1",
            created_at=datetime.now(UTC),

            assessment_id="A1",

            rank_position=1,

            ranking_score=120,

            priority="HIGH",

            portfolio_eligible=True,

            rationale="Invalid score.",
        )


# ==========================================================
# Portfolio Eligibility
# ==========================================================

def test_not_ready_for_portfolio():

    ranking = OpportunityRanking(
        ranking_id="RANK-002",
        created_at=datetime.now(UTC),

        assessment_id="ASSESSMENT-002",

        rank_position=2,

        ranking_score=30,

        priority="LOW",

        portfolio_eligible=False,

        rationale="Low quality opportunity.",
    )

    assert not ranking.ready_for_portfolio
    assert ranking.is_low_priority