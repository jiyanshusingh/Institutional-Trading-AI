"""
Trade Candidate

Version 1.0

A TradeCandidate represents a fully specified trading
proposal produced from a PortfolioDecision.

It performs no computation.

It is immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class TradeCandidate:
    """
    Immutable Trade Candidate.
    """

    # ----------------------------------------------------------
    # Identity
    # ----------------------------------------------------------

    trade_id: str

    created_at: datetime

    # ----------------------------------------------------------
    # Instrument
    # ----------------------------------------------------------

    symbol: str

    timeframe: str

    # ----------------------------------------------------------
    # Trade
    # ----------------------------------------------------------

    direction: str

    capital_allocation: float

    position_size: float

    # ----------------------------------------------------------
    # Price Specification
    # ----------------------------------------------------------

    entry_price: float | None = None

    stop_loss: float | None = None

    take_profit: float | None = None

    risk_reward_ratio: float | None = None

    # ----------------------------------------------------------
    # Execution
    # ----------------------------------------------------------

    order_type: str = "UNKNOWN"

    validity: str = "UNKNOWN"

    # ----------------------------------------------------------
    # Explanation
    # ----------------------------------------------------------

    rationale: str = ""

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    def __post_init__(self):

        if not self.trade_id:
            raise ValueError(
                "Trade ID cannot be empty."
            )

        if not self.symbol:
            raise ValueError(
                "Symbol cannot be empty."
            )

        if not self.timeframe:
            raise ValueError(
                "Timeframe cannot be empty."
            )

        if self.direction not in (
            "LONG",
            "SHORT",
            "WAIT",
        ):
            raise ValueError(
                "Invalid trade direction."
            )

        if not (
            0.0 <= self.capital_allocation <= 100.0
        ):
            raise ValueError(
                "Capital allocation must be between "
                "0 and 100."
            )

        if self.position_size < 0:
            raise ValueError(
                "Position size cannot be negative."
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
            self.risk_reward_ratio is not None
            and self.risk_reward_ratio < 0
        ):
            raise ValueError(
                "Risk reward ratio cannot be negative."
            )

    # ----------------------------------------------------------
    # Convenience
    # ----------------------------------------------------------

    @property
    def is_long(self) -> bool:
        return self.direction == "LONG"

    @property
    def is_short(self) -> bool:
        return self.direction == "SHORT"

    @property
    def is_wait(self) -> bool:
        return self.direction == "WAIT"

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
    def is_executable(self) -> bool:
        """
        Version 1:

        WAIT trades are never executable.

        LONG and SHORT become executable only when
        entry, stop loss and take profit exist.
        """

        return (
            self.direction != "WAIT"
            and self.entry_price is not None
            and self.stop_loss is not None
            and self.take_profit is not None
        )

    @property
    def summary(self) -> dict:

        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "direction": self.direction,
            "capital_allocation": self.capital_allocation,
            "position_size": self.position_size,
            "order_type": self.order_type,
        }

    def __str__(self) -> str:

        return (
            f"TradeCandidate("
            f"{self.symbol}, "
            f"{self.direction}, "
            f"{self.capital_allocation:.1f}%"
            f")"
        )