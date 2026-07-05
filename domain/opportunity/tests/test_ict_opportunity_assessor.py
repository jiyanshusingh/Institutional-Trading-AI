from datetime import UTC, datetime

from domain.opportunity.ict_opportunity_assessor import (
    ICTOpportunityAssessor,
)
from domain.opportunity.opportunity import Opportunity
from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)


def make_opportunity(priority: str) -> Opportunity:

    return Opportunity(
        opportunity_id="OPP-001",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        opportunity_type="LONG" if priority != "LOW" else "WAIT",
        direction="LONG" if priority != "LOW" else "NONE",
        priority=priority,

        supporting_thesis_ids=("THESIS-001",),

        evidence_quality="STRONG",
        reasoning_quality="HIGH",

        expected_structural_evolution=(
            "Bullish continuation."
        ),

        assumptions=(
            "Structure remains valid.",
        ),

        invalidation=(
            "Confirmed bearish CHOCH.",
        ),
    )


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    assessor = ICTOpportunityAssessor()

    assert assessor.assessor_name == "ICTOpportunityAssessor"
    assert assessor.theory == "ICT"
    assert assessor.version == "1.0"


# ==========================================================
# Public API
# ==========================================================

def test_assess_returns_tuple():

    assessor = ICTOpportunityAssessor()

    assessments = assessor.assess(
        (make_opportunity("HIGH"),)
    )

    assert isinstance(assessments, tuple)


def test_assess_returns_assessment():

    assessor = ICTOpportunityAssessor()

    assessments = assessor.assess(
        (make_opportunity("HIGH"),)
    )

    assert len(assessments) == 1
    assert isinstance(
        assessments[0],
        OpportunityAssessment,
    )


# ==========================================================
# Assessment Rules
# ==========================================================

def test_high_priority_assessment():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("HIGH"),)
    )[0]

    assert assessment.assessment_level == "HIGH"


def test_medium_priority_assessment():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("MEDIUM"),)
    )[0]

    assert assessment.assessment_level == "MEDIUM"


def test_low_priority_assessment():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("LOW"),)
    )[0]

    assert assessment.assessment_level == "LOW"


# ==========================================================
# Score
# ==========================================================

def test_high_priority_score():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("HIGH"),)
    )[0]

    assert assessment.overall_score == 80


def test_medium_priority_score():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("MEDIUM"),)
    )[0]

    assert assessment.overall_score == 60


def test_low_priority_score():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("LOW"),)
    )[0]

    assert assessment.overall_score == 30


# ==========================================================
# Actionability
# ==========================================================

def test_actionable_propagates():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("HIGH"),)
    )[0]

    assert assessment.actionable


def test_ready_for_ranking():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("HIGH"),)
    )[0]

    assert assessment.ready_for_ranking


def test_wait_not_ready_for_ranking():

    assessor = ICTOpportunityAssessor()

    assessment = assessor.assess(
        (make_opportunity("LOW"),)
    )[0]

    assert not assessment.ready_for_ranking