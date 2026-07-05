"""
Execution Plan

Version 1.0

An ExecutionPlan represents the execution strategy for a
TradeCandidate.

It performs no computation.

It is immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    """
    Immutable Execution Plan.
    """

    # ----------------------------------------------------------
    # Identity
    # ----------------------------------------------------------

    execution_plan_id: str

    created_at: datetime

    trade_id: str

    # ----------------------------------------------------------
    # Execution
    # ----------------------------------------------------------

    execution_method: str

    order_type: str

    # ----------------------------------------------------------
    # Prices
    # ----------------------------------------------------------

    entry_price: float | None = None

    stop_loss: float | None = None

    take_profit: float | None = None

    # ----------------------------------------------------------
    # Order Properties
    # ----------------------------------------------------------

    validity: str = "UNKNOWN"

    time_in_force: str = "UNKNOWN"

    # ----------------------------------------------------------
    # Risk Controls
    # ----------------------------------------------------------

    maximum_slippage: float | None = None

    partial_fill_allowed: bool = True

    # ----------------------------------------------------------
    # Explanation
    # ----------------------------------------------------------

    rationale: str = ""

    # ==========================================================
    # Validation
    # ==========================================================

    def __post_init__(self):

        if not self.execution_plan_id:
            raise ValueError(
                "Execution Plan ID cannot be empty."
            )

        if not self.trade_id:
            raise ValueError(
                "Trade ID cannot be empty."
            )

        if self.execution_method not in (
            "IMMEDIATE",
            "UNKNOWN",
        ):
            raise ValueError(
                "Invalid execution method."
            )

        if self.order_type not in (
            "MARKET",
            "LIMIT",
            "STOP",
            "UNKNOWN",
        ):
            raise ValueError(
                "Invalid order type."
            )

        if self.validity not in (
            "DAY",
            "GTC",
            "UNKNOWN",
        ):
            raise ValueError(
                "Invalid validity."
            )

        if (
            self.entry_price is not None
            and self.entry_price <= 0
        ):
            raise ValueError(
                "Entry price must be positive."
            )

        if (
            self.stop_loss is not None
            and self.stop_loss <= 0
        ):
            raise ValueError(
                "Stop loss must be positive."
            )

        if (
            self.take_profit is not None
            and self.take_profit <= 0
        ):
            raise ValueError(
                "Take profit must be positive."
            )

        if (
            self.maximum_slippage is not None
            and self.maximum_slippage < 0
        ):
            raise ValueError(
                "Maximum slippage cannot be negative."
            )

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def is_market_order(self) -> bool:
        return self.order_type == "MARKET"

    @property
    def is_limit_order(self) -> bool:
        return self.order_type == "LIMIT"

    @property
    def is_stop_order(self) -> bool:
        return self.order_type == "STOP"

    @property
    def has_entry_price(self) -> bool:
        return self.entry_price is not None

    @property
    def has_stop_loss(self) -> bool:
        return self.stop_loss is not None

    @property
    def has_take_profit(self) -> bool:
        return self.take_profit is not None

    @property
    def has_complete_execution_prices(self) -> bool:
        return (
            self.entry_price is not None
            and self.stop_loss is not None
            and self.take_profit is not None
        )

    @property
    def is_ready_for_execution(self) -> bool:
        """
        Version 1 readiness.

        Execution requires

        • execution method
        • order type
        • entry
        • stop
        • target
        """

        return (
            self.execution_method != "UNKNOWN"
            and self.order_type != "UNKNOWN"
            and self.has_complete_execution_prices
        )

    @property
    def summary(self) -> dict:

        return {
            "execution_method": self.execution_method,
            "order_type": self.order_type,
            "validity": self.validity,
            "time_in_force": self.time_in_force,
            "partial_fill_allowed": self.partial_fill_allowed,
        }

    def __str__(self) -> str:

        return (
            f"ExecutionPlan("
            f"order_type={self.order_type}, "
            f"method={self.execution_method})"
        )