"""
Professional Equity Momentum — subclass of MomentumStrategy
with wider stops and volume filter from tuning.
"""

from __future__ import annotations

from strategies.momentum_strategy import MomentumStrategy


class ProfessionalMomentumStrategy(MomentumStrategy):
    def __init__(self, min_vol_ratio=None, **kwargs):
        if min_vol_ratio is not None:
            kwargs["vol_mult"] = min_vol_ratio
        super().__init__(**kwargs)

    @property
    def name(self) -> str:
        return "Professional Equity Momentum"
