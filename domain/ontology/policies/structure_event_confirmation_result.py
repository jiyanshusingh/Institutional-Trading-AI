"""
Structure Event Confirmation Result

Theory 1.0

Represents the outcome of attempting to confirm a
StructureEventCandidate.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StructureEventConfirmationResult:

    confirmed: bool

    confirmation_index: int | None = None

    reason: str | None = None

    def __post_init__(self):

        if self.confirmed:

            if self.confirmation_index is None:
                raise ValueError(
                    "Confirmed events require a confirmation index."
                )

        else:

            if self.confirmation_index is not None:
                raise ValueError(
                    "Rejected events cannot have a confirmation index."
                )