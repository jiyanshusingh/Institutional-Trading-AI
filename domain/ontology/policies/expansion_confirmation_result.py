"""
Expansion Confirmation Result

Represents the outcome of attempting to confirm
an ExpansionCandidate.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExpansionConfirmationResult:

    confirmed: bool

    confirmation_index: int | None = None

    reason: str | None = None

    def __post_init__(self):

        if self.confirmed:

            if self.confirmation_index is None:
                raise ValueError(
                    "Confirmed results require a confirmation index."
                )

        else:

            if self.confirmation_index is not None:
                raise ValueError(
                    "Rejected results cannot have a confirmation index."
                )