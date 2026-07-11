"""
Shared capital model for the Institutional Probability strategy.

Single source of truth for account size, per-trade risk, daily entry cap, and
position sizing. Used by BOTH the backtest engine and the paper trader so the
risk model can never silently diverge between simulation and live trading.
"""

from __future__ import annotations

INITIAL_CAPITAL = 50000.0    # ₹ account size
RISK_PER_TRADE_PCT = 1.0     # % of capital risked per trade → ₹500 on ₹50k
MAX_TRADES_PER_DAY = 5       # cap concurrent-day new entries (quality over quantity)


def position_size_for(entry: float, sl: float) -> float:
    """Notional position value for a capital-based fixed-% risk trade.

    Risk budget = INITIAL_CAPITAL * RISK_PER_TRADE_PCT / 100 (e.g. ₹500 on
    ₹50k @ 1%). Shares = int(risk_budget / risk_per_share). Returns the
    notional (shares * entry). Returns 0.0 when the trade is infeasible on the
    account (risk_per_share too wide to afford even 1 share, or the 1-share
    notional exceeds available capital).
    """
    risk_per_share = abs(entry - sl)
    if risk_per_share <= 0 or entry <= 0:
        return 0.0
    risk_budget = INITIAL_CAPITAL * (RISK_PER_TRADE_PCT / 100.0)
    shares = int(risk_budget / risk_per_share)
    if shares < 1:
        return 0.0
    notional = shares * entry
    # Cannot deploy more than the account holds (no leverage assumed).
    if notional > INITIAL_CAPITAL:
        shares = int(INITIAL_CAPITAL / entry)
        if shares < 1:
            return 0.0
        notional = shares * entry
    return notional
