"""
Opportunity Ranker Contract

Version 1.0

An OpportunityRanker compares one or more
OpportunityAssessment objects and produces
standardized OpportunityRanking objects.

It defines the contract implemented by all
concrete opportunity ranking models.

Examples

- ICTOpportunityRanker
- WyckoffOpportunityRanker
- TrendOpportunityRanker
- MLOpportunityRanker
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)
from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)


class OpportunityRanker(ABC):
    """
    Abstract Opportunity Ranker contract.
    """

    @property
    @abstractmethod
    def ranker_name(self) -> str:
        """
        Human-readable name of the ranker.
        """
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """
        Theory implemented by this ranker.
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Ranker version.
        """
        ...

    @abstractmethod
    def rank(
        self,
        assessments: tuple[OpportunityAssessment, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[OpportunityRanking, ...]:
        """
        Rank one or more Opportunity Assessments.

        Parameters
        ----------
        assessments
            OpportunityAssessment objects produced by an
            OpportunityAssessor.

        objectives
            Explicit portfolio objectives.

        constraints
            Portfolio constraints.

        Returns
        -------
        tuple[OpportunityRanking, ...]
            Zero or more immutable OpportunityRanking
            objects ordered by descending attractiveness.
        """
        ...