from abc import ABC, abstractmethod


class StructuralRule(ABC):

    @abstractmethod
    def evaluate(self, configuration):
        pass