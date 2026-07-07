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

    "atr": Feature(

        name="Average True Range",

        category=FeatureCategory.VOLATILITY,

        description="Average True Range",

        units="Price",

        deterministic=True,

        status=FeatureStatus.PLANNED,

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