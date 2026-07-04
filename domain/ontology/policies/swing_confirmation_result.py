"""
Swing Confirmation Result

Represents the outcome of applying a Swing
Confirmation Policy to a Swing Candidate.

This is a construction artifact.

It is NOT part of the ontology.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SwingConfirmationResult:

    confirmed: bool

    confirmation_index: int | None = None

    reason: str | None = None

    def __post_init__(self):

        if not self.confirmed:

            if self.confirmation_index is not None:
                raise ValueError(
                    "Rejected candidates cannot have a confirmation index."
                )

        else:

            if self.confirmation_index is None:
                raise ValueError(
                    "Confirmed candidates require a confirmation index."
                )