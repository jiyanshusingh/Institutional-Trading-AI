"""
Structural Model

Base interface for all Structural Models.

A Structural Model is a deterministic hypothesis that converts
market observations into a complete Market Structure representation.
"""

from abc import ABC, abstractmethod

from .market_structure_result import MarketStructureResult


class StructuralModel(ABC):
    """
    Base class for every Structural Model.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable model name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Model version."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description of the model."""
        pass

    @abstractmethod
    def generate_market_structure(
        self,
        observations,
    ) -> MarketStructureResult:
        """
        Generate a complete Market Structure.

        Parameters
        ----------
        observations
            Observation History or market observations.

        Returns
        -------
        MarketStructureResult
        """
        pass