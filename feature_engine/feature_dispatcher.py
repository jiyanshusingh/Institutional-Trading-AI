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
from .features.volume import VolumeFeatures
from .features.volatility import VolatilityFeatures
from .features.trend import TrendFeatures
from .features.momentum import MomentumFeatures


# ==========================================================
# Price Features
# ==========================================================

PRICE_DISPATCHER = {

    # Base
    "candle_range": PriceFeatures.candle_range,
    "body_size": PriceFeatures.body_size,

    # Anatomy
    "body_ratio": PriceFeatures.body_ratio,
    "upper_wick": PriceFeatures.upper_wick,
    "lower_wick": PriceFeatures.lower_wick,
    "upper_wick_ratio": PriceFeatures.upper_wick_ratio,
    "lower_wick_ratio": PriceFeatures.lower_wick_ratio,
    "open_position": PriceFeatures.open_position,
    "close_position": PriceFeatures.close_position,

    # Price Relationships
    "gap": PriceFeatures.gap,
    "gap_percent": PriceFeatures.gap_percent,

    # Price Averages
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

    "volume": VolumeFeatures.volume,

    "volume_change": VolumeFeatures.volume_change,
    "volume_change_percent": VolumeFeatures.volume_change_percent,

    "volume_ma_5": VolumeFeatures.volume_ma_5,
    "volume_ma_10": VolumeFeatures.volume_ma_10,
    "volume_ma_20": VolumeFeatures.volume_ma_20,

    "relative_volume_5": VolumeFeatures.relative_volume_5,
    "relative_volume_10": VolumeFeatures.relative_volume_10,
    "relative_volume_20": VolumeFeatures.relative_volume_20,

    "cumulative_volume": VolumeFeatures.cumulative_volume,
}


# ==========================================================
# Volatility Features
# ==========================================================

VOLATILITY_DISPATCHER = {

    "true_range": VolatilityFeatures.true_range,

    "atr_5": VolatilityFeatures.atr_5,
    "atr_10": VolatilityFeatures.atr_10,
    "atr_14": VolatilityFeatures.atr_14,
    "atr_20": VolatilityFeatures.atr_20,

    "range_ma_5": VolatilityFeatures.range_ma_5,
    "range_ma_10": VolatilityFeatures.range_ma_10,
    "range_ma_20": VolatilityFeatures.range_ma_20,

    "range_expansion": VolatilityFeatures.range_expansion,
    "range_contraction": VolatilityFeatures.range_contraction,
    "atr_percent_5": VolatilityFeatures.atr_percent_5,
    "atr_percent_10": VolatilityFeatures.atr_percent_10,
    "atr_percent_14": VolatilityFeatures.atr_percent_14,
    "atr_percent_20": VolatilityFeatures.atr_percent_20,
    
    "std_5": VolatilityFeatures.std_5,
    "std_10": VolatilityFeatures.std_10,
    "std_20": VolatilityFeatures.std_20,
    "variance_5": VolatilityFeatures.variance_5,
    "variance_10": VolatilityFeatures.variance_10,
    "variance_20": VolatilityFeatures.variance_20,
    
    "atr_ratio": VolatilityFeatures.atr_ratio,
    "volatility_expansion": VolatilityFeatures.volatility_expansion,
    "volatility_compression": VolatilityFeatures.volatility_compression,
}


# ==========================================================
# Future Modules
# ==========================================================

TREND_DISPATCHER = {

    "ema_5": TrendFeatures.ema_5,
    "ema_9": TrendFeatures.ema_9,
    "ema_10": TrendFeatures.ema_10,
    "ema_20": TrendFeatures.ema_20,
    "ema_21": TrendFeatures.ema_21,
    "ema_34": TrendFeatures.ema_34,
    "ema_50": TrendFeatures.ema_50,
    "ema_100": TrendFeatures.ema_100,
    "ema_200": TrendFeatures.ema_200,
    "sma_5": TrendFeatures.sma_5,
    "sma_10": TrendFeatures.sma_10,
    "sma_20": TrendFeatures.sma_20,
    "sma_50": TrendFeatures.sma_50,
    "sma_100": TrendFeatures.sma_100,
    "sma_200": TrendFeatures.sma_200,
    "distance_from_ema20": TrendFeatures.distance_from_ema20,
    "distance_from_ema50": TrendFeatures.distance_from_ema50,
    "distance_from_ema200": TrendFeatures.distance_from_ema200,
    "distance_from_sma20": TrendFeatures.distance_from_sma20,
    "distance_from_sma50": TrendFeatures.distance_from_sma50,
    "distance_from_sma200": TrendFeatures.distance_from_sma200,
    "ema20_slope": TrendFeatures.ema20_slope,
    "ema50_slope": TrendFeatures.ema50_slope,
    "ema200_slope": TrendFeatures.ema200_slope,

}

MOMENTUM_DISPATCHER = {
    "rsi_7": MomentumFeatures.rsi_7,
    "rsi_14": MomentumFeatures.rsi_14,
    "rsi_21": MomentumFeatures.rsi_21,
    "roc_5": MomentumFeatures.roc_5,
    "roc_10": MomentumFeatures.roc_10,
    "roc_20": MomentumFeatures.roc_20,
    "momentum_5": MomentumFeatures.momentum_5,
    "momentum_10": MomentumFeatures.momentum_10,
    "momentum_20": MomentumFeatures.momentum_20,
    "macd": MomentumFeatures.macd,
    "macd_signal": MomentumFeatures.macd_signal,
    "macd_histogram": MomentumFeatures.macd_histogram,
    "stochastic_k": MomentumFeatures.stochastic_k,
    "stochastic_d": MomentumFeatures.stochastic_d,
    "williams_r": MomentumFeatures.williams_r,
    "cci_20": MomentumFeatures.cci_20,
}

STRUCTURE_DISPATCHER = {}

LIQUIDITY_DISPATCHER = {}

MARKET_DISPATCHER = {}

SECTOR_DISPATCHER = {}

STATISTICAL_DISPATCHER = {}

EXECUTION_DISPATCHER = {}


# ==========================================================
# Master Dispatcher
# ==========================================================

FEATURE_DISPATCHER = {

    **PRICE_DISPATCHER,

    **VOLUME_DISPATCHER,

    **VOLATILITY_DISPATCHER,

    **TREND_DISPATCHER,

    **MOMENTUM_DISPATCHER,

    **STRUCTURE_DISPATCHER,

    **LIQUIDITY_DISPATCHER,

    **MARKET_DISPATCHER,

    **SECTOR_DISPATCHER,

    **STATISTICAL_DISPATCHER,

    **EXECUTION_DISPATCHER,

}


# ==========================================================
# Helper Functions
# ==========================================================

def get_dispatcher():
    """
    Return complete dispatcher.
    """
    return FEATURE_DISPATCHER


def has_feature(feature: str) -> bool:
    """
    Check whether a feature is registered.
    """
    return feature in FEATURE_DISPATCHER


def list_dispatchable_features() -> list[str]:
    """
    Return all dispatchable features.
    """
    return sorted(FEATURE_DISPATCHER.keys())


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FEATURE DISPATCHER")
    print("=" * 60)

    print()

    print(
        f"Dispatchable Features : "
        f"{len(FEATURE_DISPATCHER)}"
    )

    print()

    for feature in sorted(FEATURE_DISPATCHER):

        print(feature)