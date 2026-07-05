from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from domain.execution.execution_plan import (
    ExecutionPlan,
)
from domain.execution.execution_planner import (
    ExecutionPlanner,
)
from domain.trade.trade_candidate import (
    TradeCandidate,
)


class ICTExecutionPlanner(ExecutionPlanner):
    """
    Version 1 ICT Execution Planner.

    Converts TradeCandidate objects into
    ExecutionPlan objects.

    Version 1 intentionally uses simple,
    deterministic execution rules.
    """

    @property
    def planner_name(self) -> str:
        return "ICTExecutionPlanner"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def plan(
        self,
        trade_candidates: tuple[TradeCandidate, ...],
        objectives=None,
        constraints=None,
    ) -> tuple[ExecutionPlan, ...]:

        plans = []

        for trade in trade_candidates:

            plans.append(
                self._construct_execution_plan(
                    trade
                )
            )

        return tuple(plans)

    # ==========================================================
    # Internal Construction
    # ==========================================================

    def _construct_execution_plan(
        self,
        trade: TradeCandidate,
    ) -> ExecutionPlan:

        return ExecutionPlan(
            execution_plan_id=str(uuid4()),
            created_at=datetime.now(UTC),

            trade_id=trade.trade_id,

            execution_method=self._determine_execution_method(
                trade
            ),

            order_type=self._determine_order_type(
                trade
            ),

            entry_price=trade.entry_price,

            stop_loss=trade.stop_loss,

            take_profit=trade.take_profit,

            validity=self._determine_validity(
                trade
            ),

            time_in_force=self._determine_time_in_force(
                trade
            ),

            maximum_slippage=self._determine_maximum_slippage(
                trade
            ),

            partial_fill_allowed=self._allow_partial_fill(
                trade
            ),

            rationale=(
                "Execution plan constructed from "
                "Trade Candidate."
            ),
        )

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def _determine_execution_method(
        self,
        trade: TradeCandidate,
    ) -> str:
        """
        Version 1 always executes immediately.
        """

        return "IMMEDIATE"

    def _determine_order_type(
        self,
        trade: TradeCandidate,
    ) -> str:
        """
        Version 1 rule:

        If entry price exists -> LIMIT

        Otherwise -> MARKET
        """

        if trade.entry_price is not None:
            return "LIMIT"

        return "MARKET"

    def _determine_validity(
        self,
        trade: TradeCandidate,
    ) -> str:
        """
        Version 1 uses DAY orders.
        """

        return "DAY"

    def _determine_time_in_force(
        self,
        trade: TradeCandidate,
    ) -> str:
        """
        Version 1 uses DAY validity.
        """

        return "DAY"

    def _determine_maximum_slippage(
        self,
        trade: TradeCandidate,
    ) -> float:
        """
        Version 1 fixed slippage allowance.
        """

        return 0.20

    def _allow_partial_fill(
        self,
        trade: TradeCandidate,
    ) -> bool:
        """
        Version 1 always allows partial fills.
        """

        return True