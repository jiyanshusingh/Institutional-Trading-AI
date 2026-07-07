from dataclasses import dataclass

from .swing import Swing


@dataclass(frozen=True, slots=True)
class ActiveStructure:
    """
    Canonical representation of the currently
    active structural swings.

    The object stores only established structural
    facts.

    It does not contain any logic explaining why a
    swing is active.
    """

    active_swings: tuple[Swing, ...]

    def __post_init__(self):

        if self.active_swings is None:
            raise ValueError(
                "Active swings cannot be None."
            )

        if not all(
            isinstance(swing, Swing)
            for swing in self.active_swings
        ):
            raise TypeError(
                "All active swings must be Swing instances."
            )

    @property
    def active_highs(self) -> tuple[Swing, ...]:

        return tuple(
            swing
            for swing in self.active_swings
            if swing.is_high
        )

    @property
    def active_lows(self) -> tuple[Swing, ...]:

        return tuple(
            swing
            for swing in self.active_swings
            if swing.is_low
        )

    def __len__(self):

        return len(self.active_swings)

    def __iter__(self):

        return iter(self.active_swings)