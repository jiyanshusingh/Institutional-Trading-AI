"""
Execution Planner Contract

Version 1.0

An ExecutionPlanner transforms one or more TradeCandidate
objects into ExecutionPlan objects.

It defines the contract implemented by all concrete
execution planning models.

Examples

- ICTExecutionPlanner
- WyckoffExecutionPlanner
- TrendExecutionPlanner
- MLExecutionPlanner
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.execution.execution_plan import (
    ExecutionPlan,
)
from domain.trade.trade_candidate import (
    TradeCandidate,
)


class ExecutionPlanner(ABC):
    """
    Abstract Execution Planner contract.
    """

    @property
    @abstractmethod
    def planner_name(self) -> str:
        """
        Human-readable planner name.
        """
        ...

    @property
    @abstractmethod
    def theory(self) -> str:
        """
        Theory implemented by this planner.
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Planner version.
        """
        ...

    @abstractmethod
    def plan(
        self,
        trade_candidates: tuple[TradeCandidate, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[ExecutionPlan, ...]:
        """
        Convert Trade Candidates into Execution Plans.

        Parameters
        ----------
        trade_candidates
            Immutable TradeCandidate objects produced
            by a TradeConstructor.

        objectives
            Execution objectives.

        constraints
            Execution constraints.

        Returns
        -------
        tuple[ExecutionPlan, ...]
            Zero or more immutable ExecutionPlan
            objects.
        """
        ...