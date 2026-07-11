"""
Structural Model Registry

Registers and retrieves Structural Models.
"""

from .structural_model import StructuralModel


class StructuralModelRegistry:
    """
    Registry for Structural Models.
    """

    def __init__(self):
        self._models: dict[str, StructuralModel] = {}

    def register(
        self,
        model: StructuralModel,
    ) -> None:
        """
        Register a Structural Model.
        """

        if model.name in self._models:
            raise ValueError(
                f"Structural Model '{model.name}' is already registered."
            )

        self._models[model.name] = model

    def get(
        self,
        name: str,
    ) -> StructuralModel:
        """
        Retrieve a Structural Model by name.
        """

        try:
            return self._models[name]
        except KeyError:
            raise KeyError(
                f"Structural Model '{name}' is not registered."
            )

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a model exists.
        """

        return name in self._models

    def all_models(
        self,
    ) -> list[StructuralModel]:
        """
        Return all registered Structural Models.
        """

        return list(self._models.values())

    def names(
        self,
    ) -> list[str]:
        """
        Return registered model names.
        """

        return sorted(self._models.keys())