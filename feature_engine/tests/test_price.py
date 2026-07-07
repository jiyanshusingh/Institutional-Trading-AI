"""
==========================================================
Price Feature Tests
==========================================================

Purpose
-------
Unit tests for deterministic price features.

Every feature should produce identical output
for identical input.

==========================================================
"""

import unittest

import pandas as pd

from feature_engine.feature_calculator import FeatureCalculator


class TestPriceFeatures(unittest.TestCase):

    def setUp(self):
        """
        Create sample OHLC data.
        """

        self.df = pd.DataFrame({

            "open": [100, 110],

            "high": [110, 120],

            "low": [95, 105],

            "close": [105, 115],

            "volume": [1000, 1500],

        })

        self.calculator = FeatureCalculator()

    # ======================================================
    # Candle Range
    # ======================================================

    def test_candle_range(self):

        result = self.calculator.compute(
            self.df,
            ["candle_range"],
        )

        expected = [15, 15]

        self.assertEqual(
            result["candle_range"].tolist(),
            expected,
        )

    # ======================================================
    # Body Size
    # ======================================================

    def test_body_size(self):

        result = self.calculator.compute(
            self.df,
            ["body_size"],
        )

        expected = [5, 5]

        self.assertEqual(
            result["body_size"].tolist(),
            expected,
        )

    # ======================================================
    # Body Ratio
    # ======================================================

    def test_body_ratio(self):

        result = self.calculator.compute(
            self.df,
            ["body_ratio"],
        )

        expected = [
            5 / 15,
            5 / 15,
        ]

        for actual, exp in zip(
            result["body_ratio"],
            expected,
        ):
            self.assertAlmostEqual(
                actual,
                exp,
                places=6,
            )

    # ======================================================
    # Gap
    # ======================================================

    def test_gap(self):

        result = self.calculator.compute(
            self.df,
            ["gap"],
        )

        expected = [
            None,
            5,
        ]

        self.assertTrue(
            pd.isna(result["gap"].iloc[0])
        )

        self.assertEqual(
            result["gap"].iloc[1],
            expected[1],
        )

    # ======================================================
    # HL2
    # ======================================================

    def test_hl2(self):

        result = self.calculator.compute(
            self.df,
            ["hl2"],
        )

        expected = [
            (110 + 95) / 2,
            (120 + 105) / 2,
        ]

        for actual, exp in zip(
            result["hl2"],
            expected,
        ):
            self.assertAlmostEqual(
                actual,
                exp,
                places=6,
            )

    # ======================================================
    # HLC3
    # ======================================================

    def test_hlc3(self):

        result = self.calculator.compute(
            self.df,
            ["hlc3"],
        )

        expected = [
            (110 + 95 + 105) / 3,
            (120 + 105 + 115) / 3,
        ]

        for actual, exp in zip(
            result["hlc3"],
            expected,
        ):
            self.assertAlmostEqual(
                actual,
                exp,
                places=6,
            )

    # ======================================================
    # OHLC4
    # ======================================================

    def test_ohlc4(self):

        result = self.calculator.compute(
            self.df,
            ["ohlc4"],
        )

        expected = [
            (100 + 110 + 95 + 105) / 4,
            (110 + 120 + 105 + 115) / 4,
        ]

        for actual, exp in zip(
            result["ohlc4"],
            expected,
        ):
            self.assertAlmostEqual(
                actual,
                exp,
                places=6,
            )

    # ======================================================
    # Typical Price
    # ======================================================

    def test_typical_price(self):

        result = self.calculator.compute(
            self.df,
            ["typical_price"],
        )

        expected = [
            (110 + 95 + 105) / 3,
            (120 + 105 + 115) / 3,
        ]

        for actual, exp in zip(
            result["typical_price"],
            expected,
        ):
            self.assertAlmostEqual(
                actual,
                exp,
                places=6,
            )

    # ======================================================
    # Weighted Close
    # ======================================================

    def test_weighted_close(self):

        result = self.calculator.compute(
            self.df,
            ["weighted_close"],
        )

        expected = [
            (110 + 95 + 2 * 105) / 4,
            (120 + 105 + 2 * 115) / 4,
        ]

        for actual, exp in zip(
            result["weighted_close"],
            expected,
        ):
            self.assertAlmostEqual(
                actual,
                exp,
                places=6,
            )


if __name__ == "__main__":

    unittest.main()