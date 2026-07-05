"""
Opportunity Assessor Contract

Version 1.0

An OpportunityAssessor evaluates one or more Opportunity
objects and produces standardized OpportunityAssessment
objects.

It defines the contract implemented by all concrete
opportunity assessment models.

Examples

- ICTOpportunityAssessor
- WyckoffOpportunityAssessor
- TrendOpportunityAssessor
- MLOpportunityAssessor
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.opportunity.opportunity import Opportunity
from domain.opportunity.opportunity_assessment import (
    OpportunityAssessment,
)


class OpportunityAssessor(ABC):
    """
    Abstract Opportunity Assessor contract.
    """

    @property
    @abstractmethod
    def assessor_name(self) -> str:
        """
        Human-readable name of the assessor.
        """
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """
        Theory implemented by this assessor.
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Assessor version.
        """
        ...

    @abstractmethod
    def assess(
        self,
        opportunities: tuple[Opportunity, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[OpportunityAssessment, ...]:
        """
        Assess one or more Opportunities.

        Parameters
        ----------
        opportunities
            Opportunity objects produced by an
            OpportunityGenerator.

        objectives
            Explicit investment objectives.

        constraints
            Portfolio or operational constraints.

        Returns
        -------
        tuple[OpportunityAssessment, ...]
            Zero or more immutable OpportunityAssessment
            objects.
        """
        ...