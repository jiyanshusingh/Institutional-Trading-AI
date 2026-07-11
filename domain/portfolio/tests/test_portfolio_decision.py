from datetime import UTC, datetime

import pytest

from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)


def make_decision() -> PortfolioDecision:

    return PortfolioDecision(
        decision_id="DECISION-001",
        created_at=datetime.now(UTC),

        selected_ranking_ids=(
            "RANK-001",
            "RANK-002",
            "RANK-003",
        ),

        capital_allocations=(
            40.0,
            35.0,
            25.0,
        ),

        symbols=("TEST", "TEST", "TEST"),
        timeframes=("1d", "1d", "1d"),
        directions=("LONG", "LONG", "LONG"),

        allocation_method="FIXED_WEIGHT",

        total_allocated=100.0,

        cash_reserve=0.0,

        constraints=(),

        rationale="Allocate capital according to ranking.",
    )


# ==========================================================
# Creation
# ==========================================================

def test_decision_creation():

    decision = make_decision()

    assert decision.opportunity_count == 3
    assert decision.total_allocated == 100.0
    assert decision.cash_reserve == 0.0


# ==========================================================
# Convenience Properties
# ==========================================================

def test_is_fully_invested():

    decision = make_decision()

    assert decision.is_fully_invested


def test_has_no_cash_reserve():

    decision = make_decision()

    assert not decision.has_cash_reserve


def test_average_allocation():

    decision = make_decision()

    assert decision.average_allocation == (
        100.0 / 3.0
    )


# ==========================================================
# Summary
# ==========================================================

def test_summary():

    decision = make_decision()

    summary = decision.summary

    assert summary["opportunities"] == 3
    assert summary["allocation_method"] == "FIXED_WEIGHT"
    assert summary["total_allocated"] == 100.0
    assert summary["cash_reserve"] == 0.0


# ==========================================================
# Validation
# ==========================================================

def make_single_decision(
    ranking_ids=("R1",),
    allocations=(100.0,),
    total=100.0,
    cash=0.0,
):
    return PortfolioDecision(
        decision_id="1",
        created_at=datetime.now(UTC),
        selected_ranking_ids=ranking_ids,
        capital_allocations=allocations,
        symbols=("TEST",) * len(ranking_ids),
        timeframes=("1d",) * len(ranking_ids),
        directions=("LONG",) * len(ranking_ids),
        allocation_method="FIXED_WEIGHT",
        total_allocated=total,
        cash_reserve=cash,
        constraints=(),
        rationale="Test.",
    )


def test_invalid_lengths():

    with pytest.raises(ValueError):
        make_single_decision(
            ranking_ids=("R1", "R2"),
            allocations=(100.0,),
            total=100.0,
            cash=0.0,
        )


def test_negative_cash_reserve():

    with pytest.raises(ValueError):

        make_single_decision(
            cash=-1.0,
        )


def test_total_not_100_percent():

    with pytest.raises(ValueError):

        make_single_decision(
            allocations=(50.0,),
            total=50.0,
            cash=40.0,
        )


def test_negative_allocation():

    with pytest.raises(ValueError):

        make_single_decision(
            allocations=(-10.0,),
            total=-10.0,
            cash=110.0,
        )


# ==========================================================
# Cash Reserve
# ==========================================================

def test_cash_reserve():

    decision = PortfolioDecision(
        decision_id="DECISION-002",
        created_at=datetime.now(UTC),

        selected_ranking_ids=("RANK-001",),

        capital_allocations=(80.0,),

        symbols=("TEST",),
        timeframes=("1d",),
        directions=("LONG",),

        allocation_method="FIXED_WEIGHT",

        total_allocated=80.0,

        cash_reserve=20.0,

        constraints=(),

        rationale="Keep 20% cash.",
    )

    assert decision.has_cash_reserve
    assert not decision.is_fully_invested
    assert decision.cash_reserve == 20.0