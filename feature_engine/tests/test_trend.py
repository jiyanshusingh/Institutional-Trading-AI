import unittest
import pandas as pd

from feature_engine.feature_calculator import FeatureCalculator


class TestTrendFeatures(unittest.TestCase):

    def setUp(self):

        self.calculator = FeatureCalculator()

        self.df = pd.DataFrame({

            "open": range(1, 301),

            "high": [x + 1 for x in range(1, 301)],

            "low": [x - 1 for x in range(1, 301)],

            "close": range(1, 301),

            "volume": [1000] * 300,

        })

    def test_ema_5(self):

        result = self.calculator.compute(
            self.df,
            ["ema_5"],
        )

        self.assertIn("ema_5", result.columns)


    def test_ema_9(self):

        result = self.calculator.compute(
            self.df,
            ["ema_9"],
        )

        self.assertIn("ema_9", result.columns)


    def test_ema_10(self):

        result = self.calculator.compute(
            self.df,
            ["ema_10"],
        )

        self.assertIn("ema_10", result.columns)


    def test_ema_20(self):

        result = self.calculator.compute(
            self.df,
            ["ema_20"],
        )

        self.assertIn("ema_20", result.columns)


    def test_ema_21(self):

        result = self.calculator.compute(
            self.df,
            ["ema_21"],
        )

        self.assertIn("ema_21", result.columns)


    def test_ema_34(self):

        result = self.calculator.compute(
            self.df,
            ["ema_34"],
        )

        self.assertIn("ema_34", result.columns)


    def test_ema_50(self):

        result = self.calculator.compute(
            self.df,
            ["ema_50"],
        )

        self.assertIn("ema_50", result.columns)


    def test_ema_100(self):

        result = self.calculator.compute(
            self.df,
            ["ema_100"],
        )

        self.assertIn("ema_100", result.columns)


    def test_ema_200(self):

        result = self.calculator.compute(
            self.df,
            ["ema_200"],
        )

        self.assertIn("ema_200", result.columns)
    def test_sma_5(self):

        result = self.calculator.compute(
            self.df,
            ["sma_5"],
        )

        self.assertIn(
            "sma_5",
            result.columns,
        )


    def test_sma_10(self):

        result = self.calculator.compute(
            self.df,
            ["sma_10"],
        )

        self.assertIn(
            "sma_10",
            result.columns,
        )


    def test_sma_20(self):

        result = self.calculator.compute(
            self.df,
            ["sma_20"],
        )

        self.assertIn(
            "sma_20",
            result.columns,
        )


    def test_sma_50(self):

        result = self.calculator.compute(
            self.df,
            ["sma_50"],
        )

        self.assertIn(
            "sma_50",
            result.columns,
        )


    def test_sma_100(self):

        result = self.calculator.compute(
            self.df,
            ["sma_100"],
        )

        self.assertIn(
            "sma_100",
            result.columns,
        )


    def test_sma_200(self):

        result = self.calculator.compute(
            self.df,
            ["sma_200"],
        )

        self.assertIn(
            "sma_200",
            result.columns,
        )
    def test_distance_from_ema20(self):

        result = self.calculator.compute(
            self.df,
            ["distance_from_ema20"],
        )

        self.assertIn(
            "distance_from_ema20",
            result.columns,
        )


    def test_distance_from_ema50(self):

        result = self.calculator.compute(
            self.df,
            ["distance_from_ema50"],
        )

        self.assertIn(
            "distance_from_ema50",
            result.columns,
        )


    def test_distance_from_ema200(self):

        result = self.calculator.compute(
            self.df,
            ["distance_from_ema200"],
        )

        self.assertIn(
            "distance_from_ema200",
            result.columns,
        )


    def test_distance_from_sma20(self):

        result = self.calculator.compute(
            self.df,
            ["distance_from_sma20"],
        )

        self.assertIn(
            "distance_from_sma20",
            result.columns,
        )


    def test_distance_from_sma50(self):

        result = self.calculator.compute(
            self.df,
            ["distance_from_sma50"],
        )

        self.assertIn(
            "distance_from_sma50",
            result.columns,
        )


    def test_distance_from_sma200(self):

        result = self.calculator.compute(
            self.df,
            ["distance_from_sma200"],
        )

        self.assertIn(
            "distance_from_sma200",
            result.columns,
        )


    def test_ema20_slope(self):

        result = self.calculator.compute(
            self.df,
            ["ema20_slope"],
        )

        self.assertIn(
            "ema20_slope",
            result.columns,
        )


    def test_ema50_slope(self):

        result = self.calculator.compute(
            self.df,
            ["ema50_slope"],
        )

        self.assertIn(
            "ema50_slope",
            result.columns,
        )


    def test_ema200_slope(self):

        result = self.calculator.compute(
            self.df,
            ["ema200_slope"],
        )

        self.assertIn(
            "ema200_slope",
            result.columns,
        )