"""
Opportunity Generator Contract

Version 1.0

An OpportunityGenerator transforms one or more Market Theses
into standardized Opportunity objects.

It defines the contract implemented by all concrete
opportunity generation models.

Examples

- ICTOpportunityGenerator
- WyckoffOpportunityGenerator
- TrendOpportunityGenerator
- MLOpportunityGenerator
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.opportunity.opportunity import Opportunity
from domain.thesis.market_thesis import MarketThesis


class OpportunityGenerator(ABC):
    """
    Abstract Opportunity Generator contract.
    """

    @property
    @abstractmethod
    def generator_name(self) -> str:
        """
        Human-readable name of the generator.
        """
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """
        Theory implemented by this generator.
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Generator version.
        """
        ...

    @abstractmethod
    def generate(
        self,
        market_theses: tuple[MarketThesis, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[Opportunity, ...]:
        """
        Generate one or more Opportunities from one or more
        Market Theses.

        Parameters
        ----------
        market_theses
            Market Theses produced by a Reasoning Model.

        objectives
            Explicit decision objectives.

        constraints
            Operational or portfolio constraints.

        Returns
        -------
        tuple[Opportunity, ...]
            Zero or more immutable Opportunity objects.
        """
        ...