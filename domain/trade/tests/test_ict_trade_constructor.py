from datetime import UTC, datetime

from domain.portfolio.portfolio_decision import (
    PortfolioDecision,
)
from domain.trade.ict_trade_constructor import (
    ICTTradeConstructor,
)
from domain.trade.trade_candidate import (
    TradeCandidate,
)


def make_portfolio_decision() -> PortfolioDecision:

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

        rationale="Test portfolio decision.",
    )


# ==========================================================
# Metadata
# ==========================================================

def test_metadata():

    constructor = ICTTradeConstructor()

    assert constructor.constructor_name == "ICTTradeConstructor"
    assert constructor.theory == "ICT"
    assert constructor.version == "2.0"


# ==========================================================
# Public API
# ==========================================================

def test_construct_returns_tuple():

    constructor = ICTTradeConstructor()

    trades = constructor.construct(
        make_portfolio_decision()
    )

    assert isinstance(trades, tuple)


def test_construct_returns_trade_candidates():

    constructor = ICTTradeConstructor()

    trades = constructor.construct(
        make_portfolio_decision()
    )

    assert len(trades) == 3

    assert all(
        isinstance(trade, TradeCandidate)
        for trade in trades
    )


# ==========================================================
# Trade Construction
# ==========================================================

def test_trade_count_matches_allocations():

    constructor = ICTTradeConstructor()

    trades = constructor.construct(
        make_portfolio_decision()
    )

    assert len(trades) == 3


def test_capital_allocations_propagate():

    constructor = ICTTradeConstructor()

    trades = constructor.construct(
        make_portfolio_decision()
    )

    allocations = tuple(
        trade.capital_allocation
        for trade in trades
    )

    assert allocations == (
        40.0,
        35.0,
        25.0,
    )


def test_position_size_placeholder():

    constructor = ICTTradeConstructor()

    trades = constructor.construct(
        make_portfolio_decision()
    )

    assert trades[0].position_size == 40.0
    assert trades[1].position_size == 35.0
    assert trades[2].position_size == 25.0


# ==========================================================
# Trade Construction
# ==========================================================

def test_symbol_from_decision():

    constructor = ICTTradeConstructor()

    trade = constructor.construct(
        make_portfolio_decision()
    )[0]

    assert trade.symbol == "TEST"


def test_timeframe_from_decision():

    constructor = ICTTradeConstructor()

    trade = constructor.construct(
        make_portfolio_decision()
    )[0]

    assert trade.timeframe == "1d"


def test_direction_from_decision():

    constructor = ICTTradeConstructor()

    trade = constructor.construct(
        make_portfolio_decision()
    )[0]

    assert trade.direction == "LONG"


def test_execution_fields_defaults():

    constructor = ICTTradeConstructor()

    trade = constructor.construct(
        make_portfolio_decision()
    )[0]

    assert trade.entry_price is None
    assert trade.stop_loss is None
    assert trade.take_profit is None

    assert trade.order_type == "MARKET"
    assert trade.validity == "DAY"

    assert not trade.is_executable


# ==========================================================
# Empty Portfolio
# ==========================================================

def test_empty_portfolio_returns_empty_tuple():

    constructor = ICTTradeConstructor()

    empty_decision = PortfolioDecision(
        decision_id="EMPTY",
        created_at=datetime.now(UTC),

        selected_ranking_ids=(),

        capital_allocations=(),

        symbols=(),
        timeframes=(),
        directions=(),

        allocation_method="FIXED_WEIGHT",

        total_allocated=0.0,

        cash_reserve=100.0,

        constraints=(),

        rationale="No opportunities.",
    )

    trades = constructor.construct(
        empty_decision
    )

    assert trades == ()
