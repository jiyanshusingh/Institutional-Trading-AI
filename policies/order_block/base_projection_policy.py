from abc import ABC, abstractmethod

from architecture.selection.candidate import Candidate


class ProjectionPolicy(ABC):

    @abstractmethod
    def select(
        self,
        candidates: tuple[Candidate, ...]
    ) -> Candidate:
        """
        Select one projection candidate.

        Must be deterministic.

        Must never modify candidates.

        Must return exactly one candidate
        or raise an explicit error.
        """
        pass