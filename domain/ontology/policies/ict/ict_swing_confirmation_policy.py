"""
ICT Swing Confirmation Policy

Theory 1.0

Determines whether a SwingCandidate becomes
a confirmed Swing.

Version 2

Features:
- Confirmation delay
- Confirmation index

Not yet implemented:
- ATR displacement
- Structural validation
- ICT-specific confirmation rules
"""

from domain.market_observation.observation_history import ObservationHistory

from domain.ontology.candidates.swing_candidate import SwingCandidate

from ..swing_confirmation_policy import SwingConfirmationPolicy
from ..swing_confirmation_result import SwingConfirmationResult


class ICTSwingConfirmationPolicy(
    SwingConfirmationPolicy
):

    def __init__(
        self,
        strength_calculator,
        lookback=3,
    ):

        self._strength_calculator = strength_calculator
        self._lookback = lookback
        
    def confirm(
        self,
        candidate: SwingCandidate,
        observation_history: ObservationHistory,
    ) -> SwingConfirmationResult:

        confirmation_index = (
            candidate.index + self._lookback
        )

        #
        # Not enough future observations
        #

        if confirmation_index >= len(observation_history):

            return SwingConfirmationResult(
                confirmed=False,
                reason="Insufficient future observations.",
            )

        #
        # Candidate confirmed
        #

        return SwingConfirmationResult(
            confirmed=True,
            confirmation_index=confirmation_index,
        )