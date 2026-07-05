from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)
from domain.trade.trade_candidate import (
    TradeCandidate,
)
from domain.trade.trade_constructor import (
    TradeConstructor,
)


class ICTTradeConstructor(TradeConstructor):
    """
    Version 1 ICT Trade Constructor.

    Converts a PortfolioDecision into one or more
    TradeCandidate objects.

    Version 1 intentionally leaves execution-specific
    fields (entry, stop, target) unknown.
    """

    @property
    def constructor_name(self) -> str:
        return "ICTTradeConstructor"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "1.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def construct(
        self,
        portfolio_decision: PortfolioDecision,
        objectives=None,
        constraints=None,
    ) -> tuple[TradeCandidate, ...]:

        trades = []

        for ranking_id, allocation in zip(
            portfolio_decision.selected_ranking_ids,
            portfolio_decision.capital_allocations,
        ):

            trades.append(
                self._construct_trade_candidate(
                    ranking_id,
                    allocation,
                )
            )

        return tuple(trades)

    # ==========================================================
    # Internal Construction
    # ==========================================================

    def _construct_trade_candidate(
        self,
        ranking_id: str,
        capital_allocation: float,
    ) -> TradeCandidate:
        """
        Version 1 uses placeholder values for
        symbol, timeframe and execution fields.

        Future versions will populate these from
        the Opportunity / OpportunityRanking chain.
        """

        return TradeCandidate(
            trade_id=str(uuid4()),
            created_at=datetime.now(UTC),

            # ------------------------------------------
            # Placeholder Instrument Information
            # ------------------------------------------

            symbol="UNKNOWN",
            timeframe="UNKNOWN",

            # ------------------------------------------
            # Trade
            # ------------------------------------------

            direction=self._determine_direction(),

            capital_allocation=capital_allocation,

            position_size=self._calculate_position_size(
                capital_allocation
            ),

            # ------------------------------------------
            # Execution (Version 1 Unknown)
            # ------------------------------------------

            entry_price=None,
            stop_loss=None,
            take_profit=None,
            risk_reward_ratio=None,

            order_type="UNKNOWN",
            validity="UNKNOWN",

            rationale=(
                f"Constructed from Portfolio Ranking "
                f"{ranking_id}."
            ),
        )

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def _determine_direction(self) -> str:
        """
        Version 1 placeholder.

        Future versions will derive the direction
        from the originating Opportunity.
        """

        return "LONG"

    def _calculate_position_size(
        self,
        capital_allocation: float,
    ) -> float:
        """
        Version 1 placeholder.

        Position sizing will later use

        - Account Equity
        - Risk Budget
        - Stop Distance
        - Volatility

        Currently we simply return the allocation.
        """

        return capital_allocation