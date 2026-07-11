"""
==========================================================
Outcome Builder
==========================================================

Purpose
-------
Assigns a research outcome to a ResearchSample.

Responsibilities
----------------
- Evaluate one OutcomeDefinition
- Label one ResearchSample

Does NOT
---------
- Compute features
- Detect market structure
- Run statistical tests
- Build datasets

==========================================================
"""

from __future__ import annotations

import pandas as pd

from research.sample import ResearchSample
from research.outcome_definitions import (
    OutcomeDefinition,
    EvaluationMetric,
)


class OutcomeBuilder:
    """
    Labels ResearchSample objects.
    """

    @staticmethod
    def build(
        sample: ResearchSample,
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> ResearchSample:
        """
        Assign outcome to a ResearchSample.

        Parameters
        ----------
        sample
            Sample to label.

        future_df
            Future candles beginning immediately after
            the event candle.

        definition
            OutcomeDefinition to evaluate.
        """

        outcome = OutcomeBuilder.evaluate(
            sample=sample,
            future_df=future_df,
            definition=definition,
        )

        sample.set_outcome(outcome)

        return sample

    # ======================================================
    # Evaluation
    # ======================================================

    @staticmethod
    def evaluate(
        sample: ResearchSample,
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> str:
        """
        Evaluate one OutcomeDefinition.

        Returns
        -------
        Outcome name if successful,
        otherwise "<outcome>_failure".
        """

        future_df = future_df.head(
            definition.max_bars
        )

        success = False

        # --------------------------------------------------
        # ATR Target
        # --------------------------------------------------

        if definition.success_metric == EvaluationMetric.ATR:

            success = OutcomeBuilder._evaluate_atr(
                sample,
                future_df,
                definition,
            )

        # --------------------------------------------------
        # Price Target
        # --------------------------------------------------

        elif definition.success_metric == EvaluationMetric.PRICE:

            success = OutcomeBuilder._evaluate_price(
                sample,
                future_df,
                definition,
            )

        # --------------------------------------------------
        # Percent Target
        # --------------------------------------------------

        elif definition.success_metric == EvaluationMetric.PERCENT:

            success = OutcomeBuilder._evaluate_percent(
                sample,
                future_df,
                definition,
            )

        # --------------------------------------------------
        # Candle Target
        # --------------------------------------------------

        elif definition.success_metric == EvaluationMetric.CANDLES:

            success = OutcomeBuilder._evaluate_candles(
                future_df,
                definition,
            )

        # --------------------------------------------------
        # Swing Target
        # --------------------------------------------------

        elif definition.success_metric == EvaluationMetric.SWING:

            success = OutcomeBuilder._evaluate_swing(
                sample,
                future_df,
                definition,
            )

        # --------------------------------------------------

        if success:

            return definition.outcome

        return f"{definition.outcome}_failure"

    # ======================================================
    # ATR
    # ======================================================

    @staticmethod
    def _evaluate_atr(
        sample: ResearchSample,
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> bool:

        if not sample.has_feature("atr_14"):
            return False

        if future_df.empty:
            return False

        atr = sample.get_feature("atr_14")

        entry = sample.get_metadata("price")

        direction = sample.get_metadata("direction")

        if (
            atr is None
            or entry is None
            or direction is None
        ):
            return False

        target = atr * definition.success_value

        if direction.lower() == "bullish":

            mfe = future_df["high"].max() - entry

            return mfe >= target

        mfe = entry - future_df["low"].min()

        return mfe >= target

    # ======================================================
    # Price
    # ======================================================

    @staticmethod
    def _evaluate_price(
        sample: ResearchSample,
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> bool:

        if future_df.empty:
            return False

        entry = sample.get_metadata("price")

        direction = sample.get_metadata("direction")

        if (
            entry is None
            or direction is None
        ):
            return False

        if direction.lower() == "bullish":

            return (
                future_df["high"].max()
                >= entry + definition.success_value
            )

        return (
            future_df["low"].min()
            <= entry - definition.success_value
        )

    # ======================================================
    # Percent
    # ======================================================

    @staticmethod
    def _evaluate_percent(
        sample: ResearchSample,
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> bool:

        if future_df.empty:
            return False

        entry = sample.get_metadata("price")

        direction = sample.get_metadata("direction")

        if (
            entry is None
            or direction is None
        ):
            return False

        target = (
            entry
            * definition.success_value
            / 100
        )

        if direction.lower() == "bullish":

            return (
                future_df["high"].max()
                >= entry + target
            )

        return (
            future_df["low"].min()
            <= entry - target
        )

    # ======================================================
    # Candle
    # ======================================================

    @staticmethod
    def _evaluate_candles(
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> bool:

        return (
            len(future_df)
            >= definition.success_value
        )

    # ======================================================
    # Swing
    # ======================================================

    @staticmethod
    def _evaluate_swing(
        sample: ResearchSample,
        future_df: pd.DataFrame,
        definition: OutcomeDefinition,
    ) -> bool:
        """
        Placeholder.

        This will later query the
        Market Structure Engine.
        """

        return False