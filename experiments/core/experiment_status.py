"""
Experiment Status

Defines the lifecycle states of an experiment.
"""

from enum import Enum


class ExperimentStatus(str, Enum):
    """
    Lifecycle states for a research experiment.
    """

    REGISTERED = "REGISTERED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EVALUATED = "EVALUATED"