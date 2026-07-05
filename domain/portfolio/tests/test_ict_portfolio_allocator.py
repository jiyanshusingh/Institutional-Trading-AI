from datetime import UTC, datetime

from domain.opportunity.opportunity_ranking import (
    OpportunityRanking,
)
from domain.portfolio.ict_portfolio_allocator import (
    ICTPortfolioAllocator,
)
from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)


def make_ranking(
    ranking_id: str,
    rank_position: int,
    score: int = 80,
) -> OpportunityRanking:

    return OpportunityRanking(
        ranking_id=ranking_id,
        created_at=datetime.now(UTC),

        assessment_id=f"ASSESSMENT-{ranking_id}",

        rank_position=rank_position,

        ranking_score=score,

        priority="HIGH",

        portfolio_eligible=True,

        rationale="Test ranking.",
    )


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    allocator = ICTPortfolioAllocator()

    assert allocator.allocator_name == "ICTPortfolioAllocator"
    assert allocator.theory == "ICT"
    assert allocator.version == "1.0"


# ==========================================================
# Public API
# ==========================================================

def test_allocate_returns_portfolio_decision():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
        )
    )

    assert isinstance(
        decision,
        PortfolioDecision,
    )


# ==========================================================
# Allocation Rules
# ==========================================================

def test_single_opportunity():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
        )
    )

    assert decision.capital_allocations == (
        100.0,
    )

    assert decision.total_allocated == 100.0
    assert decision.cash_reserve == 0.0


def test_two_opportunities():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
            make_ranking("R2", 2),
        )
    )

    assert decision.capital_allocations == (
        60.0,
        40.0,
    )

    assert decision.total_allocated == 100.0
    assert decision.cash_reserve == 0.0


def test_three_opportunities():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
            make_ranking("R2", 2),
            make_ranking("R3", 3),
        )
    )

    assert decision.capital_allocations == (
        40.0,
        35.0,
        25.0,
    )

    assert decision.total_allocated == 100.0
    assert decision.cash_reserve == 0.0


# ==========================================================
# Ranking Propagation
# ==========================================================

def test_selected_ranking_ids():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
            make_ranking("R2", 2),
            make_ranking("R3", 3),
        )
    )

    assert decision.selected_ranking_ids == (
        "R1",
        "R2",
        "R3",
    )


# ==========================================================
# Empty Portfolio
# ==========================================================

def test_empty_rankings():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(())

    assert decision.selected_ranking_ids == ()
    assert decision.capital_allocations == ()

    assert decision.total_allocated == 0.0
    assert decision.cash_reserve == 100.0


# ==========================================================
# Allocation Method
# ==========================================================

def test_allocation_method():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
        )
    )

    assert decision.allocation_method == "FIXED_WEIGHT"


# ==========================================================
# Opportunity Count
# ==========================================================

def test_opportunity_count():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
            make_ranking("R2", 2),
        )
    )

    assert decision.opportunity_count == 2


# ==========================================================
# Portfolio State
# ==========================================================

def test_fully_invested():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(
        (
            make_ranking("R1", 1),
            make_ranking("R2", 2),
            make_ranking("R3", 3),
        )
    )

    assert decision.is_fully_invested
    assert not decision.has_cash_reserve


def test_empty_portfolio_has_cash():

    allocator = ICTPortfolioAllocator()

    decision = allocator.allocate(())

    assert not decision.is_fully_invested
    assert decision.has_cash_reserve