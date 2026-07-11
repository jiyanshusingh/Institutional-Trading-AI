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
from domain.semantic_construction.canonical_market_model import (
    CanonicalMarketModel,
)


class ICTTradeConstructor(TradeConstructor):
    """
    Version 2 ICT Trade Constructor.

    Converts a PortfolioDecision into one or more
    TradeCandidate objects using actual market data
    from the CanonicalMarketModel to derive entry,
    stop loss, and take profit levels.
    """

    def __init__(
        self,
        stop_loss_multiplier: float = 3.0,
        take_profit_multiplier: float = 4.0,
        atr_period: int = 14,
        min_risk_reward: float = 0.0,
    ):
        self._stop_mult = stop_loss_multiplier
        self._target_mult = take_profit_multiplier
        self._atr_period = atr_period
        self._min_rr = min_risk_reward

    @property
    def constructor_name(self) -> str:
        return "ICTTradeConstructor"

    @property
    def theory(self) -> str:
        return "ICT"

    @property
    def version(self) -> str:
        return "2.0"

    # ==========================================================
    # Public API
    # ==========================================================

    def construct(
        self,
        portfolio_decision: PortfolioDecision,
        market: CanonicalMarketModel | None = None,
        objectives=None,
        constraints=None,
    ) -> tuple[TradeCandidate, ...]:

        trades = []

        for i in range(len(portfolio_decision.selected_ranking_ids)):
            symbol = (
                portfolio_decision.symbols[i]
                if i < len(portfolio_decision.symbols)
                else "UNKNOWN"
            )
            timeframe = (
                portfolio_decision.timeframes[i]
                if i < len(portfolio_decision.timeframes)
                else "UNKNOWN"
            )
            direction = (
                portfolio_decision.directions[i]
                if i < len(portfolio_decision.directions)
                else "LONG"
            )
            allocation = (
                portfolio_decision.capital_allocations[i]
                if i < len(portfolio_decision.capital_allocations)
                else 0.0
            )

            trade = self._construct_trade_candidate(
                ranking_id=portfolio_decision.selected_ranking_ids[i],
                symbol=symbol,
                timeframe=timeframe,
                direction=direction,
                capital_allocation=allocation,
                market=market,
            )

            if trade is not None:
                trades.append(trade)

        return tuple(trades)

    # ==========================================================
    # Internal Construction
    # ==========================================================

    def _construct_trade_candidate(
        self,
        ranking_id: str,
        symbol: str,
        timeframe: str,
        direction: str,
        capital_allocation: float,
        market: CanonicalMarketModel | None = None,
    ) -> TradeCandidate | None:

        entry_price, stop_loss, take_profit = (
            self._derive_price_levels(
                direction,
                market,
            )
        )

        risk_reward = (
            self._calculate_risk_reward(
                entry_price,
                stop_loss,
                take_profit,
            )
        )

        if risk_reward is not None and risk_reward < self._min_rr:
            return None

        order_type = "LIMIT" if entry_price is not None else "MARKET"

        return TradeCandidate(
            trade_id=str(uuid4()),
            created_at=datetime.now(UTC),

            symbol=symbol,
            timeframe=timeframe,
            direction=direction,

            capital_allocation=capital_allocation,

            position_size=self._calculate_position_size(
                capital_allocation
            ),

            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward_ratio=risk_reward,

            order_type=order_type,
            validity="DAY",

            rationale=(
                f"Constructed from Portfolio Ranking "
                f"{ranking_id}. Direction: {direction}, "
                f"Entry: {entry_price}, Stop: {stop_loss}, "
                f"Target: {take_profit}, R:R: {risk_reward}."
            ),
        )

    # ==========================================================
    # Price Derivation
    # ==========================================================

    def _derive_price_levels(
        self,
        direction: str,
        market: CanonicalMarketModel | None,
    ) -> tuple[float | None, float | None, float | None]:
        """
        Derive entry, stop loss, and take profit from
        the CanonicalMarketModel.

        Version 2 uses the last observed price as reference,
        with ATR-based stops and targets.
        """

        if market is None:
            return None, None, None

        observations = market.observation_history
        if len(observations) == 0:
            return None, None, None

        last = observations[-1]

        atr = self._estimate_atr(observations, period=self._atr_period)
        if atr is None or atr == 0.0:
            atr = (last.high - last.low) * 1.5

        if direction == "LONG":
            entry = last.close
            stop = last.close - (atr * self._stop_mult)
            target = last.close + (atr * self._target_mult)
        elif direction == "SHORT":
            entry = last.close
            stop = last.close + (atr * self._stop_mult)
            target = last.close - (atr * self._target_mult)
        else:
            return None, None, None

        return (
            round(entry, 2),
            round(stop, 2),
            round(target, 2),
        )

    def _estimate_atr(self, observations, period: int = 14) -> float | None:
        """Simple ATR estimate from observation history."""
        if len(observations) < period + 1:
            return None

        tr_sum = 0.0
        for i in range(-period, 0):
            curr = observations[i]
            prev = observations[i - 1]
            high_low = curr.high - curr.low
            high_close = abs(curr.high - prev.close)
            low_close = abs(curr.low - prev.close)
            tr = max(high_low, high_close, low_close)
            tr_sum += tr

        return tr_sum / period

    def _calculate_risk_reward(
        self,
        entry: float | None,
        stop: float | None,
        target: float | None,
    ) -> float | None:
        if entry is None or stop is None or target is None:
            return None
        if entry == stop:
            return None
        risk = abs(entry - stop)
        reward = abs(target - entry)
        if risk == 0.0:
            return None
        return round(reward / risk, 2)

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def _determine_direction(self) -> str:
        return "LONG"

    def _calculate_position_size(
        self,
        capital_allocation: float,
    ) -> float:
        return capital_allocation