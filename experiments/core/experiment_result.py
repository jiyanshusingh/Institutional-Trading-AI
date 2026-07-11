"""
Experiment Result

Represents the outcome of a completed experiment.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .experiment_status import ExperimentStatus


@dataclass
class ExperimentResult:
    """
    Stores the outcome of a research experiment.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    experiment_id: str

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    status: ExperimentStatus = ExperimentStatus.REGISTERED

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------

    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_seconds: float | None = None

    # ------------------------------------------------------------------
    # Outcome
    # ------------------------------------------------------------------

    success: bool = False

    # ------------------------------------------------------------------
    # Experiment Outputs
    # ------------------------------------------------------------------

    artifacts: dict[str, str] = field(default_factory=dict)

    metrics: dict[str, float] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Error Information
    # ------------------------------------------------------------------

    error_message: str | None = None