from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)
from domain.opportunity.opportunity_ranker import (
    OpportunityRanker,
)
from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)


class ICTOpportunityRanker(OpportunityRanker):
    """
    Version 1 ICT Opportunity Ranker.

    Compares Opportunity Assessments and assigns
    deterministic rankings.
    """

    @property
    def ranker_name(self) -> str:
        return "ICTOpportunityRanker"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def rank(
        self,
        assessments: tuple[OpportunityAssessment, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[OpportunityRanking, ...]:

        if not assessments:
            return ()

        ordered = sorted(
            assessments,
            key=lambda assessment: assessment.overall_score,
            reverse=True,
        )

        rankings = []

        for position, assessment in enumerate(
            ordered,
            start=1,
        ):

            rankings.append(
                self._rank_assessment(
                    assessment,
                    position,
                )
            )

        return tuple(rankings)

    # ==========================================================
    # Internal Ranking Logic
    # ==========================================================

    def _rank_assessment(
        self,
        assessment: OpportunityAssessment,
        rank_position: int,
    ) -> OpportunityRanking:

        return OpportunityRanking(
            ranking_id=str(uuid4()),
            created_at=datetime.now(UTC),

            assessment_id=assessment.assessment_id,

            symbol=assessment.symbol,
            timeframe=assessment.timeframe,
            direction=assessment.direction,

            rank_position=rank_position,

            ranking_score=assessment.overall_score,

            priority=self._determine_priority(
                assessment
            ),

            portfolio_eligible=self._is_portfolio_eligible(
                assessment
            ),

            rationale=(
                f"Ranked #{rank_position} "
                f"based on assessment score "
                f"{assessment.overall_score}."
            ),
        )

    # ==========================================================
    # Ranking Rules
    # ==========================================================

    def _determine_priority(
        self,
        assessment: OpportunityAssessment,
    ) -> str:

        if assessment.overall_score >= 80:
            return "HIGH"

        if assessment.overall_score >= 60:
            return "MEDIUM"

        return "LOW"

    def _is_portfolio_eligible(
        self,
        assessment: OpportunityAssessment,
    ) -> bool:

        return (
            assessment.actionable
            and assessment.overall_score >= 60
        )