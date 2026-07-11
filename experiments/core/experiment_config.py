"""
Experiment Configuration

Defines everything required to execute a single experiment.

This object is immutable and represents the experiment specification.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    """
    Configuration for a single experiment.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    experiment_id: str
    name: str
    description: str

    # ------------------------------------------------------------------
    # Experiment Components
    # ------------------------------------------------------------------

    dataset: str
    structural_model: str
    target: str

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    evaluation_metrics: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    output_directory: str = "research/experiments/storage/results"

    # ------------------------------------------------------------------
    # Optional Parameters
    # ------------------------------------------------------------------

    parameters: dict[str, Any] = field(default_factory=dict)