from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from domain.opportunity.opportunity import Opportunity
from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)
from domain.opportunity.opportunity_assessor import (
    OpportunityAssessor,
)


class ICTOpportunityAssessor(OpportunityAssessor):
    """
    Version 1 ICT Opportunity Assessor.

    Evaluates Opportunities independently.
    """

    @property
    def assessor_name(self) -> str:
        return "ICTOpportunityAssessor"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def assess(
        self,
        opportunities: tuple[Opportunity, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[OpportunityAssessment, ...]:

        assessments = []

        for opportunity in opportunities:

            assessments.append(
                self._assess_opportunity(
                    opportunity,
                    objectives,
                    constraints,
                )
            )

        return tuple(assessments)

    # ==========================================================
    # Internal Assessment Logic
    # ==========================================================

    def _assess_opportunity(
        self,
        opportunity: Opportunity,
        objectives=None,
        constraints=None,
    ) -> OpportunityAssessment:

        assessment_level = self._determine_assessment_level(
            opportunity
        )

        overall_score = self._calculate_score(
            opportunity
        )

        actionable = opportunity.is_actionable

        objective_alignment = self._check_objective_alignment(
            opportunity,
            objectives,
        )

        constraint_satisfaction = self._check_constraints(
            opportunity,
            constraints,
        )

        return OpportunityAssessment(
            assessment_id=str(uuid4()),
            created_at=datetime.now(UTC),

            opportunity_id=opportunity.opportunity_id,

            symbol=opportunity.symbol,
            timeframe=opportunity.timeframe,
            direction=opportunity.direction,

            assessment_level=assessment_level,

            overall_score=overall_score,

            actionable=actionable,

            objective_alignment=objective_alignment,

            constraint_satisfaction=constraint_satisfaction,

            rationale=(
                f"{assessment_level} quality opportunity "
                f"with score {overall_score}."
            ),
        )

    # ==========================================================
    # Assessment Rules
    # ==========================================================

    def _determine_assessment_level(
        self,
        opportunity: Opportunity,
    ) -> str:

        if opportunity.priority == "HIGH":
            return "HIGH"

        if opportunity.priority == "MEDIUM":
            return "MEDIUM"

        return "LOW"

    def _calculate_score(
        self,
        opportunity: Opportunity,
    ) -> int:

        if opportunity.priority == "HIGH":
            return 80

        if opportunity.priority == "MEDIUM":
            return 60

        return 30

    def _check_objective_alignment(
        self,
        opportunity: Opportunity,
        objectives,
    ) -> bool:
        """
        Version 1 assumes objectives are satisfied.
        """

        return True

    def _check_constraints(
        self,
        opportunity: Opportunity,
        constraints,
    ) -> bool:
        """
        Version 1 assumes constraints are satisfied.
        """

        return True