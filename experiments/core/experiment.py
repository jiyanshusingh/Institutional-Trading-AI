"""
Experiment

Represents one executable research experiment.

The Experiment object does NOT execute anything.
It simply binds together:

    - Experiment Configuration
    - Experiment Result (after execution)

Execution is handled by ExperimentRunner.
"""

from dataclasses import dataclass
from typing import Optional

from .experiment_config import ExperimentConfig
from .experiment_result import ExperimentResult


@dataclass
class Experiment:
    """
    Represents a single research experiment.
    """

    config: ExperimentConfig
    result: Optional[ExperimentResult] = None

    @property
    def experiment_id(self) -> str:
        return self.config.experiment_id

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def structural_model(self) -> str:
        return self.config.structural_model

    @property
    def dataset(self) -> str:
        return self.config.dataset

    @property
    def target(self) -> str:
        return self.config.target

    @property
    def completed(self) -> bool:
        return self.result is not None

    def attach_result(self, result: ExperimentResult) -> None:
        """
        Attach the execution result to this experiment.
        """
        self.result = result