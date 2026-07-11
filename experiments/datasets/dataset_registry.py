"""
Dataset Registry

Registers and retrieves datasets available to the
experimental framework.
"""

from pathlib import Path

from .dataset import Dataset


class DatasetRegistry:
    """
    Registry for experiment datasets.
    """

    def __init__(self) -> None:
        self._datasets: dict[str, Dataset] = {}

    def register(
        self,
        dataset: Dataset,
    ) -> None:
        """
        Register a dataset.
        """

        if dataset.name in self._datasets:
            raise ValueError(
                f"Dataset '{dataset.name}' is already registered."
            )

        self._datasets[dataset.name] = dataset

    def get(
        self,
        name: str,
    ) -> Dataset:
        """
        Retrieve a dataset.
        """

        try:
            return self._datasets[name]
        except KeyError:
            raise KeyError(
                f"Dataset '{name}' is not registered."
            )

    def exists(
        self,
        name: str,
    ) -> bool:
        return name in self._datasets

    def unregister(
        self,
        name: str,
    ) -> None:
        if name not in self._datasets:
            raise KeyError(
                f"Dataset '{name}' is not registered."
            )

        del self._datasets[name]

    def names(self) -> list[str]:
        return sorted(self._datasets.keys())

    def all_datasets(self) -> list[Dataset]:
        return list(self._datasets.values())

    def clear(self) -> None:
        self._datasets.clear()