from abc import ABC, abstractmethod


class CandidateGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        *args,
        **kwargs
    ):
        """
        Generate the complete set of eligible candidates.
        """
        pass