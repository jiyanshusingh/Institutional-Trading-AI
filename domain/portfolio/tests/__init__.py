"""
Portfolio Allocator Contract

Version 1.0

A PortfolioAllocator transforms one or more
OpportunityRanking objects into a PortfolioDecision.

It defines the contract implemented by all concrete
portfolio allocation models.

Examples

- ICTPortfolioAllocator
- WyckoffPortfolioAllocator
- TrendPortfolioAllocator
- MLPortfolioAllocator
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)
from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)


class PortfolioAllocator(ABC):
    """
    Abstract Portfolio Allocator contract.
    """

    @property
    @abstractmethod
    def allocator_name(self) -> str:
        """
        Human-readable name of the allocator.
        """
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """
        Theory implemented by this allocator.
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Allocator version.
        """
        ...

    @abstractmethod
    def allocate(
        self,
        rankings: tuple[OpportunityRanking, ...],
        available_capital: float = 100.0,
        objectives=None,
        constraints=None,
    ) -> PortfolioDecision:
        """
        Allocate available capital across ranked opportunities.

        Parameters
        ----------
        rankings
            Ranked opportunities produced by an
            OpportunityRanker.

        available_capital
            Total capital available for allocation.
            Version 1 assumes 100%.

        objectives
            Portfolio objectives.

        constraints
            Portfolio constraints.

        Returns
        -------
        PortfolioDecision
            Immutable portfolio allocation decision.
        """
        ...