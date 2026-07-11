from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)
from domain.portfolio.portfolio_allocator import (
    PortfolioAllocator,
)
from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)


class ICTPortfolioAllocator(PortfolioAllocator):
    """
    Version 2 ICT Portfolio Allocator.

    Produces a deterministic PortfolioDecision from one
    or more Opportunity Rankings.

    Allocation Rules

    1 Opportunity
        100%

    2 Opportunities
        60%
        40%

    3+ Opportunities
        40%
        35%
        25%

    Remaining opportunities receive 0%.
    """

    @property
    def allocator_name(self) -> str:
        return "ICTPortfolioAllocator"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "2.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def allocate(
        self,
        rankings: tuple[OpportunityRanking, ...],
        available_capital: float = 100.0,
        objectives=None,
        constraints=None,
    ) -> PortfolioDecision:

        eligible = [
            r for r in rankings if r.portfolio_eligible
        ]

        if not eligible:

            return PortfolioDecision(
                decision_id=str(uuid4()),
                created_at=datetime.now(UTC),

                selected_ranking_ids=(),

                capital_allocations=(),

                symbols=(),
                timeframes=(),
                directions=(),

                allocation_method="FIXED_WEIGHT",

                total_allocated=0.0,

                cash_reserve=available_capital,

                constraints=tuple(constraints or ()),

                rationale="No eligible opportunities.",
            )

        allocations = self._determine_allocations(
            len(eligible)
        )

        selected_ids = []
        capital_allocations = []
        symbols = []
        timeframes = []
        directions = []

        for ranking, allocation in zip(
            eligible,
            allocations,
        ):
            selected_ids.append(
                ranking.ranking_id
            )
            capital_allocations.append(
                allocation
            )
            symbols.append(ranking.symbol)
            timeframes.append(ranking.timeframe)
            directions.append(ranking.direction)

        total_allocated = sum(
            capital_allocations
        )

        cash_reserve = (
            available_capital
            - total_allocated
        )

        return PortfolioDecision(
            decision_id=str(uuid4()),
            created_at=datetime.now(UTC),

            selected_ranking_ids=tuple(
                selected_ids
            ),

            capital_allocations=tuple(
                capital_allocations
            ),

            symbols=tuple(symbols),
            timeframes=tuple(timeframes),
            directions=tuple(directions),

            allocation_method="FIXED_WEIGHT",

            total_allocated=total_allocated,

            cash_reserve=cash_reserve,

            constraints=tuple(
                constraints or ()
            ),

            rationale=(
                "Capital allocated according to "
                "deterministic ICT allocation rules."
            ),
        )

    # ==========================================================
    # Allocation Rules
    # ==========================================================

    def _determine_allocations(
        self,
        count: int,
    ) -> tuple[float, ...]:

        if count <= 0:
            return ()

        if count == 1:
            return (100.0,)

        if count == 2:
            return (
                60.0,
                40.0,
            )

        return (
            40.0,
            35.0,
            25.0,
        )