from datetime import UTC, datetime

from domain.opportunity.ict_opportunity_ranker import (
    ICTOpportunityRanker,
)
from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)
from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)


def make_assessment(
    assessment_id: str,
    score: int,
    level: str,
    actionable: bool = True,
) -> OpportunityAssessment:

    return OpportunityAssessment(
        assessment_id=assessment_id,
        created_at=datetime.now(UTC),

        opportunity_id=f"OPP-{assessment_id}",

        assessment_level=level,

        overall_score=score,

        actionable=actionable,

        objective_alignment=True,

        constraint_satisfaction=True,

        rationale="Test assessment.",
    )


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    ranker = ICTOpportunityRanker()

    assert ranker.ranker_name == "ICTOpportunityRanker"
    assert ranker.theory == "ICT"
    assert ranker.version == "1.0"


# ==========================================================
# Public API
# ==========================================================

def test_rank_returns_tuple():

    ranker = ICTOpportunityRanker()

    rankings = ranker.rank(
        (
            make_assessment(
                "A1",
                80,
                "HIGH",
            ),
        )
    )

    assert isinstance(rankings, tuple)


def test_rank_returns_ranking():

    ranker = ICTOpportunityRanker()

    rankings = ranker.rank(
        (
            make_assessment(
                "A1",
                80,
                "HIGH",
            ),
        )
    )

    assert len(rankings) == 1
    assert isinstance(
        rankings[0],
        OpportunityRanking,
    )


# ==========================================================
# Ranking Order
# ==========================================================

def test_highest_score_ranked_first():

    ranker = ICTOpportunityRanker()

    rankings = ranker.rank(
        (
            make_assessment(
                "LOW",
                30,
                "LOW",
            ),
            make_assessment(
                "HIGH",
                80,
                "HIGH",
            ),
            make_assessment(
                "MEDIUM",
                60,
                "MEDIUM",
            ),
        )
    )

    assert rankings[0].assessment_id == "HIGH"
    assert rankings[0].rank_position == 1


def test_second_rank():

    ranker = ICTOpportunityRanker()

    rankings = ranker.rank(
        (
            make_assessment(
                "A",
                80,
                "HIGH",
            ),
            make_assessment(
                "B",
                60,
                "MEDIUM",
            ),
        )
    )

    assert rankings[1].rank_position == 2


def test_third_rank():

    ranker = ICTOpportunityRanker()

    rankings = ranker.rank(
        (
            make_assessment(
                "A",
                80,
                "HIGH",
            ),
            make_assessment(
                "B",
                60,
                "MEDIUM",
            ),
            make_assessment(
                "C",
                30,
                "LOW",
            ),
        )
    )

    assert rankings[2].rank_position == 3


# ==========================================================
# Priority
# ==========================================================

def test_high_score_priority():

    ranker = ICTOpportunityRanker()

    ranking = ranker.rank(
        (
            make_assessment(
                "A",
                80,
                "HIGH",
            ),
        )
    )[0]

    assert ranking.priority == "HIGH"


def test_medium_score_priority():

    ranker = ICTOpportunityRanker()

    ranking = ranker.rank(
        (
            make_assessment(
                "A",
                60,
                "MEDIUM",
            ),
        )
    )[0]

    assert ranking.priority == "MEDIUM"


def test_low_score_priority():

    ranker = ICTOpportunityRanker()

    ranking = ranker.rank(
        (
            make_assessment(
                "A",
                30,
                "LOW",
            ),
        )
    )[0]

    assert ranking.priority == "LOW"


# ==========================================================
# Portfolio Eligibility
# ==========================================================

def test_actionable_is_portfolio_eligible():

    ranker = ICTOpportunityRanker()

    ranking = ranker.rank(
        (
            make_assessment(
                "A",
                80,
                "HIGH",
                actionable=True,
            ),
        )
    )[0]

    assert ranking.portfolio_eligible


def test_non_actionable_not_portfolio_eligible():

    ranker = ICTOpportunityRanker()

    ranking = ranker.rank(
        (
            make_assessment(
                "A",
                80,
                "HIGH",
                actionable=False,
            ),
        )
    )[0]

    assert not ranking.portfolio_eligible


# ==========================================================
# Empty Input
# ==========================================================

def test_empty_input_returns_empty_tuple():

    ranker = ICTOpportunityRanker()

    rankings = ranker.rank(())

    assert rankings == ()