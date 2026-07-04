"""
Swing Confirmation Policy

Determines whether a SwingCandidate
becomes a confirmed Swing.
"""

from abc import ABC, abstractmethod

from domain.market_observation.observation_history import ObservationHistory
from domain.ontology.candidates.swing_candidate import SwingCandidate
from domain.ontology.policies.swing_confirmation_result import SwingConfirmationResult


class SwingConfirmationPolicy(ABC):

    @abstractmethod
    def confirm(
        self,
        candidate: SwingCandidate,
        observation_history: ObservationHistory,
    ) -> SwingConfirmationResult:
        """
        Return True if the candidate
        should become a confirmed Swing.
        """
        ...