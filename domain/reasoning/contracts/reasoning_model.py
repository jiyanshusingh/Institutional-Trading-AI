from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from domain.thesis.market_thesis import MarketThesis


class ReasoningModel(ABC):
    """
    Abstract base class for all reasoning models.

    A Reasoning Model transforms an objective Canonical Market Model
    into one or more explainable Market Theses.

    Examples:

    - ICT
    - Wyckoff
    - Trend Following
    - Mean Reversion
    - Machine Learning
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Human-readable model name."""
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """Underlying market theory."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Model version."""
        ...

    @abstractmethod
    def construct_market_theses(
        self,
        market,
        objectives=None,
        constraints=None,
    ) -> Tuple[MarketThesis, ...]:
        """
        Construct one or more Market Theses from the Canonical Market Model.
        """
        ...