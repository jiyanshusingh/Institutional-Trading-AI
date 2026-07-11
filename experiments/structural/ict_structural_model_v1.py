"""
ICT Structural Model V1

Baseline Structural Model used by the experimental framework.

This class adapts the existing ICT Market Structure Engine to the
StructuralModel interface.
"""

from pandas import DataFrame

from research.experiments.structural.market_structure_result import (
    MarketStructureResult,
)
from research.experiments.structural.structural_model import StructuralModel


class ICTStructuralModelV1(StructuralModel):
    """
    Baseline ICT Structural Model.

    This model wraps the existing market structure implementation
    already present in the project.
    """

    @property
    def name(self) -> str:
        return "ICTStructuralModelV1"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return (
            "Baseline deterministic ICT structural model "
            "used for structural research."
        )

    def generate_market_structure(
        self,
        observations: DataFrame,
    ) -> MarketStructureResult:
        """
        Generate market structure from observations.

        Parameters
        ----------
        observations
            Historical OHLCV dataframe.

        Returns
        -------
        MarketStructureResult
        """

        # -------------------------------------------------------------
        # TODO:
        # Replace this section by calling your existing market
        # structure engine.
        #
        # Example:
        #
        # engine = MarketStructureEngine()
        # structure = engine.build(observations)
        #
        # -------------------------------------------------------------

        structure = None

        return MarketStructureResult(
            structural_model=self.name,
            swings=getattr(structure, "swings", []),
            protected_swings=getattr(
                structure,
                "protected_swings",
                [],
            ),
            structure_events=getattr(
                structure,
                "structure_events",
                [],
            ),
            expansions=getattr(
                structure,
                "expansions",
                [],
            ),
            statistics={},
            metadata={
                "version": self.version,
                "rows": len(observations),
            },
        )