"""
==========================================================
Target Definitions
==========================================================

Purpose
-------
Defines research targets that can be generated directly
from historical OHLCV data.

A TargetDefinition describes WHAT future outcome is to be
measured. It does not compute the target.

Examples
--------
- 5-bar forward return
- 10-bar forward return
- Maximum Favorable Excursion (MFE)
- Maximum Adverse Excursion (MAE)
- Future Volatility

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ==========================================================
# Target Type
# ==========================================================

class TargetType(str, Enum):
    """
    Supported research target types.
    """

    FORWARD_RETURN = "forward_return"

    FORWARD_HIGH = "forward_high"

    FORWARD_LOW = "forward_low"

    MAX_FAVORABLE_EXCURSION = "mfe"

    MAX_ADVERSE_EXCURSION = "mae"

    FUTURE_VOLATILITY = "future_volatility"


# ==========================================================
# Target Definition
# ==========================================================

@dataclass(frozen=True, slots=True)
class TargetDefinition:
    """
    Immutable definition of one research target.
    """

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    name: str

    target_type: TargetType

    # ------------------------------------------------------
    # Parameters
    # ------------------------------------------------------

    horizon: int

    description: str = ""

    # ======================================================
    # Validation
    # ======================================================

    def __post_init__(self) -> None:

        if not self.name.strip():

            raise ValueError(
                "Target name cannot be empty."
            )

        if self.horizon <= 0:

            raise ValueError(
                "Target horizon must be greater than zero."
            )

    # ======================================================
    # Helpers
    # ======================================================

    @property
    def column_name(self) -> str:
        """
        Name of the generated DataFrame column.
        """

        return f"{self.target_type.value}_{self.horizon}"

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self) -> str:

        return (

            "TargetDefinition("

            f"name='{self.name}', "

            f"type='{self.target_type.value}', "

            f"horizon={self.horizon}"

            ")"

        )


# ==========================================================
# Standard Target Library
# ==========================================================

FORWARD_RETURN_5 = TargetDefinition(

    name="Forward Return (5)",

    target_type=TargetType.FORWARD_RETURN,

    horizon=5,

)

FORWARD_RETURN_10 = TargetDefinition(

    name="Forward Return (10)",

    target_type=TargetType.FORWARD_RETURN,

    horizon=10,

)

FORWARD_RETURN_20 = TargetDefinition(

    name="Forward Return (20)",

    target_type=TargetType.FORWARD_RETURN,

    horizon=20,

)

FORWARD_RETURN_50 = TargetDefinition(

    name="Forward Return (50)",

    target_type=TargetType.FORWARD_RETURN,

    horizon=50,

)

MFE_10 = TargetDefinition(

    name="Maximum Favorable Excursion (10)",

    target_type=TargetType.MAX_FAVORABLE_EXCURSION,

    horizon=10,

)

MFE_20 = TargetDefinition(

    name="Maximum Favorable Excursion (20)",

    target_type=TargetType.MAX_FAVORABLE_EXCURSION,

    horizon=20,

)

MAE_10 = TargetDefinition(

    name="Maximum Adverse Excursion (10)",

    target_type=TargetType.MAX_ADVERSE_EXCURSION,

    horizon=10,

)

MAE_20 = TargetDefinition(

    name="Maximum Adverse Excursion (20)",

    target_type=TargetType.MAX_ADVERSE_EXCURSION,

    horizon=20,

)

FUTURE_VOLATILITY_10 = TargetDefinition(

    name="Future Volatility (10)",

    target_type=TargetType.FUTURE_VOLATILITY,

    horizon=10,

)

FUTURE_VOLATILITY_20 = TargetDefinition(

    name="Future Volatility (20)",

    target_type=TargetType.FUTURE_VOLATILITY,

    horizon=20,

)


# ==========================================================
# Registry
# ==========================================================

TARGET_DEFINITIONS: tuple[TargetDefinition, ...] = (

    FORWARD_RETURN_5,

    FORWARD_RETURN_10,

    FORWARD_RETURN_20,

    FORWARD_RETURN_50,

    MFE_10,

    MFE_20,

    MAE_10,

    MAE_20,

    FUTURE_VOLATILITY_10,

    FUTURE_VOLATILITY_20,

)