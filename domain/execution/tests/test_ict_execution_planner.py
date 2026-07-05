from datetime import UTC, datetime

from domain.execution.execution_plan import (
    ExecutionPlan,
)
from domain.execution.ict_execution_planner import (
    ICTExecutionPlanner,
)
from domain.trade.trade_candidate import (
    TradeCandidate,
)


def make_trade(
    entry_price=None,
    stop_loss=None,
    take_profit=None,
) -> TradeCandidate:

    return TradeCandidate(
        trade_id="TRADE-001",
        created_at=datetime.now(UTC),

        symbol="RELIANCE",
        timeframe="15m",

        direction="LONG",

        capital_allocation=40.0,

        position_size=100.0,

        entry_price=entry_price,
        stop_loss=stop_loss,
        take_profit=take_profit,

        risk_reward_ratio=None,

        order_type="UNKNOWN",

        validity="UNKNOWN",

        rationale="Test Trade Candidate.",
    )


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    planner = ICTExecutionPlanner()

    assert planner.planner_name == "ICTExecutionPlanner"
    assert planner.theory == "ICT"
    assert planner.version == "1.0"


# ==========================================================
# Public API
# ==========================================================

def test_plan_returns_tuple():

    planner = ICTExecutionPlanner()

    plans = planner.plan(
        (
            make_trade(),
        )
    )

    assert isinstance(plans, tuple)


def test_plan_returns_execution_plan():

    planner = ICTExecutionPlanner()

    plans = planner.plan(
        (
            make_trade(),
        )
    )

    assert len(plans) == 1

    assert isinstance(
        plans[0],
        ExecutionPlan,
    )


# ==========================================================
# Execution Method
# ==========================================================

def test_execution_method():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(),
        )
    )[0]

    assert plan.execution_method == "IMMEDIATE"


# ==========================================================
# Order Type
# ==========================================================

def test_market_order_without_entry_price():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(),
        )
    )[0]

    assert plan.order_type == "MARKET"


def test_limit_order_with_entry_price():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(
                entry_price=2500.0,
            ),
        )
    )[0]

    assert plan.order_type == "LIMIT"


# ==========================================================
# Defaults
# ==========================================================

def test_validity():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(),
        )
    )[0]

    assert plan.validity == "DAY"


def test_time_in_force():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(),
        )
    )[0]

    assert plan.time_in_force == "DAY"


def test_partial_fill_allowed():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(),
        )
    )[0]

    assert plan.partial_fill_allowed


def test_maximum_slippage():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(),
        )
    )[0]

    assert plan.maximum_slippage == 0.20


# ==========================================================
# Price Propagation
# ==========================================================

def test_prices_propagate():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(
                entry_price=2500.0,
                stop_loss=2450.0,
                take_profit=2650.0,
            ),
        )
    )[0]

    assert plan.entry_price == 2500.0
    assert plan.stop_loss == 2450.0
    assert plan.take_profit == 2650.0


# ==========================================================
# Ready For Execution
# ==========================================================

def test_ready_for_execution():

    planner = ICTExecutionPlanner()

    plan = planner.plan(
        (
            make_trade(
                entry_price=2500.0,
                stop_loss=2450.0,
                take_profit=2650.0,
            ),
        )
    )[0]

    assert plan.is_ready_for_execution


# ==========================================================
# Empty Input
# ==========================================================

def test_empty_input_returns_empty_tuple():

    planner = ICTExecutionPlanner()

    plans = planner.plan(())

    assert plans == ()