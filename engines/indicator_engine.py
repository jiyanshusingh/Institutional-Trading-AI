from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

from config.trading_config import (
    EMA_FAST,
    EMA_MEDIUM,
    EMA_SLOW,
    RSI_PERIOD,
    ATR_PERIOD,
)


class IndicatorEngine:

    def calculate(self, df):

        df = df.copy()

        # =====================================================
        # Trend Indicators
        # =====================================================

        df["EMA20"] = EMAIndicator(
            df["Close"],
            window=EMA_FAST
        ).ema_indicator()

        df["EMA50"] = EMAIndicator(
            df["Close"],
            window=EMA_MEDIUM
        ).ema_indicator()

        df["EMA200"] = EMAIndicator(
            df["Close"],
            window=EMA_SLOW
        ).ema_indicator()

        # =====================================================
        # Momentum Indicators
        # =====================================================

        df["RSI"] = RSIIndicator(
            df["Close"],
            window=RSI_PERIOD
        ).rsi()

        macd = MACD(df["Close"])

        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()
        df["MACD_HIST"] = macd.macd_diff()

        # =====================================================
        # Volatility Indicators
        # =====================================================

        atr = AverageTrueRange(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            window=ATR_PERIOD
        )

        df["ATR"] = atr.average_true_range()

        return df