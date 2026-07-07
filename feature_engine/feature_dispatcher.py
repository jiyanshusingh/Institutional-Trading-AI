"""
==========================================================
Feature Dispatcher
==========================================================

Purpose
-------
Maps feature names to their implementation functions.

This module contains NO computation.

Responsibilities
----------------
- Register feature implementations
- Dispatch feature requests
- Keep FeatureCalculator independent of
  individual feature modules

==========================================================
"""

from __future__ import annotations

# ==========================================================
# Feature Modules
# ==========================================================

from .features.price import PriceFeatures

# Future modules
# from .features.volume import VolumeFeatures
# from .features.volatility import VolatilityFeatures
# from .features.trend import TrendFeatures
# from .features.structure import StructureFeatures
# from .features.liquidity import LiquidityFeatures


# ==========================================================
# Price Features
# ==========================================================

PRICE_DISPATCHER = {

    "candle_range": PriceFeatures.candle_range,
    "body_size": PriceFeatures.body_size,
    "body_ratio": PriceFeatures.body_ratio,

    "upper_wick": PriceFeatures.upper_wick,
    "lower_wick": PriceFeatures.lower_wick,

    "upper_wick_ratio": PriceFeatures.upper_wick_ratio,
    "lower_wick_ratio": PriceFeatures.lower_wick_ratio,

    "open_position": PriceFeatures.open_position,
    "close_position": PriceFeatures.close_position,

    # -----------------------------
    # New Price Features
    # -----------------------------

    "gap": PriceFeatures.gap,

    "gap_percent": PriceFeatures.gap_percent,

    "median_price": PriceFeatures.median_price,

    "typical_price": PriceFeatures.typical_price,

    "weighted_close": PriceFeatures.weighted_close,

    "hl2": PriceFeatures.hl2,

    "hlc3": PriceFeatures.hlc3,

    "ohlc4": PriceFeatures.ohlc4,

}
# ==========================================================
# Volume Features
# ==========================================================

VOLUME_DISPATCHER = {

    # "relative_volume": VolumeFeatures.relative_volume,

}


# ==========================================================
# Volatility Features
# ==========================================================

VOLATILITY_DISPATCHER = {

    # "atr": VolatilityFeatures.atr,

}


# ==========================================================
# Trend Features
# ==========================================================

TREND_DISPATCHER = {

}


# ==========================================================
# Structure Features
# ==========================================================

STRUCTURE_DISPATCHER = {

}


# ==========================================================
# Liquidity Features
# ==========================================================

LIQUIDITY_DISPATCHER = {

}


# ==========================================================
# Master Dispatcher
# ==========================================================

FEATURE_DISPATCHER = {}

FEATURE_DISPATCHER.update(PRICE_DISPATCHER)

FEATURE_DISPATCHER.update(VOLUME_DISPATCHER)

FEATURE_DISPATCHER.update(VOLATILITY_DISPATCHER)

FEATURE_DISPATCHER.update(TREND_DISPATCHER)

FEATURE_DISPATCHER.update(STRUCTURE_DISPATCHER)

FEATURE_DISPATCHER.update(LIQUIDITY_DISPATCHER)


# ==========================================================
# Helper
# ==========================================================

def get_dispatcher():

    """
    Return the complete dispatcher.
    """

    return FEATURE_DISPATCHER