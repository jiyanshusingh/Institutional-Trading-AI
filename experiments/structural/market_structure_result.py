"""
Market Structure Result

Represents the complete output produced by a Structural Model.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MarketStructureResult:
    """
    Output produced by a Structural Model.
    """

    structural_model: str

    # Primary market structure objects
    swings: list[Any] = field(default_factory=list)
    protected_swings: list[Any] = field(default_factory=list)
    structure_events: list[Any] = field(default_factory=list)
    expansions: list[Any] = field(default_factory=list)

    # Optional derived data
    statistics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)