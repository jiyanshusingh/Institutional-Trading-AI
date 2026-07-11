"""
==========================================================
Research Experiment
==========================================================

Purpose
-------
Represents one complete research experiment.

A ResearchExperiment defines

- Hypothesis
- Outcome
- Dataset
- Features
- Statistical Results

It orchestrates the research pipeline but performs
no statistical computations itself.

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from research.dataset import ResearchDataset
from research.hypothesis_registry import Hypothesis
from research.outcome_definitions import OutcomeDefinition
from research.statistics.statistical_result import (
    StatisticalResult,
)
from research.statistics.statistical_tests import (
    StatisticalTests,
)


# ==========================================================
# Research Experiment
# ==========================================================

@dataclass
class ResearchExperiment:
    """
    Represents one research experiment.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    experiment_id: str

    name: str

    description: str

    # ------------------------------------------------------
    # Research Definition
    # ------------------------------------------------------

    hypothesis: Hypothesis

    outcome_definition: OutcomeDefinition

    # ------------------------------------------------------
    # Dataset
    # ------------------------------------------------------

    dataset: ResearchDataset

    # ------------------------------------------------------
    # Features To Evaluate
    # ------------------------------------------------------

    features: list[str]

    target: str

    # ------------------------------------------------------
    # Results
    # ------------------------------------------------------

    results: list[StatisticalResult] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    # ======================================================
    # Public API
    # ======================================================

    def run(self) -> None:
        """
        Execute the experiment.
        """

        df = self.dataset.to_dataframe()

        self.results.clear()

        for feature in self.features:

            feature_results = StatisticalTests.evaluate_feature(

                df=df,

                feature=feature,

                target=self.target,

            )

            for result in feature_results.values():

                if isinstance(
                    result,
                    StatisticalResult,
                ):

                    self.results.append(result)

    # ======================================================
    # Helpers
    # ======================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    def successful_results(
        self,
    ) -> list[StatisticalResult]:

        return [

            result

            for result in self.results

            if result.is_significant()

        ]

    def failed_results(
        self,
    ) -> list[StatisticalResult]:

        return [

            result

            for result in self.results

            if not result.is_significant()

        ]

    # ======================================================
    # Export
    # ======================================================

    def summary(self) -> dict:

        return {

            "experiment_id": self.experiment_id,

            "name": self.name,

            "hypothesis": self.hypothesis.name,

            "dataset_size": len(self.dataset),

            "features": self.features,

            "target": self.target,

            "tests_run": len(self.results),

            "significant": len(

                self.successful_results()

            ),

            "created_at": self.created_at,

        }

    def __repr__(self) -> str:

        return (

            f"ResearchExperiment("

            f"id={self.experiment_id}, "

            f"name={self.name}, "

            f"features={len(self.features)}, "

            f"results={len(self.results)}"

            f")"

        )