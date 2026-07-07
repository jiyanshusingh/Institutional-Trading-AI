import unittest
import pandas as pd

from feature_engine.feature_calculator import FeatureCalculator


class TestMomentumFeatures(unittest.TestCase):

    def setUp(self):

        self.calculator = FeatureCalculator()

        self.df = pd.DataFrame({

            "open": range(1, 301),

            "high": [x + 1 for x in range(1, 301)],

            "low": [x - 1 for x in range(1, 301)],

            "close": range(1, 301),

            "volume": [1000] * 300,

        })

    def test_rsi_7(self):

        result = self.calculator.compute(
            self.df,
            ["rsi_7"],
        )

        self.assertIn(
            "rsi_7",
            result.columns,
        )


    def test_rsi_14(self):

        result = self.calculator.compute(
            self.df,
            ["rsi_14"],
        )

        self.assertIn(
            "rsi_14",
            result.columns,
        )


    def test_rsi_21(self):

        result = self.calculator.compute(
            self.df,
            ["rsi_21"],
        )

        self.assertIn(
            "rsi_21",
            result.columns,
        )


    def test_roc_5(self):

        result = self.calculator.compute(
            self.df,
            ["roc_5"],
        )

        self.assertIn(
            "roc_5",
            result.columns,
        )


    def test_roc_10(self):

        result = self.calculator.compute(
            self.df,
            ["roc_10"],
        )

        self.assertIn(
            "roc_10",
            result.columns,
        )


    def test_roc_20(self):

        result = self.calculator.compute(
            self.df,
            ["roc_20"],
        )

        self.assertIn(
            "roc_20",
            result.columns,
        )
    def test_momentum_5(self):

        result = self.calculator.compute(
            self.df,
            ["momentum_5"],
        )

        self.assertIn(
            "momentum_5",
            result.columns,
        )


    def test_momentum_10(self):

        result = self.calculator.compute(
            self.df,
            ["momentum_10"],
        )

        self.assertIn(
            "momentum_10",
            result.columns,
        )


    def test_momentum_20(self):

        result = self.calculator.compute(
            self.df,
            ["momentum_20"],
        )

        self.assertIn(
            "momentum_20",
            result.columns,
        )


    def test_macd(self):

        result = self.calculator.compute(
            self.df,
            ["macd"],
        )

        self.assertIn(
            "macd",
            result.columns,
        )


    def test_macd_signal(self):

        result = self.calculator.compute(
            self.df,
            ["macd_signal"],
        )

        self.assertIn(
            "macd_signal",
            result.columns,
        )


    def test_macd_histogram(self):

        result = self.calculator.compute(
            self.df,
            ["macd_histogram"],
        )

        self.assertIn(
            "macd_histogram",
            result.columns,
        )
    def test_stochastic_k(self):

        result = self.calculator.compute(
            self.df,
            ["stochastic_k"],
        )

        self.assertIn(
            "stochastic_k",
            result.columns,
        )


    def test_stochastic_d(self):

        result = self.calculator.compute(
            self.df,
            ["stochastic_d"],
        )

        self.assertIn(
            "stochastic_d",
            result.columns,
        )


    def test_williams_r(self):

        result = self.calculator.compute(
            self.df,
            ["williams_r"],
        )

        self.assertIn(
            "williams_r",
            result.columns,
        )


    def test_cci_20(self):

        result = self.calculator.compute(
            self.df,
            ["cci_20"],
        )

        self.assertIn(
            "cci_20",
            result.columns,
        )