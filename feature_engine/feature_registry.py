"""
==========================================================
Feature Registry
==========================================================

Purpose
-------
Central registry of every deterministic feature supported
by the Feature Engine.

This module DOES NOT compute features.

It only defines:

- Feature names
- Categories
- Status
- Dependencies
- Metadata

All feature implementations live inside
feature_calculator.py

==========================================================
"""

from dataclasses import dataclass
from enum import Enum


# ==========================================================
# Feature Status
# ==========================================================

class FeatureStatus(Enum):

    PLANNED = "Planned"

    EXPERIMENTAL = "Experimental"

    VALIDATED = "Validated"

    CORE = "Core"

    DEPRECATED = "Deprecated"


# ==========================================================
# Feature Category
# ==========================================================

class FeatureCategory(Enum):

    PRICE = "Price"

    VOLUME = "Volume"

    VOLATILITY = "Volatility"

    TREND = "Trend"
    MOMENTUM = "Momentum"
    STRUCTURE = "Structure"

    LIQUIDITY = "Liquidity"

    MARKET = "Market"

    SECTOR = "Sector"

    INDUSTRY = "Industry"

    RELATIVE_STRENGTH = "Relative Strength"

    TIME = "Time"

    RISK = "Risk"

    EXECUTION = "Execution"

    STATISTICAL = "Statistical"

    MICROSTRUCTURE = "Microstructure"


# ==========================================================
# Feature Metadata
# ==========================================================

@dataclass(frozen=True)
class Feature:

    name: str

    category: FeatureCategory

    description: str

    units: str

    deterministic: bool

    status: FeatureStatus

    dependencies: tuple[str, ...]
# ==========================================================
# Feature Registry
# ==========================================================

FEATURES = {

    # ------------------------------------------------------
    # Price
    # ------------------------------------------------------

    "candle_range": Feature(

        name="Candle Range",

        category=FeatureCategory.PRICE,

        description="High minus Low",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("high", "low"),

    ),

    "body_size": Feature(

        name="Body Size",

        category=FeatureCategory.PRICE,

        description="Absolute candle body",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("open", "close"),

    ),
    "gap": Feature(

        name="Gap",

        category=FeatureCategory.PRICE,

        description="Current Open minus Previous Close",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("open", "close"),

    ),
    "gap_percent": Feature(

        name="Gap Percent",

        category=FeatureCategory.PRICE,

        description="Gap expressed as percentage of previous close",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("gap",),

    ),
    "median_price": Feature(

        name="Median Price",

        category=FeatureCategory.PRICE,

        description="(High + Low) / 2",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("high", "low"),

    ),
    "typical_price": Feature(

        name="Typical Price",

        category=FeatureCategory.PRICE,

        description="(High + Low + Close) / 3",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("high", "low", "close"),

    ),
    "weighted_close": Feature(

        name="Weighted Close",

        category=FeatureCategory.PRICE,

        description="(High + Low + 2 × Close) / 4",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("high", "low", "close"),

    ),
    "hl2": Feature(

        name="HL2",

        category=FeatureCategory.PRICE,

        description="(High + Low) / 2",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("high", "low"),

    ),
    "hlc3": Feature(

        name="HLC3",

        category=FeatureCategory.PRICE,

        description="(High + Low + Close) / 3",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("high", "low", "close"),

    ),
    "ohlc4": Feature(

        name="OHLC4",

        category=FeatureCategory.PRICE,

        description="(Open + High + Low + Close) / 4",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("open", "high", "low", "close"),

    ),

    # ------------------------------------------------------
    # Volume
    # ------------------------------------------------------
    "volume": Feature(
        name="Volume",
        category=FeatureCategory.VOLUME,
        description="Raw traded volume",
        units="Shares",
        deterministic=True,
        status=FeatureStatus.CORE,
        dependencies=("volume",),
    ),

    "volume_change": Feature(
        name="Volume Change",
        category=FeatureCategory.VOLUME,
        description="Difference from previous candle volume",
        units="Shares",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume",),
    ),

    "volume_change_percent": Feature(
        name="Volume Change Percent",
        category=FeatureCategory.VOLUME,
        description="Percentage change from previous volume",
        units="Percent",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume_change","volume",),
    ),

    "volume_ma_5": Feature(
        name="Volume MA 5",
        category=FeatureCategory.VOLUME,
        description="5-period moving average of volume",
        units="Shares",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume",),
    ),

    "volume_ma_10": Feature(
        name="Volume MA 10",
        category=FeatureCategory.VOLUME,
        description="10-period moving average of volume",
        units="Shares",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume",),
    ),

    "volume_ma_20": Feature(
        name="Volume MA 20",
        category=FeatureCategory.VOLUME,
        description="20-period moving average of volume",
        units="Shares",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume",),
    ),

    "relative_volume_5": Feature(
        name="Relative Volume 5",
        category=FeatureCategory.VOLUME,
        description="Current volume divided by 5-period average volume",
        units="Ratio",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume", "volume_ma_5"),
    ),

    "relative_volume_10": Feature(
        name="Relative Volume 10",
        category=FeatureCategory.VOLUME,
        description="Current volume divided by 10-period average volume",
        units="Ratio",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume", "volume_ma_10"),
    ),

    "relative_volume_20": Feature(
        name="Relative Volume 20",
        category=FeatureCategory.VOLUME,
        description="Current volume divided by 20-period average volume",
        units="Ratio",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume", "volume_ma_20"),
    ),

    "cumulative_volume": Feature(
        name="Cumulative Volume",
        category=FeatureCategory.VOLUME,
        description="Running cumulative traded volume",
        units="Shares",
        deterministic=True,
        status=FeatureStatus.PLANNED,
        dependencies=("volume",),
    ),

    # ------------------------------------------------------
    # Volatility
    # ------------------------------------------------------

    "true_range": Feature(

        name="True Range",

        category=FeatureCategory.VOLATILITY,

        description="Maximum of High-Low, High-Previous Close, Low-Previous Close",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("high", "low", "close"),

    ),

    "atr_5": Feature(

        name="ATR 5",

        category=FeatureCategory.VOLATILITY,

        description="5-period Average True Range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("true_range",),

    ),

    "atr_10": Feature(

        name="ATR 10",

        category=FeatureCategory.VOLATILITY,

        description="10-period Average True Range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("true_range",),

    ),

    "atr_14": Feature(

        name="ATR 14",

        category=FeatureCategory.VOLATILITY,

        description="14-period Average True Range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("true_range",),

    ),

    "atr_20": Feature(

        name="ATR 20",

        category=FeatureCategory.VOLATILITY,

        description="20-period Average True Range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("true_range",),

    ),

    "range_ma_5": Feature(

        name="Range MA 5",

        category=FeatureCategory.VOLATILITY,

        description="5-period moving average of candle range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("candle_range",),

    ),

    "range_ma_10": Feature(

        name="Range MA 10",

        category=FeatureCategory.VOLATILITY,

        description="10-period moving average of candle range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("candle_range",),

    ),

    "range_ma_20": Feature(

        name="Range MA 20",

        category=FeatureCategory.VOLATILITY,

        description="20-period moving average of candle range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("candle_range",),

    ),

    "range_expansion": Feature(

        name="Range Expansion",

        category=FeatureCategory.VOLATILITY,

        description="Current candle range relative to 20-period average range",

        units="Ratio",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("candle_range", "range_ma_20"),

    ),

    "range_contraction": Feature(

        name="Range Contraction",

        category=FeatureCategory.VOLATILITY,

        description="20-period average range relative to current candle range",

        units="Ratio",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("candle_range", "range_ma_20"),

    ),
    "atr_percent_5": Feature(

        name="ATR Percent 5",

        category=FeatureCategory.VOLATILITY,

        description="ATR 5 expressed as percentage of Close",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("atr_5", "close"),

    ),

    "atr_percent_10": Feature(

        name="ATR Percent 10",

        category=FeatureCategory.VOLATILITY,

        description="ATR 10 expressed as percentage of Close",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("atr_10", "close"),

    ),

    "atr_percent_14": Feature(

        name="ATR Percent 14",

        category=FeatureCategory.VOLATILITY,

        description="ATR 14 expressed as percentage of Close",

        units="%",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("atr_14", "close"),

    ),

    "atr_percent_20": Feature(

        name="ATR Percent 20",

        category=FeatureCategory.VOLATILITY,

        description="ATR 20 expressed as percentage of Close",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("atr_20", "close"),

    ),
    "std_5": Feature(

        name="Standard Deviation 5",

        category=FeatureCategory.VOLATILITY,

        description="5-period rolling standard deviation of Close",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "std_10": Feature(

        name="Standard Deviation 10",

        category=FeatureCategory.VOLATILITY,

        description="10-period rolling standard deviation of Close",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "std_20": Feature(

        name="Standard Deviation 20",

        category=FeatureCategory.VOLATILITY,

        description="20-period rolling standard deviation of Close",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "variance_5": Feature(

        name="Variance 5",

        category=FeatureCategory.VOLATILITY,

        description="5-period rolling variance of Close",

        units="Price²",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "variance_10": Feature(

        name="Variance 10",

        category=FeatureCategory.VOLATILITY,

        description="10-period rolling variance of Close",

        units="Price²",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "variance_20": Feature(

        name="Variance 20",

        category=FeatureCategory.VOLATILITY,

        description="20-period rolling variance of Close",

        units="Price²",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),
    "atr_ratio": Feature(

        name="ATR Ratio",

        category=FeatureCategory.VOLATILITY,

        description="ATR 14 divided by ATR 20",

        units="Ratio",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("atr_14", "atr_20"),

    ),

    "volatility_expansion": Feature(

        name="Volatility Expansion",

        category=FeatureCategory.VOLATILITY,

        description="ATR 14 increasing compared to previous candle",

        units="Boolean",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("atr_14",),

    ),

    "volatility_compression": Feature(

        name="Volatility Compression",

        category=FeatureCategory.VOLATILITY,

        description="ATR 14 decreasing compared to previous candle",

        units="Boolean",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("atr_14",),

    ),
    "ema_5": Feature(

        name="EMA 5",

        category=FeatureCategory.TREND,

        description="5-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "ema_9": Feature(

        name="EMA 9",

        category=FeatureCategory.TREND,

        description="9-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "ema_10": Feature(

        name="EMA 10",

        category=FeatureCategory.TREND,

        description="10-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "ema_20": Feature(

        name="EMA 20",

        category=FeatureCategory.TREND,

        description="20-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "ema_21": Feature(

        name="EMA 21",

        category=FeatureCategory.TREND,

        description="21-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "ema_34": Feature(

        name="EMA 34",

        category=FeatureCategory.TREND,

        description="34-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "ema_50": Feature(

        name="EMA 50",

        category=FeatureCategory.TREND,

        description="50-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "ema_100": Feature(

        name="EMA 100",

        category=FeatureCategory.TREND,

        description="100-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "ema_200": Feature(

        name="EMA 200",

        category=FeatureCategory.TREND,

        description="200-period Exponential Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),
    "sma_5": Feature(

        name="SMA 5",

        category=FeatureCategory.TREND,

        description="5-period Simple Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "sma_10": Feature(

        name="SMA 10",

        category=FeatureCategory.TREND,

        description="10-period Simple Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "sma_20": Feature(

        name="SMA 20",

        category=FeatureCategory.TREND,

        description="20-period Simple Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "sma_50": Feature(

        name="SMA 50",

        category=FeatureCategory.TREND,

        description="50-period Simple Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "sma_100": Feature(

        name="SMA 100",

        category=FeatureCategory.TREND,

        description="100-period Simple Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "sma_200": Feature(

        name="SMA 200",

        category=FeatureCategory.TREND,

        description="200-period Simple Moving Average",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),
    "distance_from_ema20": Feature(

        name="Distance from EMA 20",

        category=FeatureCategory.TREND,

        description="Close minus EMA 20",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close", "ema_20"),

    ),

    "distance_from_ema50": Feature(

        name="Distance from EMA 50",

        category=FeatureCategory.TREND,

        description="Close minus EMA 50",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close", "ema_50"),

    ),

    "distance_from_ema200": Feature(

        name="Distance from EMA 200",

        category=FeatureCategory.TREND,

        description="Close minus EMA 200",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close", "ema_200"),

    ),

    "distance_from_sma20": Feature(

        name="Distance from SMA 20",

        category=FeatureCategory.TREND,

        description="Close minus SMA 20",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close", "sma_20"),

    ),

    "distance_from_sma50": Feature(

        name="Distance from SMA 50",

        category=FeatureCategory.TREND,

        description="Close minus SMA 50",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close", "sma_50"),

    ),

    "distance_from_sma200": Feature(

        name="Distance from SMA 200",

        category=FeatureCategory.TREND,

        description="Close minus SMA 200",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close", "sma_200"),

    ),

    "ema20_slope": Feature(

        name="EMA20 Slope",

        category=FeatureCategory.TREND,

        description="EMA20 change from previous candle",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("ema_20",),

    ),

    "ema50_slope": Feature(

        name="EMA50 Slope",

        category=FeatureCategory.TREND,

        description="EMA50 change from previous candle",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("ema_50",),

    ),

    "ema200_slope": Feature(

        name="EMA200 Slope",

        category=FeatureCategory.TREND,

        description="EMA200 change from previous candle",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("ema_200",),

    ),
    "rsi_7": Feature(

        name="RSI 7",

        category=FeatureCategory.MOMENTUM,

        description="7-period Relative Strength Index",

        units="Index",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "rsi_14": Feature(

        name="RSI 14",

        category=FeatureCategory.MOMENTUM,

        description="14-period Relative Strength Index",

        units="Index",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "rsi_21": Feature(

        name="RSI 21",

        category=FeatureCategory.MOMENTUM,

        description="21-period Relative Strength Index",

        units="Index",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "roc_5": Feature(

        name="ROC 5",

        category=FeatureCategory.MOMENTUM,

        description="5-period Rate of Change",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "roc_10": Feature(

        name="ROC 10",

        category=FeatureCategory.MOMENTUM,

        description="10-period Rate of Change",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "roc_20": Feature(

        name="ROC 20",

        category=FeatureCategory.MOMENTUM,

        description="20-period Rate of Change",

        units="%",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),
    "momentum_5": Feature(

        name="Momentum 5",

        category=FeatureCategory.MOMENTUM,

        description="5-period Momentum",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "momentum_10": Feature(

        name="Momentum 10",

        category=FeatureCategory.MOMENTUM,

        description="10-period Momentum",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("close",),

    ),

    "momentum_20": Feature(

        name="Momentum 20",

        category=FeatureCategory.MOMENTUM,

        description="20-period Momentum",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "macd": Feature(

        name="MACD",

        category=FeatureCategory.MOMENTUM,

        description="EMA12 - EMA26",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("close",),

    ),

    "macd_signal": Feature(

        name="MACD Signal",

        category=FeatureCategory.MOMENTUM,

        description="9-period EMA of MACD",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("macd",),

    ),

    "macd_histogram": Feature(

        name="MACD Histogram",

        category=FeatureCategory.MOMENTUM,

        description="MACD minus Signal",

        units="Price",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("macd", "macd_signal"),

    ),
    "stochastic_k": Feature(

        name="Stochastic %K",

        category=FeatureCategory.MOMENTUM,

        description="14-period Stochastic Oscillator %K",

        units="Percent",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("high", "low", "close"),

    ),

    "stochastic_d": Feature(

        name="Stochastic %D",

        category=FeatureCategory.MOMENTUM,

        description="3-period moving average of %K",

        units="Percent",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("stochastic_k",),

    ),

    "williams_r": Feature(

        name="Williams %R",

        category=FeatureCategory.MOMENTUM,

        description="14-period Williams Percent Range",

        units="Percent",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("high", "low", "close"),

    ),

    "cci_20": Feature(

        name="CCI 20",

        category=FeatureCategory.MOMENTUM,

        description="20-period Commodity Channel Index",

        units="Index",

        deterministic=True,

        status=FeatureStatus.CORE,

        dependencies=("high", "low", "close"),

    ),

    # ------------------------------------------------------
    # Structure
    # ------------------------------------------------------

    "impulse_size": Feature(

        name="Impulse Size",

        category=FeatureCategory.STRUCTURE,

        description="Percentage movement during impulse",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("Swing Detection",),

    ),

    "pullback_depth": Feature(

        name="Pullback Depth",

        category=FeatureCategory.STRUCTURE,

        description="Percentage retracement",

        units="%",

        deterministic=True,

        status=FeatureStatus.PLANNED,

        dependencies=("Impulse",),

    ),

}


# ==========================================================
# Helper Functions
# ==========================================================

def get_feature(feature_name: str) -> Feature:
    """
    Return metadata for a feature.
    """

    return FEATURES[feature_name]


def list_features():
    """
    Return all registered feature names.
    """

    return sorted(FEATURES.keys())


def features_by_category(category: FeatureCategory):
    """
    Return all features belonging to a category.
    """

    return {

        name: feature

        for name, feature in FEATURES.items()

        if feature.category == category

    }


def features_by_status(status: FeatureStatus):
    """
    Return all features having the given status.
    """

    return {

        name: feature

        for name, feature in FEATURES.items()

        if feature.status == status

    }


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FEATURE REGISTRY")
    print("=" * 60)

    print()

    print(f"Total Features : {len(FEATURES)}")

    print()

    for name in list_features():

        print(name)