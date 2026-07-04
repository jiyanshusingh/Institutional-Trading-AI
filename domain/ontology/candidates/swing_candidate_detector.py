"""
Swing Candidate Detector

Finds possible turning points.

Does NOT confirm them.
"""

from abc import ABC, abstractmethod

from domain.market_observation.observation_history import ObservationHistory

from .swing_candidate import SwingCandidate


class SwingCandidateDetector(ABC):

    @abstractmethod
    def detect(
        self,
        observation_history: ObservationHistory,
    ) -> tuple[SwingCandidate, ...]:
        """
        Detect potential Swing candidates.
        """
        ...