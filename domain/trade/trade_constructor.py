"""
Trade Constructor Contract

Version 1.0

A TradeConstructor transforms a PortfolioDecision into one
or more TradeCandidate objects.

It defines the contract implemented by all concrete
trade construction models.

Examples

- ICTTradeConstructor
- WyckoffTradeConstructor
- TrendTradeConstructor
- MLTradeConstructor
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)
from domain.trade.trade_candidate import (
    TradeCandidate,
)


class TradeConstructor(ABC):
    """
    Abstract Trade Constructor contract.
    """

    @property
    @abstractmethod
    def constructor_name(self) -> str:
        """
        Human-readable name of the constructor.
        """
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """
        Theory implemented by this constructor.
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Constructor version.
        """
        ...

    @abstractmethod
    def construct(
        self,
        portfolio_decision: PortfolioDecision,
        market=None,
        objectives=None,
        constraints=None,
    ) -> tuple[TradeCandidate, ...]:
        """
        Construct one or more Trade Candidates from a
        Portfolio Decision.

        Parameters
        ----------
        portfolio_decision
            PortfolioDecision produced by a
            PortfolioAllocator.

        market
            Optional CanonicalMarketModel for price derivation.

        objectives
            Trading objectives.

        constraints
            Trading constraints.

        Returns
        -------
        tuple[TradeCandidate, ...]
            Zero or more immutable TradeCandidate
            objects.
        """
        ...