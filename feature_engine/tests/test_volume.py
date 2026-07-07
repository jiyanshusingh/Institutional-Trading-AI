import unittest

import pandas as pd

from feature_engine.feature_calculator import FeatureCalculator


class TestVolumeFeatures(unittest.TestCase):

    def setUp(self):

        self.calculator = FeatureCalculator()

        self.df = pd.DataFrame(
            {
                "open": [100, 102, 104, 103, 105],
                "high": [105, 106, 108, 107, 110],
                "low": [99, 101, 102, 101, 104],
                "close": [104, 105, 103, 106, 109],
                "volume": [1000, 1200, 900, 1500, 1800],
            }
        )

    # =====================================================
    # Volume
    # =====================================================

    def test_volume(self):

        result = self.calculator.compute(
            self.df,
            ["volume"],
        )

        self.assertIn(
            "volume",
            result.columns,
        )

        self.assertEqual(
            result.loc[0, "volume"],
            1000,
        )

    # =====================================================
    # Volume Change
    # =====================================================

    def test_volume_change(self):

        result = self.calculator.compute(
            self.df,
            ["volume_change"],
        )

        self.assertTrue(
            pd.isna(
                result.loc[0, "volume_change"]
            )
        )

        self.assertEqual(
            result.loc[1, "volume_change"],
            200,
        )

        self.assertEqual(
            result.loc[2, "volume_change"],
            -300,
        )

    # =====================================================
    # Volume Change %
    # =====================================================

    def test_volume_change_percent(self):

        result = self.calculator.compute(
            self.df,
            ["volume_change_percent"],
        )

        expected = 20.0

        self.assertAlmostEqual(
            result.loc[1, "volume_change_percent"],
            expected,
            places=5,
        )

    # =====================================================
    # Volume MA 5
    # =====================================================

    def test_volume_ma_5(self):

        result = self.calculator.compute(
            self.df,
            ["volume_ma_5"],
        )

        expected = (
            1000
            + 1200
            + 900
            + 1500
            + 1800
        ) / 5

        self.assertAlmostEqual(
            result.loc[4, "volume_ma_5"],
            expected,
            places=5,
        )

    # =====================================================
    # Relative Volume 5
    # =====================================================

    def test_relative_volume_5(self):

        result = self.calculator.compute(
            self.df,
            ["relative_volume_5"],
        )

        ma = (
            1000
            + 1200
            + 900
            + 1500
            + 1800
        ) / 5

        expected = 1800 / ma

        self.assertAlmostEqual(
            result.loc[4, "relative_volume_5"],
            expected,
            places=5,
        )

    # =====================================================
    # Cumulative Volume
    # =====================================================

    def test_cumulative_volume(self):

        result = self.calculator.compute(
            self.df,
            ["cumulative_volume"],
        )

        self.assertEqual(
            result.loc[4, "cumulative_volume"],
            6400,
        )


if __name__ == "__main__":

    unittest.main()