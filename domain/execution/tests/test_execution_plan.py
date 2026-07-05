from datetime import UTC, datetime

import pytest

from domain.execution.execution_plan import ExecutionPlan


def make_execution_plan() -> ExecutionPlan:

    return ExecutionPlan(
        execution_plan_id="PLAN-001",
        created_at=datetime.now(UTC),

        trade_id="TRADE-001",

        execution_method="IMMEDIATE",

        order_type="MARKET",

        entry_price=None,
        stop_loss=None,
        take_profit=None,

        validity="DAY",

        time_in_force="DAY",

        maximum_slippage=None,

        partial_fill_allowed=True,

        rationale="Test execution plan.",
    )


# ==========================================================
# Creation
# ==========================================================

def test_execution_plan_creation():

    plan = make_execution_plan()

    assert plan.trade_id == "TRADE-001"
    assert plan.execution_method == "IMMEDIATE"
    assert plan.order_type == "MARKET"


# ==========================================================
# Order Type
# ==========================================================

def test_is_market_order():

    plan = make_execution_plan()

    assert plan.is_market_order


def test_not_limit_order():

    plan = make_execution_plan()

    assert not plan.is_limit_order


def test_not_stop_order():

    plan = make_execution_plan()

    assert not plan.is_stop_order


# ==========================================================
# Prices
# ==========================================================

def test_has_no_entry_price():

    plan = make_execution_plan()

    assert not plan.has_entry_price


def test_has_no_stop_loss():

    plan = make_execution_plan()

    assert not plan.has_stop_loss


def test_has_no_take_profit():

    plan = make_execution_plan()

    assert not plan.has_take_profit


def test_not_ready_for_execution():

    plan = make_execution_plan()

    assert not plan.is_ready_for_execution


# ==========================================================
# Summary
# ==========================================================

def test_summary():

    plan = make_execution_plan()

    summary = plan.summary

    assert summary["execution_method"] == "IMMEDIATE"
    assert summary["order_type"] == "MARKET"
    assert summary["validity"] == "DAY"
    assert summary["time_in_force"] == "DAY"


# ==========================================================
# Validation
# ==========================================================

def test_invalid_execution_method():

    with pytest.raises(ValueError):

        ExecutionPlan(
            execution_plan_id="1",
            created_at=datetime.now(UTC),

            trade_id="TRADE",

            execution_method="FAST",

            order_type="MARKET",
        )


def test_invalid_order_type():

    with pytest.raises(ValueError):

        ExecutionPlan(
            execution_plan_id="1",
            created_at=datetime.now(UTC),

            trade_id="TRADE",

            execution_method="IMMEDIATE",

            order_type="BUY",
        )


def test_invalid_validity():

    with pytest.raises(ValueError):

        ExecutionPlan(
            execution_plan_id="1",
            created_at=datetime.now(UTC),

            trade_id="TRADE",

            execution_method="IMMEDIATE",

            order_type="MARKET",

            validity="MONTH",
        )


def test_negative_slippage():

    with pytest.raises(ValueError):

        ExecutionPlan(
            execution_plan_id="1",
            created_at=datetime.now(UTC),

            trade_id="TRADE",

            execution_method="IMMEDIATE",

            order_type="MARKET",

            maximum_slippage=-0.5,
        )


# ==========================================================
# Ready For Execution
# ==========================================================

def test_execution_plan_ready():

    plan = ExecutionPlan(
        execution_plan_id="PLAN-002",
        created_at=datetime.now(UTC),

        trade_id="TRADE-002",

        execution_method="IMMEDIATE",

        order_type="LIMIT",

        entry_price=2500.0,
        stop_loss=2450.0,
        take_profit=2650.0,

        validity="DAY",

        time_in_force="DAY",

        maximum_slippage=0.2,

        partial_fill_allowed=True,

        rationale="Ready for execution.",
    )

    assert plan.has_entry_price
    assert plan.has_stop_loss
    assert plan.has_take_profit

    assert plan.has_complete_execution_prices
    assert plan.is_ready_for_execution