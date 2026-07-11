"""
Executable Strategy Interface

Defines the uniform interface that all backtestable strategies
must implement, along with shared data types for strategy results.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class TradeCandidate:
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    is_executable: bool = True
    rationale: str = ""
    symbol: str = ""
    timeframe: str = ""
    ranking_score: int = 80


@dataclass
class StrategyResult:
    trade_candidates: list[TradeCandidate] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class ExecutableStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def run(
        self,
        df,
        symbol: str,
        timeframe: str,
        day_type: str = "",
        stock_type: str = "",
        **kwargs,
    ) -> StrategyResult:
        ...
