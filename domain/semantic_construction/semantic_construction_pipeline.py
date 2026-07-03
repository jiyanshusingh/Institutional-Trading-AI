"""
Semantic Construction Pipeline

Document 3 — Computational Model

The SemanticConstructionPipeline is responsible for constructing the
CanonicalMarketModel from an ObservationHistory.

It performs semantic construction only.

It does NOT perform:

- market evaluation
- trading decisions
- execution
- machine learning
"""

from domain.market_observation.observation_history import ObservationHistory

from .canonical_market_model import CanonicalMarketModel


class SemanticConstructionPipeline:
    """
    Builds the canonical semantic interpretation of an ObservationHistory.
    """

    def build(
        self,
        observation_history: ObservationHistory,
    ) -> CanonicalMarketModel:
        """
        Build the CanonicalMarketModel.

        Current Version:
            Skeleton implementation.

        Future Versions:
            - Swing construction
            - Structure Events
            - Expansions
            - Origin Regions
            - Fair Value Gaps
            - Order Blocks
        """

        return CanonicalMarketModel(
            observation_history=observation_history,
        )