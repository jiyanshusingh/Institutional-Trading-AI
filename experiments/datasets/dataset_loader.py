"""
Dataset Loader

Loads a registered dataset into a pandas DataFrame.
"""

from pathlib import Path

import pandas as pd

from .dataset import Dataset


class DatasetLoader:
    """
    Loads datasets for the experimental framework.
    """

    def load(
        self,
        dataset: Dataset,
    ) -> pd.DataFrame:
        """
        Load a dataset.

        Parameters
        ----------
        dataset
            Dataset metadata.

        Returns
        -------
        pd.DataFrame
            Loaded dataset.
        """

        path = Path(dataset.path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {path}"
            )

        dataframe = pd.read_csv(path)

        if dataframe.empty:
            raise ValueError(
                f"Dataset is empty: {path}"
            )

        return dataframe