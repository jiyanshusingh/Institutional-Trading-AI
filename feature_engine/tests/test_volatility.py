import unittest

import pandas as pd

from feature_engine.feature_calculator import FeatureCalculator


class TestVolatilityFeatures(unittest.TestCase):

    def setUp(self):

        self.calculator = FeatureCalculator()

        self.df = pd.DataFrame(
            {
                "open":  [100, 102, 101, 105, 108,
                          109, 110, 112, 111, 113,
                          115, 114, 116, 118, 120,
                          119, 121, 123, 122, 124],

                "high":  [105, 104, 106, 108, 110,
                          111, 113, 114, 115, 116,
                          117, 118, 120, 122, 123,
                          124, 126, 127, 128, 130],

                "low":   [99, 100, 100, 103, 106,
                          108, 109, 110, 109, 112,
                          113, 112, 115, 116, 118,
                          117, 119, 121, 120, 123],

                "close": [104, 101, 105, 107, 109,
                          110, 112, 111, 114, 115,
                          116, 117, 119, 121, 122,
                          123, 125, 126, 127, 129],

                "volume": [
                    1000, 1200, 900, 1500, 1800,
                    1700, 1650, 1750, 1600, 1550,
                    1800, 1900, 2000, 2100, 2200,
                    2050, 2150, 2250, 2350, 2400,
                ],
            }
        )

    # =====================================================
    # True Range
    # =====================================================

    def test_true_range(self):

        result = self.calculator.compute(
            self.df,
            ["true_range"],
        )

        self.assertIn(
            "true_range",
            result.columns,
        )

    # =====================================================
    # ATR 5
    # =====================================================

    def test_atr_5(self):

        result = self.calculator.compute(
            self.df,
            ["atr_5"],
        )

        self.assertIn(
            "atr_5",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[4, "atr_5"])
        )

    # =====================================================
    # ATR 10
    # =====================================================

    def test_atr_10(self):

        result = self.calculator.compute(
            self.df,
            ["atr_10"],
        )

        self.assertIn(
            "atr_10",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[9, "atr_10"])
        )

    # =====================================================
    # ATR 14
    # =====================================================

    def test_atr_14(self):

        result = self.calculator.compute(
            self.df,
            ["atr_14"],
        )

        self.assertIn(
            "atr_14",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[13, "atr_14"])
        )

    # =====================================================
    # ATR 20
    # =====================================================

    def test_atr_20(self):

        result = self.calculator.compute(
            self.df,
            ["atr_20"],
        )

        self.assertIn(
            "atr_20",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[19, "atr_20"])
        )

    # =====================================================
    # Range MA 5
    # =====================================================

    def test_range_ma_5(self):

        result = self.calculator.compute(
            self.df,
            ["range_ma_5"],
        )

        self.assertIn(
            "range_ma_5",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[4, "range_ma_5"])
        )

    # =====================================================
    # Range MA 10
    # =====================================================

    def test_range_ma_10(self):

        result = self.calculator.compute(
            self.df,
            ["range_ma_10"],
        )

        self.assertIn(
            "range_ma_10",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[9, "range_ma_10"])
        )

    # =====================================================
    # Range MA 20
    # =====================================================

    def test_range_ma_20(self):

        result = self.calculator.compute(
            self.df,
            ["range_ma_20"],
        )

        self.assertIn(
            "range_ma_20",
            result.columns,
        )

        self.assertFalse(
            pd.isna(result.loc[19, "range_ma_20"])
        )

    # =====================================================
    # Range Expansion
    # =====================================================

    def test_range_expansion(self):

        result = self.calculator.compute(
            self.df,
            ["range_expansion"],
        )

        self.assertIn(
            "range_expansion",
            result.columns,
        )

    # =====================================================
    # Range Contraction
    # =====================================================

    def test_range_contraction(self):

        result = self.calculator.compute(
            self.df,
            ["range_contraction"],
        )

        self.assertIn(
            "range_contraction",
            result.columns,
        )
    def test_atr_percent_5(self):

        result = self.calculator.compute(
            self.df,
            ["atr_percent_5"],
        )

        self.assertIn(
            "atr_percent_5",
            result.columns,
        )


    def test_atr_percent_10(self):

        result = self.calculator.compute(
            self.df,
            ["atr_percent_10"],
        )

        self.assertIn(
            "atr_percent_10",
            result.columns,
        )


    def test_atr_percent_14(self):

        result = self.calculator.compute(
            self.df,
            ["atr_percent_14"],
        )

        self.assertIn(
            "atr_percent_14",
            result.columns,
        )


    def test_atr_percent_20(self):

        result = self.calculator.compute(
            self.df,
            ["atr_percent_20"],
        )

        self.assertIn(
            "atr_percent_20",
            result.columns,
        )
    def test_std_5(self):

        result = self.calculator.compute(
            self.df,
            ["std_5"],
        )

        self.assertIn(
            "std_5",
            result.columns,
        )


    def test_std_10(self):

        result = self.calculator.compute(
            self.df,
            ["std_10"],
        )

        self.assertIn(
            "std_10",
            result.columns,
        )


    def test_std_20(self):

        result = self.calculator.compute(
            self.df,
            ["std_20"],
        )

        self.assertIn(
            "std_20",
            result.columns,
        )


    def test_variance_5(self):

        result = self.calculator.compute(
            self.df,
            ["variance_5"],
        )

        self.assertIn(
            "variance_5",
            result.columns,
        )


    def test_variance_10(self):

        result = self.calculator.compute(
            self.df,
            ["variance_10"],
        )

        self.assertIn(
            "variance_10",
            result.columns,
        )


    def test_variance_20(self):

        result = self.calculator.compute(
            self.df,
            ["variance_20"],
        )

        self.assertIn(
            "variance_20",
            result.columns,
        )
    def test_atr_ratio(self):

        result = self.calculator.compute(
            self.df,
            ["atr_ratio"],
        )

        self.assertIn(
            "atr_ratio",
            result.columns,
        )


    def test_volatility_expansion(self):

        result = self.calculator.compute(
            self.df,
            ["volatility_expansion"],
        )

        self.assertIn(
            "volatility_expansion",
            result.columns,
        )


    def test_volatility_compression(self):

        result = self.calculator.compute(
            self.df,
            ["volatility_compression"],
        )

        self.assertIn(
            "volatility_compression",
            result.columns,
        )


if __name__ == "__main__":

    unittest.main()