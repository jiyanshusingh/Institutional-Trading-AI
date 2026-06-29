from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import AverageTrueRange


class IndicatorEngine:

    def calculate(self, df):

        df = df.copy()

        # EMA
        df["EMA20"] = EMAIndicator(df["Close"], window=20).ema_indicator()
        df["EMA50"] = EMAIndicator(df["Close"], window=50).ema_indicator()
        df["EMA200"] = EMAIndicator(df["Close"], window=200).ema_indicator()

        # RSI
        df["RSI"] = RSIIndicator(df["Close"], window=14).rsi()

        # MACD
        macd = MACD(df["Close"])

        df["MACD"] = macd.macd()
        df["MACD_SIGNAL"] = macd.macd_signal()
        df["MACD_HIST"] = macd.macd_diff()

        # ATR
        atr = AverageTrueRange(
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )

        df["ATR"] = atr.average_true_range()

        return df